# Python Trading Algorithm Development for Fundezy Platform

A complete guide for developing Python-based trading algorithms on the Fundezy Trading Platform via API services.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- **Git** installed for cloning the repository
- A **Fundezy Trading Platform** account with API access enabled
- **Command line/terminal** access

## 🚀 Quick Start (6 Steps)

1. **[Clone Repository](#1-clone-repository)**
2. **[Install Python Dependencies](#2-install-dependencies)**
3. **[Setup Credentials](#3-setup-credentials)** 
4. **[Test Connection](#4-test-connection)**
5. **[Run Quick Test](#5-run-quick-test)**
6. **[Build Your Algorithm](#6-build-your-algorithm)**

**🎯 Complete System**: This provides a fully functional trading system with position management, real-time data, live trading capabilities, automatic token refresh, and a ready-to-use algorithm template.

## 🔄 Automatic Token Refresh

**NEW**: The system now includes automatic token refresh functionality to handle the 15-minute token expiration seamlessly:

- ✅ **Automatic refresh**: Tokens are refreshed before they expire (1 minute buffer)
- ✅ **Error recovery**: Automatic retry on authentication errors  
- ✅ **Long-running algorithms**: Run continuously without interruption
- ✅ **No code changes**: Existing algorithms automatically benefit
- ✅ **Thread-safe**: Safe for concurrent operations
- ✅ **Production ready**: Tested with long-running algorithms

### How It Works

The token refresh system operates automatically in three scenarios:

1. **Proactive refresh**: When a token is about to expire (within 1 minute)
2. **401 error response**: When the API returns an authentication error
3. **Manual refresh**: When explicitly called by your code

```python
# Your existing code continues to work without changes
client = FundezyTradingClient()
client.login()

# Long-running algorithm - tokens refresh automatically
while True:
    balance = client.get_balance()  # Token refreshed if needed
    positions = client.get_open_positions()
    # ... your trading logic
    time.sleep(60)
```

### Token Status Monitoring (Optional)

```python
# Check current token status
status = client.get_token_status()
print(f"Token expires in: {status['expires_in_minutes']:.1f} minutes")
print(f"Last refresh: {status['last_refresh']}")

# Manual refresh if needed
if client.refresh_token():
    print("Token refreshed successfully")
```

---

## 1. Clone Repository

First, clone this repository to your local machine:

```bash
# Clone the repository
git clone https://github.com/Fundezy-io/AlgoTradingGuide.git

# Navigate to the project directory
cd AlgoTradingGuide
```

> **💡 Tip**: If you don't have Git installed, download it from [git-scm.com](https://git-scm.com/) or download the repository as a ZIP file from GitHub.

## 2. Install Dependencies

Make sure you're in the project directory, then install the required Python packages:

```bash
# Install required packages
pip install requests pandas numpy

# Or install from requirements file
pip install -r requirements.txt
```

## 3. Setup Credentials

Create a `.env` file in the project root:

```bash
FTP_API_BASE_URL=https://platform.fundezy.io
FTP_EMAIL=your-email@example.com
FTP_PASSWORD=your-password
FTP_BROKER_ID=107
```

> **Note**: All sensitive data is loaded from environment variables - nothing sensitive is committed to git.

## 4. Test Connection

```bash
python test_connection.py
```

This verifies your credentials and platform connectivity.

## 5. Run Quick Test

```bash
python quick_test_bot.py
```

**What it does:**
- Tests BTCUSD trading (24/7 crypto market)
- Opens/closes random positions every 10 seconds
- Validates all trading endpoints in 2 minutes
- Shows real-time P&L and balance changes

**Sample Output:**
```
🚀 Starting Quick Test Bot for BTCUSD
💰 Balance: $199,950.04, Equity: $199,950.04
🎲 Signal: BUY
✅ Opened BUY position for BTCUSD
📊 Open positions: 1
```

## 6. Build Your Algorithm

### Option A: Use the Template (Recommended)

```bash
# Copy the template to create your own algorithm
cp algorithm_template.py my_strategy.py
python my_strategy.py
```

**The template includes:**
- ✅ Complete API connection setup
- ✅ Authentication and account management
- ✅ Market data retrieval and analysis
- ✅ Position opening, closing, and management
- ✅ Example moving average strategy
- ✅ Comprehensive error handling
- ✅ Customizable parameters and risk management

### Option B: Start from Scratch

Use the [API Client Reference](#-api-client-reference) below to build your own algorithm.

---

## 📁 Project Files

### 🔧 Core Components
- **`fundezy_trading_client.py`** - Complete API client library
- **`config.py`** - Configuration settings and environment variables
- **`algorithm_template.py`** - 🆕 Ready-to-use algorithm template

### 🧪 Testing Files
- **`test_connection.py`** - Basic connectivity test
- **`test_btcusd.py`** - BTCUSD-specific connectivity test  
- **`quick_test_bot.py`** - Complete trading system validation

### 📄 Documentation
- **`README.md`** - This comprehensive guide

---

## 🤖 Algorithm Template Features

The `algorithm_template.py` provides a complete foundation for building trading algorithms:

### 📊 **Built-in Components:**
- **Authentication**: Automatic login and token management
- **Market Data**: Real-time and historical data retrieval
- **Position Management**: Open, close, and monitor positions
- **Account Info**: Balance and equity tracking
- **Error Handling**: Production-ready exception handling

### ⚙️ **Customizable Parameters:**
```python
self.symbol = 'BTCUSD'          # Trading symbol
self.timeframe = 'M1'           # Timeframe (M1, M5, H1, H4, D1)
self.volume = 0.01              # Position size
self.max_positions = 3          # Maximum open positions
self.stop_loss_pips = 50        # Stop loss in pips
self.take_profit_pips = 100     # Take profit in pips
```

### 🎯 **Example Strategies to Implement:**
1. **Moving Average Crossover** ✅ (included)
2. **RSI Overbought/Oversold**
3. **MACD Signal Line Cross**
4. **Bollinger Bands Mean Reversion**
5. **Breakout Trading**
6. **Grid Trading**
7. **Scalping Strategies**
8. **Swing Trading**
9. **News-Based Trading**
10. **Machine Learning Models**

---

## 📚 API Client Reference

### Main Methods (fundezy_trading_client.py)
- `login()` - Authenticate with platform
- `get_balance()` - Get account balance and equity
- `get_candles(symbol, interval, count)` - Get historical data
- `open_position(instrument, order_side, volume)` - Open new position
- `close_position(position_id, instrument, order_side, volume)` - Close position
- `get_open_positions()` - Get all open positions

### Token Management Methods (NEW)
- `refresh_token()` - Manually refresh authentication token
- `get_token_status()` - Get current token status and expiry information
- `_ensure_valid_token()` - Internal method for automatic token validation

### Example Usage
```python
from fundezy_trading_client import FundezyTradingClient

client = FundezyTradingClient()
client.login()

# Get balance
balance = client.get_balance()
print(f"Balance: ${balance['balance']}")

# Open position
result = client.open_position('BTCUSD', 'BUY', 0.01)
print(f"Order ID: {result['orderId']}")

# Get positions
positions = client.get_open_positions()
print(f"Open positions: {len(positions)}")
```

---

## 🔧 Troubleshooting

### Common Setup Issues

**❌ Repository Cloning Issues**
- **"Git not found"**: Install Git from [git-scm.com](https://git-scm.com/)
- **"Permission denied"**: Use HTTPS URL instead of SSH, or download ZIP file from GitHub
- **"Directory not empty"**: Choose a different directory or remove existing files

**❌ Python/Dependencies Issues**
- **"Python not found"**: Install Python 3.8+ from [python.org](https://python.org/)
- **"pip not found"**: Ensure Python was installed with pip, or install pip separately
- **"Module not found"**: Make sure you're in the correct project directory and ran `pip install`

**❌ File/Directory Issues**
- **"No such file or directory"**: Ensure you're in the `AlgoTradingGuide` directory after cloning
- **"Permission denied"**: Check file permissions or run terminal as administrator (Windows)

### Common Runtime Issues

**❌ Login Failed**
- Check credentials in `.env` file
- Ensure account has API access enabled
- Verify broker ID is "107"

**❌ Position Opening Failed**
- Check sufficient account balance
- Verify symbol format (BTCUSD, EURUSD, XAUUSD)
- Ensure minimum position size (0.01)

**❌ Connection Issues**
- Check internet connection
- Verify platform is not under maintenance
- Try refreshing authentication tokens

**❌ Token Refresh Issues**
- **"Failed to refresh token"**: Check network connectivity and verify credentials are still valid
- **"SSL certificate problem"**: The client automatically disables SSL verification
- **"Web Filter Violation"**: Check corporate firewall settings, ensure access to `platform.fundezy.io`
- **Authentication loops**: Verify account has API access enabled

**❌ Algorithm Template Issues**
- Ensure all dependencies are installed
- Check that your strategy logic is implemented in `analyze_market()`
- Verify position management rules in `manage_positions()`

---

## 🔗 API Endpoints

### Authentication
- **Login**: `POST /manager/mtr-login`

### Trading API
- **Base URL**: `https://platform.fundezy.io/mtr-api/{SYSTEM_UUID}`
- **Balance**: `GET /balance`
- **Candles**: `GET /candles?symbol={SYMBOL}&interval={INTERVAL}&count={COUNT}`
- **Open Position**: `POST /position/open`
- **Get Positions**: `GET /open-positions`
- **Close Position**: `POST /position/close`

### Position Format Examples

**Opening:**
```json
{
  "instrument": "BTCUSD",
  "orderSide": "BUY",
  "volume": 0.01,
  "slPrice": 0,
  "tpPrice": 0
}
```

**Closing:**
```json
{
  "positionId": "W6093823881210053",
  "instrument": "BTCUSD", 
  "orderSide": "BUY",
  "volume": "0.01"
}
```

---

## 🎯 Development Workflow

### For Beginners:
1. **Run tests** to validate your setup (`test_connection.py`, `quick_test_bot.py`)
2. **Copy the template**: `cp algorithm_template.py my_first_bot.py`
3. **Customize parameters** (symbol, timeframe, position size)
4. **Modify the strategy** in the `analyze_market()` method
5. **Test with small positions** before going live

### For Advanced Users:
1. **Use the API client** directly with `fundezy_trading_client.py`
2. **Build custom algorithms** from scratch
3. **Implement complex strategies** with multiple indicators
4. **Add portfolio management** and risk controls
5. **Deploy production systems** with logging and monitoring

---

## 📊 What You Get

### ✅ Complete Trading System
- **API Client**: Full Fundezy platform integration
- **Algorithm Template**: Ready-to-use trading bot foundation
- **Position Management**: Open, monitor, close positions
- **Real-time Data**: Live market data and account information
- **Error Handling**: Production-ready exception handling

### ✅ Trading Capabilities
- **24/7 Trading**: BTCUSD crypto market support
- **Live Trading**: Real account trading capabilities
- **Risk Management**: Position sizing, stop loss, take profit
- **Multiple Assets**: Forex, Crypto, Commodities
- **Flexible Strategies**: Easy to implement any trading logic

### ✅ Development Tools
- **Testing Suite**: Comprehensive connectivity and functionality tests
- **Template System**: Start building algorithms immediately
- **Documentation**: Complete API reference and examples
- **Configuration**: Environment-based credential management

---

## 🚀 Next Steps

1. **Validate your setup** with the quick test
2. **Copy the algorithm template** and rename it
3. **Implement your trading strategy** in the template
4. **Test with small positions** to verify your logic
5. **Scale up** when you're confident in your algorithm
6. **Monitor and optimize** your strategy performance

Happy algorithmic trading! 🚀📈