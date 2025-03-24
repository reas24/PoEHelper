import os
import json
import logging
from datetime import datetime
import time
import threading
import requests
from flask import Flask, render_template, jsonify
from data_collector import DataCollector
from analysis_engine import AnalysisEngine
from data_integration import DataIntegration
from config import (
    CURRENT_LEAGUES, PRIMARY_LEAGUE, UPDATE_INTERVAL,
    TEMPLATES_DIR, STATIC_DIR, OUTPUT_DIR, get_platform_path, ensure_dir_exists
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder=get_platform_path(TEMPLATES_DIR),
            static_folder=get_platform_path(STATIC_DIR))

# Initialize components
data_collector = DataCollector()
analysis_engine = AnalysisEngine()
data_integration = DataIntegration()

# Global variables
last_update_time = 0
opportunities = None
update_lock = threading.Lock()
initialization_complete = False

@app.route('/')
def index():
    """Render the main page"""
    # Ensure data is initialized before serving the page
    global initialization_complete
    if not initialization_complete:
        initialize_data()
    return render_template('index.html')

@app.route('/api/opportunities')
def get_opportunities():
    """Get the current profit opportunities"""
    global opportunities, initialization_complete
    
    # If opportunities is None or initialization is not complete, initialize data
    if opportunities is None or not initialization_complete:
        initialize_data()
    
    # Return the opportunities
    return jsonify(opportunities)

@app.route('/api/update')
def trigger_update():
    """Trigger a manual update of the data and analysis"""
    update_data()
    return jsonify({'status': 'success', 'message': 'Data updated successfully'})

@app.route('/api/leagues')
def get_leagues():
    """Get the available leagues"""
    return jsonify({'leagues': CURRENT_LEAGUES, 'primary': PRIMARY_LEAGUE})

@app.route('/api/status')
def get_status():
    """Get the current status of the tool"""
    global last_update_time, initialization_complete
    
    # If initialization is not complete, return appropriate status
    if not initialization_complete:
        return jsonify({
            'last_update': None,
            'next_update': 0,
            'update_interval': UPDATE_INTERVAL,
            'status': 'initializing'
        })
    
    # Calculate time since last update
    time_since_update = time.time() - last_update_time
    next_update = max(0, UPDATE_INTERVAL - time_since_update)
    
    status = {
        'last_update': datetime.fromtimestamp(last_update_time).isoformat() if last_update_time > 0 else None,
        'next_update': int(next_update),
        'update_interval': UPDATE_INTERVAL,
        'status': 'ready'
    }
    
    return jsonify(status)

