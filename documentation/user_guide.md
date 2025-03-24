# Path of Exile Economy Analysis Tool - User Guide

## Overview

The Path of Exile Economy Analysis Tool is a comprehensive application designed to help players maximize their in-game profits through data-driven strategies. The tool analyzes real-time market data from poe.ninja to identify profitable opportunities in four key areas:

1. **Currency Flipping**: Identifies profitable currency trading opportunities, including both single-step and multi-step conversion paths
2. **Farming Strategies**: Recommends the most profitable items and mechanics to target farm based on current market values
3. **Crafting Methods**: Suggests profitable crafting strategies with detailed cost analysis and instructions
4. **Investment Opportunities**: Analyzes market trends to recommend items for long-term investment

## Installation

### Windows

1. Download and extract the PoE_Economy_Analysis_Tool.zip file
2. Ensure you have Python 3.8 or newer installed
   - Download from [python.org](https://www.python.org/downloads/) if needed
3. Open Command Prompt and navigate to the extracted directory:
   ```
   cd path\to\extracted\folder
   ```
4. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Linux/Mac

1. Download and extract the PoE_Economy_Analysis_Tool.zip file
2. Ensure you have Python 3.8 or newer installed
3. Open Terminal and navigate to the extracted directory:
   ```
   cd path/to/extracted/folder
   ```
4. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Using the Tool

### Dashboard Overview

The main dashboard displays:

- **Market Overview**: Charts showing top currency values and price trends
- **Opportunity Tabs**: Detailed tables for Flipping, Farming, Crafting, and Investment opportunities
- **League Phase Strategy Guide**: Recommendations for different phases of the league

### Currency Flipping

The Flipping tab shows profitable currency trading opportunities:

- **Single Currency**: Direct buy/sell opportunities for individual currencies
- **Multi-Step Path**: Complex trading paths that yield higher profits through multiple conversions
- **Opportunity Score**: Higher scores indicate more profitable opportunities
- **Strategy**: Detailed instructions on how to execute the flipping strategy

### Farming Strategies

The Farming tab recommends profitable items and mechanics to target:

- **Scarab Farming**: Strategies for farming specific scarabs, including map selection and Atlas passives
- **Fragment Farming**: Methods for efficiently farming valuable fragments
- **League Mechanics**: Profitable league mechanics to focus on
- **Strategy**: Detailed explanations of how to execute each farming method

### Crafting Methods

The Crafting tab suggests profitable crafting strategies:

- **Method**: The type of crafting method (e.g., Cluster Jewel Crafting, Meta Mod Crafting)
- **Description**: Overview of the crafting process
- **Opportunity Score**: Higher scores indicate more profitable opportunities
- **Strategy**: Step-by-step instructions for the crafting process, including materials needed and expected profits

### Investment Opportunities

The Investment tab recommends items for long-term investment:

- **Type**: Category of investment (Currency, Scarab, Fragment)
- **Item**: Specific item to invest in
- **Current Value**: Current market value in chaos orbs
- **Price Change**: Recent price trend percentage
- **Investment Rating**: Higher ratings indicate better investment opportunities
- **Strategy**: Detailed investment strategy, including when to buy and sell

## Data Updates

The tool automatically updates data from poe.ninja every 15 minutes. You can see the last update time and next scheduled update in the header of the application.

## League Phase Strategies

The tool provides different recommendations based on the current phase of the league:

- **Early League (First Week)**:
  - Focus on reaching maps quickly
  - Sell leveling uniques and early mapping gear
  - Invest in basic currencies that will rise in value
  - Target farm league mechanics with low entry cost
  - Sell scarabs and fragments rather than using them

- **Mid League (2-4 Weeks)**:
  - Begin investing in high-tier scarabs and fragments
  - Start crafting high-demand items
  - Flip currencies with high volatility
  - Target farm endgame bosses and content
  - Invest in items needed for popular builds

- **Late League (1+ Month)**:
  - Liquidate investments before market crashes
  - Focus on high-end crafting for min-maxers
  - Invest in standard-relevant items
  - Target farm ultra-endgame content
  - Begin preparing strategies for next league

## Troubleshooting

If you encounter any issues:

1. **Data not loading**: Check your internet connection and ensure poe.ninja is accessible
2. **Application not starting**: Verify that all dependencies are installed correctly
3. **Incorrect prices**: The tool may need to complete a data update cycle; wait for the next automatic update or trigger a manual update

For additional help, refer to the developer documentation or contact the developer.
