import os
import json
import logging
import requests
from datetime import datetime
from config import (
    POE_NINJA_API_BASE, DATA_DIR, CURRENT_LEAGUES,
    CURRENCY_TYPES, FRAGMENT_TYPES, OIL_TYPES, INCUBATOR_TYPES,
    ARTIFACT_TYPES, DIVINATION_CARD_TYPES, SCARAB_TYPES,
    CURRENCY_TYPE_URLS, ITEM_TYPE_URLS,
    get_platform_path, ensure_dir_exists
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCollector:
    """Class for collecting data from poe.ninja API"""
    
    def __init__(self):
        """Initialize the data collector"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def collect_all_data(self, league):
        """Collect all data for a specific league"""
        logger.info(f"Starting collection of all data for {league} league...")
        
        # Create directory for league data
        league_dir = get_platform_path(os.path.join(DATA_DIR, 'current', league.lower()))
        ensure_dir_exists(league_dir)
        
        # Initialize data structure
        market_data = {
            'currencies': [],
            'fragments': [],
            'oils': [],
            'incubators': [],
            'artifacts': [],
            'divination_cards': [],
            'scarabs': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Collect currency data
        for currency_type in CURRENCY_TYPES:
            try:
                logger.info(f"Fetching {currency_type} data for {league}...")
                currency_data = self._fetch_currency_data(league, currency_type)
                market_data['currencies'].extend(currency_data)
                logger.info(f"Processed {len(currency_data)} {currency_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {currency_type} data for {league}: {e}")
        
        # Collect fragment data
        for fragment_type in FRAGMENT_TYPES:
            try:
                logger.info(f"Fetching {fragment_type} data for {league}...")
                fragment_data = self._fetch_currency_data(league, fragment_type)
                market_data['fragments'].extend(fragment_data)
                logger.info(f"Processed {len(fragment_data)} {fragment_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {fragment_type} data for {league}: {e}")
        
        # Collect oil data
        for oil_type in OIL_TYPES:
            try:
                logger.info(f"Fetching {oil_type} data for {league}...")
                oil_data = self._fetch_item_data(league, oil_type)
                market_data['oils'].extend(oil_data)
                logger.info(f"Processed {len(oil_data)} {oil_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {oil_type} data for {league}: {e}")
        
        # Collect scarab data
        for scarab_type in SCARAB_TYPES:
            try:
                logger.info(f"Fetching {scarab_type} data for {league}...")
                scarab_data = self._fetch_item_data(league, scarab_type)
                market_data['scarabs'].extend(scarab_data)
                logger.info(f"Processed {len(scarab_data)} {scarab_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {scarab_type} data for {league}: {e}")
        
        # Collect incubator data
        for incubator_type in INCUBATOR_TYPES:
            try:
                logger.info(f"Fetching {incubator_type} data for {league}...")
                incubator_data = self._fetch_item_data(league, incubator_type)
                market_data['incubators'].extend(incubator_data)
                logger.info(f"Processed {len(incubator_data)} {incubator_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {incubator_type} data for {league}: {e}")
        
        # Collect artifact data
        for artifact_type in ARTIFACT_TYPES:
            try:
                logger.info(f"Fetching {artifact_type} data for {league}...")
                artifact_data = self._fetch_item_data(league, artifact_type)
                market_data['artifacts'].extend(artifact_data)
                logger.info(f"Processed {len(artifact_data)} {artifact_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {artifact_type} data for {league}: {e}")
        
        # Collect divination card data
        for div_card_type in DIVINATION_CARD_TYPES:
            try:
                logger.info(f"Fetching {div_card_type} data for {league}...")
                div_card_data = self._fetch_item_data(league, div_card_type)
                market_data['divination_cards'].extend(div_card_data)
                logger.info(f"Processed {len(div_card_data)} {div_card_type} entries for {league}")
            except Exception as e:
                logger.error(f"Error fetching {div_card_type} data for {league}: {e}")
        
        # Save data to file
        market_data_file = get_platform_path(os.path.join(league_dir, 'market_data.json'))
        with open(market_data_file, 'w') as f:
            json.dump(market_data, f, indent=4)
        
        logger.info(f"Saved market data for {league} to {market_data_file}")
        
        return market_data
    
    def _fetch_currency_data(self, league, currency_type):
        """Fetch currency data from poe.ninja API"""
        url = CURRENCY_TYPE_URLS.get(currency_type, "").format(league=league)
        logger.info(f"Fetching data from {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Process currency data
            currencies = []
            for line in data.get('lines', []):
                currency = {
                    'name': line.get('currencyTypeName'),
                    'chaos_value': line.get('chaosEquivalent'),
                    'trade_volume': line.get('receive', {}).get('count', 0),
                    'receive_change': line.get('receiveSparkLine', {}).get('totalChange', 0),
                    'pay_change': line.get('paySparkLine', {}).get('totalChange', 0),
                    'volatility': abs(line.get('receiveSparkLine', {}).get('totalChange', 0)) / 100 if line.get('receiveSparkLine', {}).get('totalChange') is not None else 0,
                    'details_id': line.get('detailsId'),
                    'currency_type': currency_type,
                    'league': league,
                    'timestamp': datetime.now().isoformat()
                }
                currencies.append(currency)
            
            return currencies
        except Exception as e:
            logger.error(f"Error fetching currency data from poe.ninja: {e}")
            return []
    
    def _fetch_item_data(self, league, item_type):
        """Fetch item data from poe.ninja API"""
        url = ITEM_TYPE_URLS.get(item_type, "").format(league=league)
        logger.info(f"Fetching data from {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Process item data
            items = []
            for line in data.get('lines', []):
                item = {
                    'name': line.get('name'),
                    'base_type': line.get('baseType'),
                    'item_type': item_type,
                    'chaos_value': line.get('chaosValue'),
                    'exalted_value': line.get('exaltedValue'),
                    'divine_value': line.get('divineValue'),
                    'trade_volume': line.get('count', 0),
                    'price_change': line.get('sparkline', {}).get('totalChange', 0),
                    'volatility': abs(line.get('sparkline', {}).get('totalChange', 0)) / 100 if line.get('sparkline', {}).get('totalChange') is not None else 0,
                    'details_id': line.get('detailsId'),
                    'league': league,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add additional fields based on item type
                if item_type == 'DivinationCard':
                    # Try to get farming locations from wiki or reference data
                    item['farming_locations'] = self._get_divination_card_locations(line.get('name'))
                
                if item_type == 'Scarab':
                    # Add scarab-specific information
                    item['effect'] = self._extract_scarab_effect(line.get('explicitModifiers', []))
                    item['investment_rating'] = self._calculate_investment_rating(
                        line.get('chaosValue', 0), 
                        line.get('sparkline', {}).get('totalChange', 0),
                        line.get('count', 0)
                    )
                
                if 'stackSize' in line:
                    item['stack_size'] = line.get('stackSize')
                
                if 'levelRequired' in line:
                    item['level'] = line.get('levelRequired')
                
                if 'links' in line:
                    item['links'] = line.get('links')
                
                if 'gemQuality' in line:
                    item['quality'] = line.get('gemQuality')
                
                if 'corrupted' in line:
                    item['corrupted'] = line.get('corrupted', False)
                
                items.append(item)
            
            return items
        except Exception as e:
            logger.error(f"Error fetching item data from poe.ninja: {e}")
            return []
    
    def _extract_scarab_effect(self, modifiers):
        """Extract the effect description from scarab modifiers"""
        if not modifiers:
            return "Unknown effect"
        
        for modifier in modifiers:
            if isinstance(modifier, dict) and 'text' in modifier:
                return modifier['text']
        
        return "Unknown effect"
    
    def _calculate_investment_rating(self, price, price_change, volume):
        """Calculate an investment rating for items based on price, change, and volume"""
        # Higher volume, higher price change (positive), and moderate price
        # result in a better investment rating
        
        # Normalize values
        price_factor = min(1.0, 50 / max(1, price))  # Lower prices get higher factor
        change_factor = (price_change / 100) + 0.5  # Normalize to 0-1 range, 0.5 is neutral
        volume_factor = min(1.0, volume / 200)  # Higher volume is better
        
        # Calculate weighted score (0-100)
        score = (price_factor * 0.3 + change_factor * 0.5 + volume_factor * 0.2) * 100
        
        return round(score, 1)
    
    def _get_divination_card_locations(self, card_name):
        """Get farming locations for a divination card from reference data"""
        # In a real implementation, we would fetch this data from the PoE wiki
        # For now, we'll return a placeholder
        return ["Check PoE Wiki for specific farming locations"]

# For testing
if __name__ == "__main__":
    collector = DataCollector()
    data = collector.collect_all_data("Phrecia")
    print(f"Collected {len(data['currencies'])} currencies")
    print(f"Collected {len(data['fragments'])} fragments")
    print(f"Collected {len(data['oils'])} oils")
    print(f"Collected {len(data['scarabs'])} scarabs")