@app.route('/api/currency_data')
def get_currency_data():
    """Get currency data for charts"""
    try:
        # Get current league data
        league_dir = get_platform_path(os.path.join(OUTPUT_DIR, 'data', 'current', PRIMARY_LEAGUE.lower()))
        market_data_file = os.path.join(league_dir, 'market_data.json')
        
        if os.path.exists(market_data_file):
            with open(market_data_file, 'r') as f:
                market_data = json.load(f)
                
            # Get top currencies by value
            currencies = market_data.get('currencies', [])
            top_currencies = sorted(
                [c for c in currencies if c.get('name') != 'Chaos Orb'],
                key=lambda x: x.get('chaos_value', 0),
                reverse=True
            )[:10]
            
            return jsonify({
                'status': 'success',
                'currencies': top_currencies
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Market data file not found'
            })
    except Exception as e:
        logger.error(f"Error getting currency data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/historical_data')
def get_historical_data():
    """Get historical data for charts"""
    try:
        # Get historical data
        historical_data_file = get_platform_path(os.path.join(OUTPUT_DIR, 'data', 'historical', 'historical_data.json'))
        
        if os.path.exists(historical_data_file):
            with open(historical_data_file, 'r') as f:
                historical_data = json.load(f)
            
            # Create datasets for the top currencies
            datasets = []
            
            # Get top currencies
            league_dir = get_platform_path(os.path.join(OUTPUT_DIR, 'data', 'current', PRIMARY_LEAGUE.lower()))
            market_data_file = os.path.join(league_dir, 'market_data.json')
            
            if os.path.exists(market_data_file):
                with open(market_data_file, 'r') as f:
                    market_data = json.load(f)
                
                currencies = market_data.get('currencies', [])
                top_currencies = sorted(
                    [c for c in currencies if c.get('name') != 'Chaos Orb'],
                    key=lambda x: x.get('chaos_value', 0),
                    reverse=True
                )[:2]  # Get top 2 currencies
                
                colors = [
                    {'border': 'rgba(255, 99, 132, 1)', 'background': 'rgba(255, 99, 132, 0.1)'},
                    {'border': 'rgba(54, 162, 235, 1)', 'background': 'rgba(54, 162, 235, 0.1)'}
                ]
                
                # Create datasets for each currency
                for i, currency in enumerate(top_currencies):
                    currency_name = currency.get('name')
                    if currency_name in historical_data:
                        datasets.append({
                            'label': currency_name,
                            'data': historical_data[currency_name],
                            'borderColor': colors[i]['border'],
                            'backgroundColor': colors[i]['background'],
                            'tension': 0.4,
                            'fill': True
                        })
            
            return jsonify({
                'status': 'success',
                'data': datasets
            })
        else:
            # Generate sample historical data if file doesn't exist
            return jsonify({
                'status': 'success',
                'data': []
            })
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

def initialize_data():
    """Initialize data on startup"""
    global initialization_complete
    
    # If already initialized, return
    if initialization_complete:
        return
    
    # Start a thread to update with real data
    threading.Thread(target=update_data, daemon=True).start()
    
    # Mark initialization as complete
    initialization_complete = True

def update_data():
    """Update the data and analysis"""
    global last_update_time, opportunities
    
    # Use a lock to prevent multiple updates at the same time
    if not update_lock.acquire(blocking=False):
        logger.info("Update already in progress, skipping")
        return
    
    try:
        logger.info("Starting data update...")
        
        # Collect data for all leagues
        market_data = {}
        for league in CURRENT_LEAGUES:
            try:
                league_data = data_collector.collect_all_data(league)
                market_data[league] = league_data
                logger.info(f"Collected data for {league} league")
            except Exception as e:
                logger.error(f"Error collecting data for {league} league: {e}")
        
        # Integrate data from different leagues
        try:
            integrated_data = data_integration.integrate_data(market_data)
            logger.info("Integrated data from different leagues")
        except Exception as e:
            logger.error(f"Error integrating data: {e}")
            integrated_data = market_data.get(PRIMARY_LEAGUE, {})
        
        # Analyze opportunities
        try:
            opportunities = analysis_engine.analyze_all_opportunities(integrated_data)
            logger.info("Analyzed opportunities")
        except Exception as e:
            logger.error(f"Error analyzing opportunities: {e}")
            # If opportunities is None, initialize it to prevent errors
            if opportunities is None:
                opportunities = {
                    'flipping': [],
                    'farming': [],
                    'crafting': [],
                    'investment': [],
                    'timestamp': datetime.now().isoformat()
                }
        
        # Update last update time
        last_update_time = time.time()
        
        logger.info("Data update completed successfully")
        
    except Exception as e:
        logger.error(f"Error updating data: {e}")
    finally:
        update_lock.release()

def background_updater():
    """Background thread to update data periodically"""
    while True:
        try:
            # Check if it's time to update
            current_time = time.time()
            if current_time - last_update_time >= UPDATE_INTERVAL:
                update_data()
            
            # Sleep for a short time
            time.sleep(10)
        except Exception as e:
            logger.error(f"Error in background updater: {e}")
            time.sleep(30)  # Sleep longer on error

if __name__ == '__main__':
    # Ensure output directory exists
    ensure_dir_exists(get_platform_path(os.path.join(OUTPUT_DIR, 'data')))
    
    # Start the background updater in a separate thread
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
