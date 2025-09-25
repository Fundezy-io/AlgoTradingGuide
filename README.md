# Python Trading Algorithm Development for Fundezy Platform

A simple guide for developing Python-based trading algorithms on the Fundezy Trading Platform via API services.

## 🚀 Quick Start (5 Steps)

1. **[Install Python Dependencies](#1-install-dependencies)**
2. **[Setup Credentials](#2-setup-credentials)** 
3. **[Test Connection](#3-test-connection)**
4. **[Run Quick Test](#4-run-quick-test)**
5. **[Start Trading](#5-start-trading)**

**🎯 Complete System**: This provides a fully functional trading system with position management, real-time data, and live trading capabilities.

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

## 5. Start Trading

The `quick_test_bot.py` offers multiple modes:
- **2-minute test** (recommended first)
- **5-minute test** 
- **10-minute test**
- **Continuous trading**

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

---

## 📋 What You Get

### ✅ Core Components
- **Complete API Client**: All trading endpoints included
- **Position Management**: Open, monitor, close positions
- **Real-time Data**: Live market data and account information
- **Error Handling**: Production-ready exception handling

### ✅ Trading Features
- **24/7 Trading**: BTCUSD crypto market support
- **Live Trading**: Real account trading capabilities
- **Risk Management**: Position sizing, stop loss, take profit
- **Multiple Assets**: Forex, Crypto, Commodities

### ✅ Test Files
- `test_connection.py` - Basic connectivity test
- `test_btcusd.py` - BTCUSD-specific connectivity test
- `quick_test_bot.py` - Complete trading system test

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

## 🎯 Next Steps

1. **Start with the quick test** to validate your setup
2. **Modify the test bot** for your trading strategy
3. **Add your indicators** (moving averages, RSI, etc.)
4. **Implement risk management** (stop loss, position sizing)
5. **Deploy for live trading**

Happy trading! 🚀📈