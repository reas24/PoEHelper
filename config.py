import os
import platform
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Current leagues
CURRENT_LEAGUES = ['Phrecia', 'Settlers']
PRIMARY_LEAGUE = 'Phrecia'
HISTORICAL_LEAGUE = 'Settlers'

# Update interval in seconds (15 minutes)
UPDATE_INTERVAL = 15 * 60

# Directory paths - using relative paths for cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CURRENT_DATA_DIR = os.path.join(DATA_DIR, 'current')
HISTORICAL_DATA_DIR = os.path.join(DATA_DIR, 'historical')
REFERENCE_DATA_DIR = os.path.join(DATA_DIR, 'reference')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# File paths
REFERENCE_DATA_FILE = os.path.join(REFERENCE_DATA_DIR, 'reference_data.json')

# API URLs
POE_NINJA_API_BASE = 'https://poe.ninja/api/data'
POE_NINJA_CURRENCY_URL = f'{POE_NINJA_API_BASE}/currencyoverview'
POE_NINJA_ITEM_URL = f'{POE_NINJA_API_BASE}/itemoverview'

# Currency types
CURRENCY_TYPES = ['Currency']
FRAGMENT_TYPES = ['Fragment']

# Item types
OIL_TYPES = ['Oil']
SCARAB_TYPES = ['Scarab']
INCUBATOR_TYPES = ['Incubator']
ARTIFACT_TYPES = ['Artifact']
DIVINATION_CARD_TYPES = ['DivinationCard']

# API URL mappings
CURRENCY_TYPE_URLS = {
    'Currency': f'{POE_NINJA_CURRENCY_URL}?league={{league}}&type=Currency',
    'Fragment': f'{POE_NINJA_CURRENCY_URL}?league={{league}}&type=Fragment',
}

ITEM_TYPE_URLS = {
    'Oil': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=Oil',
    'Scarab': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=Scarab',
    'Incubator': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=Incubator',
    'Artifact': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=Artifact',
    'DivinationCard': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=DivinationCard',
}

# Platform detection
def is_windows():
    """Check if the current platform is Windows"""
    return platform.system() == 'Windows'

def get_platform_path(path):
    """Convert path to platform-specific format"""
    # If path is absolute with forward slashes, convert to platform-specific
    if path.startswith('/'):
        # For Windows, convert to relative path from BASE_DIR
        if is_windows():
            # Extract the relevant part after /home/ubuntu/poe_economy_tool/improved/
            if '/home/ubuntu/poe_economy_tool/improved/' in path:
                rel_path = path.split('/home/ubuntu/poe_economy_tool/improved/')[-1]
                return os.path.join(BASE_DIR, rel_path)
            # Extract the relevant part after /home/ubuntu/poe_economy_tool/
            elif '/home/ubuntu/poe_economy_tool/' in path:
                rel_path = path.split('/home/ubuntu/poe_economy_tool/')[-1]
                return os.path.join(os.path.dirname(BASE_DIR), rel_path)
            # If it's some other absolute path, try to make it relative to current directory
            else:
                return os.path.join(BASE_DIR, os.path.basename(path))
    
    # Use os.path.join to handle path separators correctly
    return os.path.normpath(path)

def ensure_dir_exists(directory):
    """Ensure directory exists, create if it doesn't"""
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")

# Initialize directories
def initialize_directories():
    """Initialize all required directories"""
    directories = [
        DATA_DIR,
        CURRENT_DATA_DIR,
        HISTORICAL_DATA_DIR,
        REFERENCE_DATA_DIR,
        OUTPUT_DIR,
        os.path.join(OUTPUT_DIR, 'data'),
    ]
    
    # Create league-specific directories
    for league in CURRENT_LEAGUES:
        league_dir = os.path.join(CURRENT_DATA_DIR, league.lower())
        directories.append(league_dir)
    
    # Ensure all directories exist
    for directory in directories:
        ensure_dir_exists(directory)

# Initialize directories on import
initialize_directories()
