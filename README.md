# Python Trading Algorithm Development for Fundezy Platform

A complete guide for developing Python-based trading algorithms on the Fundezy Trading Platform via API services.

## 🚀 Quick Start (5 Steps)

1. **[Install Python Dependencies](#1-install-dependencies)**
2. **[Setup Credentials](#2-setup-credentials)** 
3. **[Test Connection](#3-test-connection)**
4. **[Run Quick Test](#4-run-quick-test)**
5. **[Build Your Algorithm](#5-build-your-algorithm)**

**🎯 Complete System**: This provides a fully functional trading system with position management, real-time data, live trading capabilities, and a ready-to-use algorithm template.

---

## 1. Install Dependencies

```bash
pip install requests pandas numpy
```

## 2. Setup Credentials

Create a `.env` file in the project root:

```bash
FTP_API_BASE_URL=https://platform.fundezy.io
FTP_EMAIL=your-email@example.com
FTP_PASSWORD=your-password
FTP_BROKER_ID=107
```

> **Note**: All sensitive data is loaded from environment variables - nothing sensitive is committed to git.

## 3. Test Connection

```bash
python test_connection.py
```

This verifies your credentials and platform connectivity.

## 4. Run Quick Test

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

## 5. Build Your Algorithm

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

### Common Issues

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