import os
import json
import logging
from datetime import datetime
from config import (
    DATA_DIR, REFERENCE_DATA_FILE, PRIMARY_LEAGUE, HISTORICAL_LEAGUE,
    get_platform_path, ensure_dir_exists
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataIntegration:
    """Class for integrating data from different sources and leagues"""
    
    def __init__(self):
        """Initialize the data integration"""
        self.reference_data = self.load_reference_data()
    
    def load_reference_data(self):
        """Load reference data from file"""
        reference_data_file = get_platform_path(REFERENCE_DATA_FILE)
        ensure_dir_exists(os.path.dirname(reference_data_file))
        
        try:
            if os.path.exists(reference_data_file):
                with open(reference_data_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default reference data
                reference_data = {
                    'divination_cards': {},
                    'farming_locations': {},
                    'crafting_recipes': {},
                    'league_mechanics': {},
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save reference data
                with open(reference_data_file, 'w') as f:
                    json.dump(reference_data, f, indent=4)
                
                return reference_data
        except Exception as e:
            logger.error(f"Error loading reference data: {e}")
            return {
                'divination_cards': {},
                'farming_locations': {},
                'crafting_recipes': {},
                'league_mechanics': {},
                'timestamp': datetime.now().isoformat()
            }
    
    def integrate_data(self, market_data):
        """Integrate data from different leagues"""
        logger.info("Integrating data from different leagues...")
        
        try:
            # Initialize integrated data structure
            integrated_data = {
                'currencies': [],
                'fragments': [],
                'oils': [],
                'incubators': [],
                'artifacts': [],
                'divination_cards': [],
                'scarabs': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Get primary league data
            primary_data = market_data.get(PRIMARY_LEAGUE, {})
            
            # Get historical league data
            historical_data = market_data.get(HISTORICAL_LEAGUE, {})
            
            # Integrate currencies
            integrated_data['currencies'] = self.integrate_currencies(
                primary_data.get('currencies', []),
                historical_data.get('currencies', [])
            )
            
            # Integrate fragments
            integrated_data['fragments'] = self.integrate_items(
                primary_data.get('fragments', []),
                historical_data.get('fragments', [])
            )
            
            # Integrate oils
            integrated_data['oils'] = self.integrate_items(
                primary_data.get('oils', []),
                historical_data.get('oils', [])
            )
            
            # Integrate scarabs
            integrated_data['scarabs'] = self.integrate_items(
                primary_data.get('scarabs', []),
                historical_data.get('scarabs', [])
            )
            
            # Integrate incubators
            integrated_data['incubators'] = self.integrate_items(
                primary_data.get('incubators', []),
                historical_data.get('incubators', [])
            )
            
            # Integrate artifacts
            integrated_data['artifacts'] = self.integrate_items(
                primary_data.get('artifacts', []),
                historical_data.get('artifacts', [])
            )
            
            # Integrate divination cards
            integrated_data['divination_cards'] = self.integrate_items(
                primary_data.get('divination_cards', []),
                historical_data.get('divination_cards', [])
            )
            
            logger.info("Data integration completed successfully")
            
            return integrated_data
            
        except Exception as e:
            logger.error(f"Error integrating data: {e}")
            return {
                'currencies': [],
                'fragments': [],
                'oils': [],
                'incubators': [],
                'artifacts': [],
                'divination_cards': [],
                'scarabs': [],
                'timestamp': datetime.now().isoformat()
            }
    
    def integrate_currencies(self, primary_currencies, historical_currencies):
        """Integrate currency data from different leagues"""
        integrated_currencies = []
        
        try:
            # Create a dictionary of historical currencies by name
            historical_dict = {c['name']: c for c in historical_currencies if 'name' in c}
            
            # Process primary currencies
            for currency in primary_currencies:
                if 'name' not in currency:
                    continue
                
                name = currency['name']
                
                # Get historical data for this currency
                historical = historical_dict.get(name)
                
                # Create integrated currency
                integrated_currency = currency.copy()
                
                # Add historical data if available
                if historical:
                    # Calculate historical price change
                    current_value = currency.get('chaos_value', 0)
                    historical_value = historical.get('chaos_value', 0)
                    
                    if historical_value > 0:
                        historical_change = ((current_value - historical_value) / historical_value) * 100
                    else:
                        historical_change = 0
                    
                    integrated_currency['historical_value'] = historical_value
                    integrated_currency['historical_change'] = historical_change
                    
                    # Calculate price trend
                    if historical_change > 10:
                        trend = 'rising'
                    elif historical_change < -10:
                        trend = 'falling'
                    else:
                        trend = 'stable'
                    
                    integrated_currency['price_trend'] = trend
                    
                    # Calculate volatility
                    current_volatility = currency.get('volatility', 0)
                    historical_volatility = historical.get('volatility', 0)
                    
                    integrated_currency['volatility'] = max(current_volatility, historical_volatility)
                
                integrated_currencies.append(integrated_currency)
            
            return integrated_currencies
            
        except Exception as e:
            logger.error(f"Error integrating currencies: {e}")
            return primary_currencies
    
    def integrate_items(self, primary_items, historical_items):
        """Integrate item data from different leagues"""
        integrated_items = []
        
        try:
            # Create a dictionary of historical items by name
            historical_dict = {i['name']: i for i in historical_items if 'name' in i}
            
            # Process primary items
            for item in primary_items:
                if 'name' not in item:
                    continue
                
                name = item['name']
                
                # Get historical data for this item
                historical = historical_dict.get(name)
                
                # Create integrated item
                integrated_item = item.copy()
                
                # Add historical data if available
                if historical:
                    # Calculate historical price change
                    current_value = item.get('chaos_value', 0)
                    historical_value = historical.get('chaos_value', 0)
                    
                    if historical_value > 0:
                        historical_change = ((current_value - historical_value) / historical_value) * 100
                    else:
                        historical_change = 0
                    
                    integrated_item['historical_value'] = historical_value
                    integrated_item['historical_change'] = historical_change
                    
                    # Calculate price trend
                    if historical_change > 10:
                        trend = 'rising'
                    elif historical_change < -10:
                        trend = 'falling'
                    else:
                        trend = 'stable'
                    
                    integrated_item['price_trend'] = trend
                    
                    # Calculate volatility
                    current_volatility = item.get('volatility', 0)
                    historical_volatility = historical.get('volatility', 0)
                    
                    integrated_item['volatility'] = max(current_volatility, historical_volatility)
                
                # Add reference data if available
                if item.get('item_type') == 'DivinationCard':
                    integrated_item['farming_locations'] = self.get_divination_card_locations(name)
                
                integrated_items.append(integrated_item)
            
            return integrated_items
            
        except Exception as e:
            logger.error(f"Error integrating items: {e}")
            return primary_items
    
    def get_divination_card_locations(self, card_name):
        """Get farming locations for a divination card from reference data"""
        try:
            # Check if card exists in reference data
            if card_name in self.reference_data.get('divination_cards', {}):
                return self.reference_data['divination_cards'][card_name].get('farming_locations', [])
            
            # Default locations
            return ["Check PoE Wiki for specific farming locations"]
            
        except Exception as e:
            logger.error(f"Error getting divination card locations: {e}")
            return ["Check PoE Wiki for specific farming locations"]
