import os
import json
import logging
from datetime import datetime
import time
from config import (
    CURRENT_LEAGUES, PRIMARY_LEAGUE, HISTORICAL_LEAGUE,
    OUTPUT_DIR, get_platform_path, ensure_dir_exists
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalysisEngine:
    """Class for analyzing market data and identifying profit opportunities"""
    
    def __init__(self):
        """Initialize the analysis engine"""
        self.opportunities = {
            'flipping': [],
            'farming': [],
            'crafting': [],
            'investment': [],
            'timestamp': None
        }
        self.last_analysis = None
    
    def analyze_all_opportunities(self, market_data):
        """Analyze all profit opportunities"""
        logger.info("Analyzing profit opportunities...")
        
        try:
            # Initialize opportunities structure
            self.opportunities = {
                'flipping': [],
                'farming': [],
                'crafting': [],
                'investment': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Analyze flipping opportunities
            self.opportunities['flipping'] = self.analyze_flipping_opportunities(market_data)
            logger.info(f"Identified {len(self.opportunities['flipping'])} flipping opportunities")
            
            # Analyze farming opportunities
            self.opportunities['farming'] = self.analyze_farming_opportunities(market_data)
            logger.info(f"Identified {len(self.opportunities['farming'])} farming opportunities")
            
            # Analyze crafting opportunities
            self.opportunities['crafting'] = self.analyze_crafting_opportunities(market_data)
            logger.info(f"Identified {len(self.opportunities['crafting'])} crafting opportunities")
            
            # Analyze investment opportunities
            self.opportunities['investment'] = self.analyze_investment_opportunities(market_data)
            logger.info(f"Identified {len(self.opportunities['investment'])} investment opportunities")
            
            # Save opportunities to file
            opportunities_file = get_platform_path(os.path.join(OUTPUT_DIR, 'data', 'profit_opportunities.json'))
            ensure_dir_exists(os.path.dirname(opportunities_file))
            with open(opportunities_file, 'w') as f:
                json.dump(self.opportunities, f, indent=4)
            
            logger.info(f"Saved opportunities to {opportunities_file}")
            
            return self.opportunities
                
        except Exception as e:
            logger.error(f"Error analyzing opportunities: {e}")
            # Initialize timestamp if it's None to prevent NoneType errors
            if self.opportunities['timestamp'] is None:
                self.opportunities['timestamp'] = datetime.now().isoformat()
            return self.opportunities
    
    def get_opportunities(self):
        """Get the analyzed opportunities"""
        # Ensure timestamp is not None to prevent NoneType errors
        if self.opportunities['timestamp'] is None:
            self.opportunities['timestamp'] = datetime.now().isoformat()
            
        return self.opportunities
    
    def analyze_flipping_opportunities(self, market_data):
        """Analyze currency flipping opportunities"""
        flipping_opportunities = []
        
        try:
            # Get all currencies and fragments
            currencies = market_data.get('currencies', [])
            fragments = market_data.get('fragments', [])
            all_currencies = currencies + fragments
            
            # Create a dictionary of currency names to chaos values
            currency_values = {item['name']: item['chaos_value'] for item in all_currencies if 'chaos_value' in item}
            
            # Find direct flipping opportunities (single-step)
            for currency in all_currencies:
                if 'chaos_value' not in currency or 'receive_change' not in currency:
                    continue
                
                # Calculate volatility and potential profit
                volatility = abs(currency.get('receive_change', 0)) / 100 if currency.get('receive_change') is not None else 0
                potential_profit = volatility * currency.get('chaos_value', 0) * 0.1  # Estimate 10% of value as potential profit
                
                # Only include currencies with significant volatility and value
                if volatility > 0.05 and currency.get('chaos_value', 0) > 5:
                    opportunity = {
                        'type': 'single-step',
                        'currency': currency['name'],
                        'chaos_value': currency.get('chaos_value', 0),
                        'volatility': volatility,
                        'potential_profit': potential_profit,
                        'strategy': f"Buy {currency['name']} when price drops, sell when price rises. Current price: {currency.get('chaos_value', 0)} chaos.",
                        'opportunity_score': self.calculate_opportunity_score(potential_profit / currency.get('chaos_value', 1), volatility, currency.get('trade_volume', 0)),
                        'league': currency.get('league', PRIMARY_LEAGUE)
                    }
                    flipping_opportunities.append(opportunity)
            
            # Find multi-step flipping opportunities
            multi_step_opportunities = self.find_multi_step_flips(all_currencies, currency_values)
            flipping_opportunities.extend(multi_step_opportunities)
            
            # Sort opportunities by opportunity score
            flipping_opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
            
            # Limit to top 20 opportunities
            return flipping_opportunities[:20]
            
        except Exception as e:
            logger.error(f"Error analyzing flipping opportunities: {e}")
            return []
    
    def find_multi_step_flips(self, currencies, currency_values):
        """Find multi-step flipping opportunities"""
        multi_step_opportunities = []
        
        try:
            # Create a list of high-volume currencies to consider for multi-step flips
            high_volume_currencies = [c for c in currencies if c.get('trade_volume', 0) > 50]
            
            # For each high-volume currency, find potential paths
            for start_currency in high_volume_currencies[:10]:  # Limit to top 10 to avoid excessive computation
                start_name = start_currency.get('name')
                start_value = start_currency.get('chaos_value', 0)
                
                if start_value < 5:  # Skip low-value currencies
                    continue
                
                # Find potential second step currencies
                for mid_currency in high_volume_currencies:
                    mid_name = mid_currency.get('name')
                    mid_value = mid_currency.get('chaos_value', 0)
                    
                    if mid_name == start_name or mid_value < 5:
                        continue
                    
                    # Find potential third step currencies
                    for end_currency in high_volume_currencies:
                        end_name = end_currency.get('name')
                        end_value = end_currency.get('chaos_value', 0)
                        
                        if end_name == start_name or end_name == mid_name or end_value < 5:
                            continue
                        
                        # Calculate potential profit
                        # Assume 1% loss per trade due to spread
                        step1_value = start_value * 0.99
                        step2_value = (step1_value / mid_value) * mid_value * 0.99
                        step3_value = (step2_value / end_value) * end_value * 0.99
                        final_value = (step3_value / start_value) * start_value
                        
                        profit = final_value - start_value
                        profit_percent = (profit / start_value) * 100
                        
                        # Only include profitable paths
                        if profit_percent > 2:  # At least 2% profit
                            opportunity = {
                                'type': 'multi-step',
                                'path': f"{start_name} -> {mid_name} -> {end_name} -> {start_name}",
                                'start_currency': start_name,
                                'mid_currency': mid_name,
                                'end_currency': end_name,
                                'profit_percent': profit_percent,
                                'potential_profit': profit,
                                'strategy': f"Convert {start_name} to {mid_name}, then to {end_name}, then back to {start_name}. Expected profit: {profit_percent:.2f}%",
                                'opportunity_score': profit_percent * 2,  # Weight multi-step higher
                                'league': start_currency.get('league', PRIMARY_LEAGUE)
                            }
                            multi_step_opportunities.append(opportunity)
            
            # Sort by profit percent
            multi_step_opportunities.sort(key=lambda x: x.get('profit_percent', 0), reverse=True)
            
            # Limit to top 10 multi-step opportunities
            return multi_step_opportunities[:10]
            
        except Exception as e:
            logger.error(f"Error finding multi-step flips: {e}")
            return []
    
    def analyze_farming_opportunities(self, market_data):
        """Analyze farming opportunities"""
        farming_opportunities = []
        
        try:
            # Get all relevant item types
            scarabs = market_data.get('scarabs', [])
            fragments = market_data.get('fragments', [])
            oils = market_data.get('oils', [])
            div_cards = market_data.get('divination_cards', [])
            
            # Analyze scarab farming opportunities
            scarab_opportunities = self.analyze_scarab_farming(scarabs)
            farming_opportunities.extend(scarab_opportunities)
            
            # Analyze fragment farming opportunities
            fragment_opportunities = self.analyze_fragment_farming(fragments)
            farming_opportunities.extend(fragment_opportunities)
            
            # Analyze oil farming opportunities
            oil_opportunities = self.analyze_oil_farming(oils)
            farming_opportunities.extend(oil_opportunities)
            
            # Analyze divination card farming opportunities
            div_card_opportunities = self.analyze_div_card_farming(div_cards)
            farming_opportunities.extend(div_card_opportunities)
            
            # Sort opportunities by opportunity score
            farming_opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
            
            # Limit to top 20 opportunities
            return farming_opportunities[:20]
            
        except Exception as e:
            logger.error(f"Error analyzing farming opportunities: {e}")
            return []
    
    def analyze_scarab_farming(self, scarabs):
        """Analyze scarab farming opportunities"""
        scarab_opportunities = []
        
        try:
            # Sort scarabs by chaos value
            sorted_scarabs = sorted(scarabs, key=lambda x: x.get('chaos_value', 0), reverse=True)
            
            # Get top valuable scarabs
            top_scarabs = sorted_scarabs[:10]
            
            for scarab in top_scarabs:
                name = scarab.get('name', '')
                chaos_value = scarab.get('chaos_value', 0)
                
                if chaos_value < 10:  # Skip low-value scarabs
                    continue
                
                # Determine scarab type and farming strategy
                scarab_type = name.split(' ')[-1] if ' ' in name else ''
                farming_strategy = self.get_scarab_farming_strategy(scarab_type)
                
                opportunity = {
                    'type': 'scarab',
                    'item': name,
                    'chaos_value': chaos_value,
                    'farming_method': farming_strategy['method'],
                    'locations': farming_strategy['locations'],
                    'strategy': farming_strategy['strategy'],
                    'opportunity_score': chaos_value * 0.8,  # Weight based on value
                    'league': scarab.get('league', PRIMARY_LEAGUE)
                }
                scarab_opportunities.append(opportunity)
            
            return scarab_opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing scarab farming: {e}")
            return []
    
    def get_scarab_farming_strategy(self, scarab_type):
        """Get farming strategy for a specific scarab type"""
        strategies = {
            'Cartography': {
                'method': 'Atlas Passive Tree + Map Farming',
                'locations': ['Maps with Cartography Scarab passives'],
                'strategy': 'Spec into Cartography Scarab nodes on Atlas Passive Tree. Run maps with "Additional Cartographer\'s Strongboxes" sextant. Use Ambush scarabs to increase strongbox quantity.'
            },
            'Reliquary': {
                'method': 'Heist Blueprint Farming',
                'locations': ['Heist Blueprints', 'Smuggler\'s Caches'],
                'strategy': 'Run Heist Blueprints with Unusual Gems or Replicas. Focus on Smuggler\'s Caches in maps. Spec into Heist nodes on Atlas Passive Tree.'
            },
            'Bestiary': {
                'method': 'Einhar Mission Farming',
                'locations': ['Maps with Einhar missions'],
                'strategy': 'Spec into Bestiary nodes on Atlas Passive Tree. Use Einhar master missions on high-tier maps. Use sextants with "Area contains additional Bestiary monsters".'
            },
            'Harbinger': {
                'method': 'Harbinger Farming',
                'locations': ['Maps with Harbinger passives'],
                'strategy': 'Spec into Harbinger nodes on Atlas Passive Tree. Use "Area contains additional Harbingers" sextant. Run maps with Harbinger scarabs.'
            },
            'Legion': {
                'method': 'Legion Farming',
                'locations': ['Maps with Legion passives'],
                'strategy': 'Spec into Legion nodes on Atlas Passive Tree. Use "Area contains additional Legion" sextant. Run maps with Legion scarabs.'
            },
            'Breach': {
                'method': 'Breach Farming',
                'locations': ['Maps with Breach passives'],
                'strategy': 'Spec into Breach nodes on Atlas Passive Tree. Use "Area contains additional Breaches" sextant. Run maps with Breach scarabs.'
            },
            'Expedition': {
                'method': 'Expedition Farming',
                'locations': ['Maps with Expedition passives'],
                'strategy': 'Spec into Expedition nodes on Atlas Passive Tree. Use "Area contains additional Expedition" sextant. Run maps with Expedition scarabs.'
            },
            'Blight': {
                'method': 'Blight Farming',
                'locations': ['Maps with Blight passives'],
                'strategy': 'Spec into Blight nodes on Atlas Passive Tree. Use "Area contains additional Blight" sextant. Run maps with Blight scarabs.'
            },
            'Metamorph': {
                'method': 'Metamorph Farming',
                'locations': ['Maps with Metamorph passives'],
                'strategy': 'Spec into Metamorph nodes on Atlas Passive Tree. Use "Area contains additional Metamorph samples" sextant. Run maps with Metamorph scarabs.'
            },
            'Divination': {
                'method': 'Divination Card Farming',
                'locations': ['Maps with Divination Card passives'],
                'strategy': 'Spec into Divination Card nodes on Atlas Passive Tree. Use "Area contains additional Divination Cards" sextant. Run maps with Divination scarabs.'
            }
        }
        
        # Default strategy if scarab type not found
        default_strategy = {
            'method': 'General Scarab Farming',
            'locations': ['Delirium Maps', 'Blight Maps', 'Legion Encounters'],
            'strategy': 'Run high-tier maps with Delirium Orbs. Focus on Legion, Blight, and Metamorph encounters. Spec into Scarab nodes on Atlas Passive Tree.'
        }
        
        return strategies.get(scarab_type, default_strategy)
    
    def analyze_fragment_farming(self, fragments):
        """Analyze fragment farming opportunities"""
        fragment_opportunities = []
        
        try:
            # Sort fragments by chaos value
            sorted_fragments = sorted(fragments, key=lambda x: x.get('chaos_value', 0), reverse=True)
            
            # Get top valuable fragments
            top_fragments = sorted_fragments[:10]
            
            for fragment in top_fragments:
                name = fragment.get('name', '')
                chaos_value = fragment.get('chaos_value', 0)
                
                if chaos_value < 15:  # Skip low-value fragments
                    continue
                
                # Determine fragment type and farming strategy
                farming_strategy = self.get_fragment_farming_strategy(name)
                
                opportunity = {
                    'type': 'fragment',
                    'item': name,
                    'chaos_value': chaos_value,
                    'farming_method': farming_strategy['method'],
                    'locations': farming_strategy['locations'],
                    'strategy': farming_strategy['strategy'],
                    'opportunity_score': chaos_value * 0.9,  # Weight based on value
                    'league': fragment.get('league', PRIMARY_LEAGUE)
                }
                fragment_opportunities.append(opportunity)
            
            return fragment_opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing fragment farming: {e}")
            return []
    
    def get_fragment_farming_strategy(self, fragment_name):
        """Get farming strategy for a specific fragment"""
        strategies = {
            'Maven\'s Invitation': {
                'method': 'Maven Witness Farming',
                'locations': ['Maps witnessed by Maven'],
                'strategy': 'Run maps with Maven witness active. Focus on completing 10 different maps in a region to spawn Maven\'s Invitation. Spec into Maven nodes on Atlas Passive Tree.'
            },
            'Forgotten': {
                'method': 'Shaper Guardian Maps',
                'locations': ['Shaper Guardian Maps'],
                'strategy': 'Run Shaper Guardian Maps (Chimera, Hydra, Minotaur, Phoenix). Use "Area contains additional Shaper Guardian" sextant. Spec into Shaper nodes on Atlas Passive Tree.'
            },
            'Formed': {
                'method': 'Elder Guardian Maps',
                'locations': ['Elder Guardian Maps'],
                'strategy': 'Run Elder Guardian Maps. Use "Area contains additional Elder Guardian" sextant. Spec into Elder nodes on Atlas Passive Tree.'
            },
            'Twisted': {
                'method': 'Breachlord Domains',
                'locations': ['Breach Domains'],
                'strategy': 'Run Breach Domains (Chayula, Uul-Netol, Tul, Esh, Xoph). Spec into Breach nodes on Atlas Passive Tree. Use Breach scarabs.'
            },
            'Mortal': {
                'method': 'Atziri Farming',
                'locations': ['Vaal Side Areas', 'Sacrifice Fragments'],
                'strategy': 'Run Vaal Side Areas in maps. Use Sacrifice fragments in map device to spawn Vaal areas. Run normal Atziri to get Mortal fragments.'
            },
            'Sacrifice': {
                'method': 'Vaal Side Area Farming',
                'locations': ['Vaal Side Areas'],
                'strategy': 'Run maps with "Area contains Vaal Side Areas" sextant. Use Vaal Fragments in map device to spawn additional Vaal Side Areas.'
            },
            'Simulacrum': {
                'method': 'Delirium Mirror Farming',
                'locations': ['Maps with Delirium passives'],
                'strategy': 'Spec into Delirium nodes on Atlas Passive Tree. Use Delirium Orbs on maps. Run maps with Delirium scarabs.'
            },
            'Timeless': {
                'method': 'Legion Farming',
                'locations': ['Maps with Legion passives'],
                'strategy': 'Spec into Legion nodes on Atlas Passive Tree. Use "Area contains additional Legion" sextant. Run maps with Legion scarabs.'
            }
        }
        
        # Check for partial matches
        for key, strategy in strategies.items():
            if key in fragment_name:
                return strategy
        
        # Default strategy if fragment name not found
        default_strategy = {
            'method': 'General Fragment Farming',
            'locations': ['High-tier Maps', 'Boss Encounters'],
            'strategy': 'Run high-tier maps with boss-focused Atlas Passive Tree. Focus on completing Maven invitations and endgame boss encounters.'
        }
        
        return default_strategy
    
    def analyze_oil_farming(self, oils):
        """Analyze oil farming opportunities"""
        oil_opportunities = []
        
        try:
            # Sort oils by chaos value
            sorted_oils = sorted(oils, key=lambda x: x.get('chaos_value', 0), reverse=True)
            
            # Get top valuable oils
            top_oils = sorted_oils[:5]
            
            for oil in top_oils:
                name = oil.get('name', '')
                chaos_value = oil.get('chaos_value', 0)
                
                if chaos_value < 10:  # Skip low-value oils
                    continue
                
                opportunity = {
                    'type': 'oil',
                    'item': name,
                    'chaos_value': chaos_value,
                    'farming_method': 'Blight Farming',
                    'locations': ['Blight Maps', 'Blight Encounters'],
                    'strategy': 'Run Blight Maps with at least 3 Teal Oils applied. Spec into Blight nodes on Atlas Passive Tree. Use Blight scarabs on high-tier maps. Focus on completing Blight Ravaged Maps for higher tier oil drops.',
                    'opportunity_score': chaos_value * 0.7,  # Weight based on value
                    'league': oil.get('league', PRIMARY_LEAGUE)
                }
                oil_opportunities.append(opportunity)
            
            return oil_opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing oil farming: {e}")
            return []
    
    def analyze_div_card_farming(self, div_cards):
        """Analyze divination card farming opportunities"""
        div_card_opportunities = []
        
        try:
            # Sort divination cards by chaos value
            sorted_div_cards = sorted(div_cards, key=lambda x: x.get('chaos_value', 0), reverse=True)
            
            # Get top valuable divination cards
            top_div_cards = sorted_div_cards[:10]
            
            for div_card in top_div_cards:
                name = div_card.get('name', '')
                chaos_value = div_card.get('chaos_value', 0)
                
                if chaos_value < 50:  # Skip low-value divination cards
                    continue
                
                # Get farming locations for the divination card
                farming_locations = self.get_div_card_farming_locations(name)
                
                opportunity = {
                    'type': 'divination_card',
                    'item': name,
                    'chaos_value': chaos_value,
                    'farming_method': 'Targeted Map Farming',
                    'locations': farming_locations['maps'],
                    'strategy': farming_locations['strategy'],
                    'opportunity_score': chaos_value * 0.6,  # Weight based on value
                    'league': div_card.get('league', PRIMARY_LEAGUE)
                }
                div_card_opportunities.append(opportunity)
            
            return div_card_opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing divination card farming: {e}")
            return []
    
    def get_div_card_farming_locations(self, card_name):
        """Get farming locations for a specific divination card"""
        locations = {
            'The Doctor': {
                'maps': ['Burial Chambers', 'Spider Forest'],
                'strategy': 'Farm Burial Chambers or Spider Forest maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Nurse': {
                'maps': ['Tower Map'],
                'strategy': 'Farm Tower maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Fiend': {
                'maps': ['Putrid Cloister'],
                'strategy': 'Farm Putrid Cloister unique maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree.'
            },
            'House of Mirrors': {
                'maps': ['The Mirror of Kalandra (Reflection of Kalandra)'],
                'strategy': 'Farm Reflection of Kalandra endgame content. This card is extremely rare and not target-farmable in a specific map.'
            },
            'The Demon': {
                'maps': ['Uber Maven', 'Uber Elder'],
                'strategy': 'Farm Uber Maven and Uber Elder encounters. Spec into Maven and Elder nodes on Atlas Passive Tree.'
            },
            'The Immortal': {
                'maps': ['Hall of Grandmasters'],
                'strategy': 'Farm Hall of Grandmasters unique map. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree.'
            },
            'The Iron Bard': {
                'maps': ['Conservatory Map'],
                'strategy': 'Farm Conservatory maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Apothecary': {
                'maps': ['Crimson Temple'],
                'strategy': 'Farm Crimson Temple maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'Unrequited Love': {
                'maps': ['Terrace Map'],
                'strategy': 'Farm Terrace maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Enlightened': {
                'maps': ['Scriptorium Map'],
                'strategy': 'Farm Scriptorium maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Sephirot': {
                'maps': ['Excavation Map'],
                'strategy': 'Farm Excavation maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'Seven Years Bad Luck': {
                'maps': ['Laboratory Map'],
                'strategy': 'Farm Laboratory maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Hoarder': {
                'maps': ['Arcade Map', 'Burial Chambers Map'],
                'strategy': 'Farm Arcade or Burial Chambers maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'The Saint\'s Treasure': {
                'maps': ['Arcade Map'],
                'strategy': 'Farm Arcade maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            },
            'Abandoned Wealth': {
                'maps': ['Arsenal Map', 'Atoll Map'],
                'strategy': 'Farm Arsenal or Atoll maps. Use Divination scarabs and spec into Divination Card nodes on Atlas Passive Tree. Apply "Area contains additional Divination Cards" sextant.'
            }
        }
        
        # Check for exact matches
        if card_name in locations:
            return locations[card_name]
        
        # Default locations if card name not found
        default_locations = {
            'maps': ['Any Map with Divination Card focus'],
            'strategy': 'Spec into Divination Card nodes on Atlas Passive Tree. Use Divination scarabs on high-tier maps. Apply "Area contains additional Divination Cards" sextant. Check PoE Wiki for specific drop locations for this card.'
        }
        
        return default_locations
    
    def analyze_crafting_opportunities(self, market_data):
        """Analyze crafting opportunities"""
        crafting_opportunities = []
        
        try:
            # Define some common crafting methods
            crafting_methods = [
                {
                    'name': 'Cluster Jewel Crafting',
                    'description': 'Crafting high-demand cluster jewels with specific notables',
                    'materials': ['Large Cluster Jewel (8 passives)', 'Chaos Orbs', 'Alteration Orbs', 'Regal Orbs'],
                    'strategy': 'Buy 8-passive Large Cluster Jewels with good bases (e.g., Critical, Elemental Damage). Use Alteration+Regal or Chaos spam to hit valuable notable combinations. Focus on meta builds for best returns.',
                    'estimated_cost': 150,
                    'estimated_return': 300,
                    'opportunity_score': 85
                },
                {
                    'name': 'Essence Crafting',
                    'description': 'Using high-tier essences to craft meta items',
                    'materials': ['Deafening Essence of Dread/Anger/Hatred/Wrath', 'Influenced item bases'],
                    'strategy': 'Buy influenced item bases (e.g., Fingerless Silk Gloves, Two-Toned Boots). Apply Deafening Essences to guarantee one mod and hope for good influenced mods. Focus on meta builds for best returns.',
                    'estimated_cost': 200,
                    'estimated_return': 350,
                    'opportunity_score': 75
                },
                {
                    'name': 'Fossil Crafting',
                    'description': 'Using specific fossil combinations to target valuable mod pools',
                    'materials': ['Pristine Fossils', 'Jagged Fossils', 'Dense Fossils', 'Resonators'],
                    'strategy': 'Buy good item bases (e.g., Astral Plate, Vaal Regalia). Use fossil combinations to target specific mod pools. For example, Pristine+Jagged+Dense for physical damage reduction and life on armor.',
                    'estimated_cost': 250,
                    'estimated_return': 500,
                    'opportunity_score': 90
                },
                {
                    'name': 'Harvest Reforge Crafting',
                    'description': 'Using Harvest reforge crafts to target specific mod types',
                    'materials': ['Base items', 'Harvest crafts (reforge with X)'],
                    'strategy': 'Buy good item bases. Use Harvest reforge crafts to target specific mod types (e.g., "Reforge with Physical modifiers" on weapons). Combine with metamods for more deterministic results.',
                    'estimated_cost': 300,
                    'estimated_return': 600,
                    'opportunity_score': 95
                },
                {
                    'name': 'Eldritch Currency Crafting',
                    'description': 'Using Eldritch currency to craft powerful implicit modifiers',
                    'materials': ['Eldritch Chaos Orbs', 'Eldritch Exalted Orbs', 'Gloves/Boots/Helmets/Body Armour'],
                    'strategy': 'Buy item bases with good explicit modifiers. Apply Eldritch currency to add powerful implicit modifiers. Focus on meta combinations like spell suppression, elemental damage, or life regeneration.',
                    'estimated_cost': 400,
                    'estimated_return': 700,
                    'opportunity_score': 80
                },
                {
                    'name': 'Fractured Item Crafting',
                    'description': 'Crafting on items with valuable fractured mods',
                    'materials': ['Items with good fractured mods', 'Essences', 'Fossils'],
                    'strategy': 'Buy items with valuable fractured mods (e.g., T1 life, high physical damage). Craft using essences or fossils to add complementary mods. The fractured mod cannot be changed, providing a guaranteed high-tier mod.',
                    'estimated_cost': 500,
                    'estimated_return': 1000,
                    'opportunity_score': 100
                },
                {
                    'name': 'Veiled Chaos Orb Crafting',
                    'description': 'Using Veiled Chaos Orbs to get powerful veiled modifiers',
                    'materials': ['Veiled Chaos Orbs', 'Influenced item bases'],
                    'strategy': 'Buy influenced item bases. Apply Veiled Chaos Orbs to reroll the item with a guaranteed veiled modifier. Unveil to select powerful mods like "Trigger a Socketed Spell when you Use a Skill".',
                    'estimated_cost': 150,
                    'estimated_return': 300,
                    'opportunity_score': 70
                },
                {
                    'name': 'Awakener Orb Crafting',
                    'description': 'Combining two influenced items to create a double-influenced item',
                    'materials': ['Awakener\'s Orb', 'Two influenced items with desired mods'],
                    'strategy': 'Buy two influenced items with desired mods (e.g., item with T1 life and item with explode mod). Use Awakener\'s Orb to destroy the first item and transfer its influence mod to the second item. Results in a double-influenced item with both mods.',
                    'estimated_cost': 1000,
                    'estimated_return': 2000,
                    'opportunity_score': 95
                },
                {
                    'name': 'Recombinator Crafting',
                    'description': 'Using recombinators to merge mods from two items',
                    'materials': ['Recombinators', 'Two well-rolled items'],
                    'strategy': 'Buy or craft two items with complementary mods. Use recombinators to merge them, with a chance to get both sets of mods on a single item. Can create otherwise impossible mod combinations.',
                    'estimated_cost': 300,
                    'estimated_return': 800,
                    'opportunity_score': 85
                },
                {
                    'name': 'Meta-mod Crafting',
                    'description': 'Using "Prefixes/Suffixes Cannot Be Changed" with other crafting methods',
                    'materials': ['Exalted Orbs', 'Divine Orbs', 'Crafting bench (2 ex for metamod)'],
                    'strategy': 'Craft an item with good prefixes or suffixes. Apply "Prefixes/Suffixes Cannot Be Changed" metamod. Use Harvest reforge, Veiled Chaos Orbs, or other methods to safely modify the other half of the item without risking the good mods.',
                    'estimated_cost': 800,
                    'estimated_return': 1500,
                    'opportunity_score': 90
                }
            ]
            
            # Add league-specific information
            for method in crafting_methods:
                method['league'] = PRIMARY_LEAGUE
                crafting_opportunities.append(method)
            
            # Sort by opportunity score
            crafting_opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
            
            return crafting_opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing crafting opportunities: {e}")
            return []
    
    def analyze_investment_opportunities(self, market_data):
        """Analyze investment opportunities"""
        investment_opportunities = []
        
        try:
            # Get all currencies and items
            currencies = market_data.get('currencies', [])
            fragments = market_data.get('fragments', [])
            scarabs = market_data.get('scarabs', [])
            oils = market_data.get('oils', [])
            
            # Combine all items
            all_items = currencies + fragments + scarabs + oils
            
            # Filter items with price history data
            items_with_history = [item for item in all_items if 'price_change' in item or 'receive_change' in item]
            
            # Calculate investment rating for each item
            for item in items_with_history:
                name = item.get('name', '')
                chaos_value = item.get('chaos_value', 0)
                
                # Get price change (use receive_change for currencies, price_change for items)
                price_change = item.get('receive_change', item.get('price_change', 0))
                
                # Skip items with no price data
                if chaos_value <= 0:
                    continue
                
                # Determine item type
                if item in currencies:
                    item_type = 'Currency'
                elif item in fragments:
                    item_type = 'Fragment'
                elif item in scarabs:
                    item_type = 'Scarab'
                elif item in oils:
                    item_type = 'Oil'
                else:
                    item_type = 'Other'
                
                # Calculate investment rating
                investment_rating = self.calculate_investment_rating(chaos_value, price_change, item.get('trade_volume', 0))
                
                # Only include items with good investment potential
                if investment_rating > 60:
                    # Determine investment strategy based on price trend
                    if price_change > 10:
                        strategy = f"Short-term investment: {name} is rising in value (+{price_change}%). Buy now and sell within 1-3 days for quick profit. Current price: {chaos_value} chaos."
                    elif price_change < -10:
                        strategy = f"Long-term investment: {name} is currently undervalued ({price_change}%). Buy now while price is low and hold for 1-2 weeks until price recovers. Current price: {chaos_value} chaos."
                    else:
                        strategy = f"Stable investment: {name} has consistent value with moderate volatility. Good for bulk buying and selling when small price fluctuations occur. Current price: {chaos_value} chaos."
                    
                    opportunity = {
                        'type': item_type,
                        'item': name,
                        'chaos_value': chaos_value,
                        'price_change': price_change,
                        'investment_rating': investment_rating,
                        'strategy': strategy,
                        'league': item.get('league', PRIMARY_LEAGUE)
                    }
                    investment_opportunities.append(opportunity)
            
            # Sort by investment rating
            investment_opportunities.sort(key=lambda x: x.get('investment_rating', 0), reverse=True)
            
            # Limit to top 20 opportunities
            return investment_opportunities[:20]
            
        except Exception as e:
            logger.error(f"Error analyzing investment opportunities: {e}")
            return []
    
    def calculate_investment_rating(self, price, price_change, volume):
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
    
    def calculate_opportunity_score(self, profit_ratio, volatility, volume):
        """Calculate an opportunity score based on profit ratio, volatility, and volume"""
        # Higher profit ratio, moderate volatility, and higher volume
        # result in a better opportunity score
        
        # Normalize values
        profit_factor = min(1.0, profit_ratio)  # Cap at 1.0
        volatility_factor = min(1.0, volatility * 5)  # Scale up, cap at 1.0
        volume_factor = min(1.0, volume / 200)  # Higher volume is better
        
        # Calculate weighted score (0-100)
        score = (profit_factor * 0.6 + volatility_factor * 0.2 + volume_factor * 0.2) * 100
        
        return round(score, 1)
