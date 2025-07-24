# Stamp Card Manager

A GUI application for managing digital stamp cards with automatic coupon assignment.

## Features

- **Visual Stamp Card Display**: Interactive donut emoji stamps (🍩) showing progress
- **Real-time Updates**: Fetch and update stamp card data via API
- **Automatic Rewards**: Auto-assigns coupons when cards are completed (4/4 stamps)
- **Progress Tracking**: Tracks cards completed and rewards earned
- **Modern UI**: Built with CustomTkinter for a sleek dark theme interface

## How It Works

- **1-3 Stamps**: Updates stamp count normally
- **4/4 Stamps**: Automatically assigns reward coupon and resets card to 0/4
- **Card Completion**: Increments cards filled and rewards earned counters

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Enter your Polygon API credentials
2. Input a Member ID
3. Click "Fetch Stamp Card" to load current data
4. Update stamp count (0-4) and click "Update Stamp Card"
5. The system will automatically handle coupon assignment for completed cards

## API Integration

Connects to the RedCat Cloud API for:
- Authentication
- Stamp card data retrieval
- Stamp card updates
- Coupon assignment

## Default Settings

- **Reward Coupon ID**: 230 ("5th Visit Freebie")
- **Stamps per Card**: 4
- **Theme**: Dark mode with blue accents

## Requirements

- Python 3.7+
- CustomTkinter 5.2.0+
- Requests 2.31.0+