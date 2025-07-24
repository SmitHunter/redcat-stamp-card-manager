# Stamp Card Manager (SCM)

A configurable GUI application for managing digital stamp cards with automatic coupon assignment. Supports any API-compatible loyalty system.

## Features

- **Fully Configurable**: Customize API endpoints, stamps per card, reward coupons, and UI elements
- **Visual Stamp Card Display**: Interactive emoji stamps showing progress (customizable emojis)
- **Dynamic Layout**: Automatically adjusts to any number of stamps per card
- **Real-time Updates**: Fetch and update stamp card data via API
- **Automatic Rewards**: Auto-assigns coupons when cards are completed
- **Progress Tracking**: Tracks cards completed and rewards earned
- **Modern UI**: Built with CustomTkinter for a sleek dark theme interface
- **Multi-Business Support**: Easy configuration for different businesses and loyalty systems

## How It Works

- **Partial Stamps**: Updates stamp count normally
- **Full Card**: Automatically assigns reward coupon and resets card to 0
- **Card Completion**: Increments cards filled and rewards earned counters
- **Configurable**: All settings (stamps per card, coupon IDs, etc.) are customizable

## Configuration

Before using SCM, you need to configure it for your business by editing `config.json`:

```json
{
  "api": {
    "base_url": "https://your-api-url.com/api/v1",
    "auth_type": "U"
  },
  "business": {
    "name": "Your Business Name",
    "stamps_per_card": 10,
    "default_coupon_id": 123,
    "default_coupon_name": "Free Coffee"
  },
  "ui": {
    "stamp_emoji": "☕",
    "empty_slot_emoji": "⭕"
  }
}
```

### Configuration Options

#### API Settings
- `base_url`: Your loyalty system's API endpoint
- `auth_type`: Authentication type (usually "U" for username/password)

#### Business Settings
- `name`: Your business name (displayed in title bar)
- `stamps_per_card`: Number of stamps needed to complete a card (any number)
- `default_coupon_id`: Default reward coupon ID to assign when cards are completed
- `default_coupon_name`: Display name for the default coupon

#### UI Settings
- `stamp_emoji`: Emoji used for filled stamps (e.g., ☕ for coffee, 🍩 for donuts, ⭐ for stars)
- `empty_slot_emoji`: Emoji used for empty stamp slots

## Installation

1. Clone this repository
2. Configure your settings in `config.json`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application to see your current configuration
2. Enter your API credentials
3. Input a Member ID
4. Click "Fetch Stamp Card" to load current data
5. Update stamp count and click "Update Stamp Card"
6. The system will automatically handle coupon assignment for completed cards

## API Integration

Compatible with RedCat Cloud API and similar loyalty system APIs:
- Authentication via username/password
- Stamp card data retrieval and updates
- Automatic coupon assignment
- Configurable endpoints and authentication methods

## Example Configurations

### Coffee Shop (10-stamp cards)
```json
{
  "business": {
    "name": "Downtown Coffee",
    "stamps_per_card": 10,
    "default_coupon_id": 101,
    "default_coupon_name": "Free Coffee"
  },
  "ui": {
    "stamp_emoji": "☕",
    "empty_slot_emoji": "⭕"
  }
}
```

### Restaurant (5-stamp cards)
```json
{
  "business": {
    "name": "Mario's Pizza",
    "stamps_per_card": 5,
    "default_coupon_id": 205,
    "default_coupon_name": "Free Slice"
  },
  "ui": {
    "stamp_emoji": "🍕",
    "empty_slot_emoji": "⭕"
  }
}
```

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller build.spec
```

The executable will be created in the `dist/` folder.

## Requirements

- Python 3.7+
- CustomTkinter 5.2.0+
- Requests 2.31.0+

## Theme

- **Dark Mode Interface**: Sleek dark theme with blue accents
- **Responsive Layout**: Adapts to any number of stamps per card
- **Visual Feedback**: Color-coded status messages and progress indicators