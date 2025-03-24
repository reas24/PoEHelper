import requests
import json
import time
import logging
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("poe_economy_tool.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class POETradeAPI:
    """
    Class to interact with the official Path of Exile Trade API
    https://www.pathofexile.com/developer/docs/api-resources
    """
    
    def __init__(self):
        """Initialize the POE Trade API client"""
        self.base_url = "https://www.pathofexile.com/api"
        self.trade_url = f"{self.base_url}/trade"
        self.headers = {
            'User-Agent': 'POE-Economy-Analysis-Tool/1.0 (contact@example.com)',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.rate_limit_delay = 1.0  # Seconds between requests to avoid rate limiting
        
    def get_leagues(self):
        """
        Get a list of currently active leagues
        
        Returns:
            list: List of league data
        """
        url = f"{self.base_url}/leagues"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(self.rate_limit_delay)
            
            leagues = response.json()
            return leagues
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching leagues: {e}")
            return []
    
    def search_items(self, league, query, sort="price", limit=10):
        """
        Search for items using the trade API
        
        Args:
            league (str): League name (e.g., 'Phrecia', 'Settlers')
            query (dict): Search query parameters
            sort (str): Sort order (default: "price")
            limit (int): Maximum number of results to return
            
        Returns:
            dict: Search results
        """
        search_url = f"{self.trade_url}/search/{league}"
        
        # Prepare the search payload
        payload = {
            "query": query,
            "sort": {"price": "asc"},
            "limit": limit
        }
        
        try:
            # Step 1: Get search results
            search_response = requests.post(search_url, headers=self.headers, json=payload)
            search_response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(self.rate_limit_delay)
            
            search_data = search_response.json()
            
            if not search_data.get('result'):
                logger.warning(f"No results found for query in {league}")
                return {"items": [], "total": 0}
            
            # Step 2: Fetch item details
            result_ids = search_data['result'][:limit]
            fetch_url = f"{self.trade_url}/fetch/{','.join(result_ids)}"
            
            fetch_response = requests.get(fetch_url, headers=self.headers)
            fetch_response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(self.rate_limit_delay)
            
            fetch_data = fetch_response.json()
            
            return {
                "items": fetch_data.get('result', []),
                "total": search_data.get('total', 0)
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching items: {e}")
            return {"items": [], "total": 0}
    
    def get_currency_rates(self, league):
        """
        Get current currency exchange rates
        
        Args:
            league (str): League name (e.g., 'Phrecia', 'Settlers')
            
        Returns:
            dict: Currency exchange rates
        """
        # Currency types to check (common currencies)
        currencies = [
            "divine", "exalted", "chaos", "ancient", "annulment", "awakener", 
            "blessing-chayula", "blessing-esh", "blessing-tul", "blessing-uul", "blessing-xoph",
            "crusader", "elder", "hunter", "redeemer", "shaper", "warlord",
            "veiled-chaos", "vaal", "regal", "orb-of-regret", "orb-of-scouring",
            "orb-of-alchemy", "orb-of-alteration", "orb-of-chance", "orb-of-fusing",
            "jewellers-orb", "chromatic-orb", "orb-of-horizons", "harbinger-orb",
            "gemcutters-prism", "glassblowers-bauble", "blessed-orb", "orb-of-binding",
            "orb-of-engineering", "orb-of-transmutation", "mirror"
        ]
        
        currency_rates = {}
        
        for currency in currencies:
            # Query for selling chaos orbs for the target currency
            chaos_to_currency_query = {
                "query": {
                    "status": {"option": "online"},
                    "have": ["chaos"],
                    "want": [currency]
                }
            }
            
            # Query for selling the target currency for chaos orbs
            currency_to_chaos_query = {
                "query": {
                    "status": {"option": "online"},
                    "have": [currency],
                    "want": ["chaos"]
                }
            }
            
            # Get exchange rates
            chaos_to_currency_results = self.search_currency_exchange(league, chaos_to_currency_query)
            time.sleep(self.rate_limit_delay + random.uniform(0.5, 1.5))  # Add random delay
            
            currency_to_chaos_results = self.search_currency_exchange(league, currency_to_chaos_query)
            time.sleep(self.rate_limit_delay + random.uniform(0.5, 1.5))  # Add random delay
            
            # Process results
            buy_rate = self.process_exchange_results(chaos_to_currency_results)
            sell_rate = self.process_exchange_results(currency_to_chaos_results, invert=True)
            
            currency_rates[currency] = {
                "buy_rate": buy_rate,  # How many of this currency you get for 1 chaos
                "sell_rate": sell_rate,  # How many chaos you get for 1 of this currency
                "spread": sell_rate - buy_rate if buy_rate and sell_rate else None
            }
        
        return currency_rates
    
    def search_currency_exchange(self, league, query):
        """
        Search for currency exchange listings
        
        Args:
            league (str): League name (e.g., 'Phrecia', 'Settlers')
            query (dict): Search query parameters
            
        Returns:
            dict: Exchange listings
        """
        exchange_url = f"{self.trade_url}/exchange/{league}"
        
        try:
            response = requests.post(exchange_url, headers=self.headers, json=query)
            response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(self.rate_limit_delay)
            
            exchange_data = response.json()
            
            if not exchange_data.get('result'):
                return {"listings": [], "total": 0}
            
            # Fetch first 10 exchange listings
            result_ids = exchange_data['result'][:10]
            fetch_url = f"{self.trade_url}/fetch/{','.join(result_ids)}"
            
            fetch_response = requests.get(fetch_url, headers=self.headers)
            fetch_response.raise_for_status()
            
            # Add delay to avoid rate limiting
            time.sleep(self.rate_limit_delay)
            
            fetch_data = fetch_response.json()
            
            return {
                "listings": fetch_data.get('result', []),
                "total": exchange_data.get('total', 0)
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching currency exchange: {e}")
            return {"listings": [], "total": 0}
    
    def process_exchange_results(self, results, invert=False):
        """
        Process currency exchange results to get average rate
        
        Args:
            results (dict): Exchange results
            invert (bool): Whether to invert the rate (for currency to chaos)
            
        Returns:
            float: Average exchange rate
        """
        if not results or not results.get('listings'):
            return None
        
        rates = []
        
        for listing in results.get('listings', []):
            if 'price' not in listing:
                continue
                
            price = listing['price']
            
            if 'amount' not in price or 'exchange' not in price:
                continue
                
            amount = price['amount']
            exchange_amount = price['exchange']['amount']
            
            if amount <= 0 or exchange_amount <= 0:
                continue
                
            # Calculate rate
            rate = exchange_amount / amount if not invert else amount / exchange_amount
            rates.append(rate)
        
        # Return average rate if we have data
        if rates:
            # Filter out outliers (values more than 2 standard deviations from mean)
            if len(rates) > 5:
                mean = sum(rates) / len(rates)
                std_dev = (sum((x - mean) ** 2 for x in rates) / len(rates)) ** 0.5
                filtered_rates = [r for r in rates if abs(r - mean) <= 2 * std_dev]
                return sum(filtered_rates) / len(filtered_rates) if filtered_rates else None
            else:
                return sum(rates) / len(rates)
        else:
            return None
    
    def get_item_price_check(self, league, item_type, item_name, additional_filters=None):
        """
        Get price check for a specific item
        
        Args:
            league (str): League name (e.g., 'Phrecia', 'Settlers')
            item_type (str): Type of item (e.g., 'unique', 'currency', 'divination_card')
            item_name (str): Name of the item
            additional_filters (dict): Additional filters for the search
            
        Returns:
            dict: Price check results
        """
        # Build query based on item type
        query = {
            "query": {
                "status": {"option": "online"},
                "name": item_name,
                "type": item_type
            }
        }
        
        # Add additional filters if provided
        if additional_filters:
            query["query"].update(additional_filters)
        
        # Search for the item
        results = self.search_items(league, query)
        
        # Process results to get price statistics
        prices = []
        for item in results.get('items', []):
            if 'listing' not in item:
                continue
                
            listing = item['listing']
            
            if 'price' not in listing:
                continue
                
            price = listing['price']
            
            if 'amount' not in price or 'currency' not in price:
                continue
                
            amount = price['amount']
            currency = price['currency']
            
            prices.append({
                'amount': amount,
                'currency': currency
            })
        
        # Calculate statistics
        if prices:
            # Filter to only chaos and divine prices for simplicity
            chaos_prices = [p['amount'] for p in prices if p['currency'] == 'chaos']
            divine_prices = [p['amount'] for p in prices if p['currency'] == 'divine']
            
            stats = {}
            
            if chaos_prices:
                stats['chaos'] = {
                    'min': min(chaos_prices),
                    'max': max(chaos_prices),
                    'mean': sum(chaos_prices) / len(chaos_prices),
                    'median': sorted(chaos_prices)[len(chaos_prices) // 2],
                    'count': len(chaos_prices)
                }
            
            if divine_prices:
                stats['divine'] = {
                    'min': min(divine_prices),
                    'max': max(divine_prices),
                    'mean': sum(divine_prices) / len(divine_prices),
                    'median': sorted(divine_prices)[len(divine_prices) // 2],
                    'count': len(divine_prices)
                }
            
            return {
                'item_name': item_name,
                'item_type': item_type,
                'league': league,
                'total_listings': results.get('total', 0),
                'prices': prices[:10],  # Include first 10 raw prices
                'stats': stats,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'item_name': item_name,
                'item_type': item_type,
                'league': league,
                'total_listings': 0,
                'prices': [],
                'stats': {},
                'timestamp': datetime.now().isoformat()
            }
    
    def get_meta_items(self, league, category, limit=20):
        """
        Get most traded/valuable items in a category to identify meta items
        
        Args:
            league (str): League name (e.g., 'Phrecia', 'Settlers')
            category (str): Item category (e.g., 'weapon', 'armour', 'jewel')
            limit (int): Maximum number of results to return
            
        Returns:
            list: Meta items
        """
        # Build query for the category
        query = {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {
                        "filters": {
                            "category": {
                                "option": category
                            }
                        }
                    }
                }
            },
            "sort": {"price": "desc"}  # Sort by highest price first
        }
        
        # Search for items
        results = self.search_items(league, query, limit=limit)
        
        # Process results to get meta items
        meta_items = []
        for item in results.get('items', []):
            if 'listing' not in item or 'item' not in item:
                continue
                
            listing = item['listing']
            item_data = item['item']
            
            if 'price' not in listing or 'name' not in item_data:
                continue
                
            price = listing['price']
            name = item_data['name']
            
            if 'amount' not in price or 'currency' not in price:
                continue
                
            meta_items.append({
                'name': name,
                'type': item_data.get('typeLine', ''),
                'price_amount': price['amount'],
                'price_currency': price['currency'],
                'ilvl': item_data.get('ilvl', 0),
                'links': len(item_data.get('sockets', [])) if 'sockets' in item_data else 0,
                'corrupted': item_data.get('corrupted', False),
                'mods': [mod['text'] for mod in item_data.get('explicitMods', [])] if 'explicitMods' in item_data else []
            })
        
        return meta_items

# Example usage
if __name__ == "__main__":
    api = POETradeAPI()
    
    # Get active leagues
    leagues = api.get_leagues()
    print(f"Active leagues: {[league['id'] for league in leagues]}")
    
    # Get currency rates for a league
    rates = api.get_currency_rates("Phrecia")
    print(f"Currency rates: {rates}")
    
    # Price check for a specific item
    price_check = api.get_item_price_check("Phrecia", "The Doctor", "Divination Card")
    print(f"Price check: {price_check}")
    
    # Get meta items
    meta_items = api.get_meta_items("Phrecia", "weapon")
    print(f"Meta items: {meta_items}")
