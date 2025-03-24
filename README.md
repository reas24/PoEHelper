# Path of Exile Economy Analysis Tool

A comprehensive tool for analyzing Path of Exile's economy and identifying profitable opportunities based on real-time market data from poe.ninja.

## Features

- **Real-time Data Collection**: Automatically fetches current market data from poe.ninja for all relevant currency types, fragments, oils, scarabs, and more
- **Multi-League Analysis**: Compares data between Phrecia (current) and Settlers (historical) leagues
- **Profit Opportunity Detection**:
  - **Currency Flipping**: Identifies both single-step and multi-step currency trading opportunities
  - **Farming Strategies**: Recommends the most profitable items to target farm with detailed explanations
  - **Crafting Methods**: Suggests profitable crafting strategies with step-by-step instructions
  - **Investment Opportunities**: Analyzes market trends to recommend items for long-term investment
- **Interactive Web Interface**: User-friendly dashboard with sortable tables and visual charts
- **Automatic Updates**: Refreshes data every 15 minutes to provide the most current recommendations
- **Cross-Platform Compatibility**: Works on both Windows and Linux/Mac systems

## Installation

### Requirements

- Python 3.8 or newer
- Internet connection to access poe.ninja API

### Windows Installation

1. Download and extract the PoE_Economy_Analysis_Tool.zip file
2. Open Command Prompt and navigate to the extracted directory:
   ```
   cd path\to\extracted\folder
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Linux/Mac Installation

1. Download and extract the PoE_Economy_Analysis_Tool.zip file
2. Open Terminal and navigate to the extracted directory:
   ```
   cd path/to/extracted/folder
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Quick Start

1. After installation, run the application and open the web interface
2. The dashboard will automatically load with the latest data
3. Navigate between the different tabs to explore various profit opportunities:
   - **Flipping**: Currency trading opportunities
   - **Farming**: Profitable items to target farm
   - **Crafting**: Profitable crafting strategies
   - **Investment**: Long-term investment opportunities
4. Use the sortable tables to find the most profitable opportunities
5. Follow the detailed strategies provided for each opportunity

## Documentation

For more detailed information, refer to:

- [User Guide](documentation/user_guide.md): Comprehensive guide for using the tool
- [Developer Guide](documentation/developer_guide.md): Technical documentation for extending or modifying the tool
- [Installation Guide](documentation/installation_guide.md): Detailed installation instructions

## Data Sources

This tool uses data from [poe.ninja](https://poe.ninja), which provides real-time market data for Path of Exile. The data is automatically updated every 15 minutes to ensure accuracy.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [poe.ninja](https://poe.ninja) for providing the market data API
- [Path of Exile](https://www.pathofexile.com) and Grinding Gear Games for creating an amazing game with a complex economy
- All contributors and testers who helped improve this tool
