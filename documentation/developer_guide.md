# Path of Exile Economy Analysis Tool - Developer Guide

## Architecture Overview

The PoE Economy Analysis Tool is built with a modular architecture consisting of the following components:

1. **Data Collection Module** (`data_collector.py`): Responsible for fetching real-time data from poe.ninja API
2. **Data Integration Module** (`data_integration.py`): Integrates data from different leagues and sources
3. **Analysis Engine** (`analysis_engine.py`): Analyzes market data to identify profitable opportunities
4. **Web Interface** (`app.py`, templates, static files): Presents data and opportunities to users
5. **Configuration** (`config.py`): Manages settings and platform compatibility

## Component Details

### Data Collection Module

The `DataCollector` class handles fetching data from poe.ninja for various item types:
- Currencies (Divine Orb, Exalted Orb, etc.)
- Fragments (Scarabs, Splinters, etc.)
- Oils (Golden Oil, Silver Oil, etc.)
- Scarabs (All types and tiers)
- Incubators
- Artifacts
- Divination Cards

Key methods:
- `collect_all_data(league)`: Collects all data types for a specific league
- `collect_currency_data(league)`: Collects currency data
- `collect_item_data(league, item_type)`: Collects data for specific item types

### Data Integration Module

The `DataIntegration` class combines data from different leagues and adds additional analysis:
- Integrates primary league (Phrecia) with historical league (Settlers)
- Calculates price trends and volatility
- Adds reference data for farming locations and strategies

Key methods:
- `integrate_data(market_data)`: Main integration method
- `integrate_currencies(primary_currencies, historical_currencies)`: Integrates currency data
- `integrate_items(primary_items, historical_items)`: Integrates item data

### Analysis Engine

The `AnalysisEngine` class identifies profitable opportunities in four categories:
- Flipping: Currency trading opportunities
- Farming: Profitable items to target farm
- Crafting: Profitable crafting strategies
- Investment: Long-term investment opportunities

Key methods:
- `analyze_all_opportunities(integrated_data)`: Main analysis method
- `analyze_flipping_opportunities(integrated_data)`: Analyzes flipping opportunities
- `analyze_farming_opportunities(integrated_data)`: Analyzes farming opportunities
- `analyze_crafting_opportunities(integrated_data)`: Analyzes crafting opportunities
- `analyze_investment_opportunities(integrated_data)`: Analyzes investment opportunities

### Web Interface

The web interface is built with Flask and includes:
- Main dashboard (`index.html`)
- JavaScript for interactive charts and tables (`main.js`)
- CSS for styling (`style.css`)

Key endpoints:
- `/`: Main dashboard
- `/api/opportunities`: Get current profit opportunities
- `/api/update`: Trigger manual data update
- `/api/leagues`: Get available leagues
- `/api/status`: Get current status
- `/api/currency_data`: Get currency data for charts

## Extending the Tool

### Adding New Item Types

To add a new item type to track:

1. Add the new item type to `ITEM_TYPES` in `config.py`:
```python
ITEM_TYPES = {
    # Existing types...
    'NewItemType': f'{POE_NINJA_ITEM_URL}?league={{league}}&type=NewItemType',
}
```

2. Update the `collect_all_data` method in `data_collector.py` to include the new item type
3. Update the `integrate_data` method in `data_integration.py` to process the new item type
4. Add analysis for the new item type in `analysis_engine.py`

### Adding New Analysis Methods

To add a new analysis method:

1. Create a new method in `analysis_engine.py`:
```python
def analyze_new_opportunities(self, integrated_data):
    # Analysis logic here
    return opportunities
```

2. Update the `analyze_all_opportunities` method to include your new analysis
3. Update the web interface to display the new opportunities

### Customizing the Web Interface

To customize the web interface:

1. Modify `templates/index.html` to add new UI elements
2. Update `static/js/main.js` to handle new data and interactions
3. Customize `static/css/style.css` to change the appearance

## Platform Compatibility

The tool is designed to work on both Windows and Unix/Linux systems:

- Path handling is managed through the `get_platform_path` function in `config.py`
- Directory creation is handled by `ensure_dir_exists` function
- All file operations use platform-agnostic path joining

When adding new file operations, always use:
```python
from config import get_platform_path
file_path = get_platform_path('/path/to/file')
```

## Performance Considerations

- The tool updates data every 15 minutes by default (configurable in `config.py`)
- Data is cached to minimize API requests
- Background updates run in a separate thread to avoid blocking the UI
- Consider implementing pagination for large datasets

## Testing

To test the tool:

1. Run unit tests for individual components:
```
python -m unittest tests/test_data_collector.py
python -m unittest tests/test_analysis_engine.py
```

2. Test the full application:
```
python app.py
```

3. Verify data accuracy by comparing with poe.ninja website

## Deployment

For production deployment:

1. Consider using a production WSGI server like Gunicorn:
```
pip install gunicorn
gunicorn -w 4 app:app
```

2. Set up a reverse proxy with Nginx or Apache
3. Configure proper logging and monitoring
4. Consider containerization with Docker for easier deployment

## Troubleshooting

Common issues and solutions:

- **API rate limiting**: Implement exponential backoff for API requests
- **Memory usage**: Optimize data structures and implement pagination
- **Slow analysis**: Profile and optimize analysis algorithms
- **Path issues**: Ensure all file operations use `get_platform_path`
