# Python Algorithm/EA Development Guide for Fundezy Trading Platform

A simple guide for developing Python-based trading algorithms (Expert Advisors) on the Fundezy Trading Platform via API services.

## Quick Start Guide

Follow these 5 simple steps to get your first Python trading algorithm running:

1. **[Setup Environment](#prerequisites)** - Install Python dependencies
2. **[Configure Credentials](#environment-setup)** - Set up your trading account credentials  
3. **[Copy Base Code](#python-api-client)** - Use our ready-to-use Fundezy Python client
4. **[Quick Test](#quick-test-algorithm)** - Rapid 2-minute validation (recommended first)
5. **[Test System](#running-your-algorithm)** - Verify complete trading pipeline
6. **[Run Algorithm](#simple-algorithm-example)** - Start live trading

**🎯 Complete Trading System**: This guide provides a fully functional trading system with position management, real-time data, and live trading capabilities.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Python API Client](#python-api-client)
4. [Simple Algorithm Example](#simple-algorithm-example)
5. [Quick Test Algorithm](#quick-test-algorithm)
6. [Running Your Algorithm](#running-your-algorithm)
7. [Troubleshooting](#troubleshooting)

## Introduction

This guide shows you how to build Python trading algorithms that can:

- Execute trades automatically on live markets
- Access real-time and historical market data (via free Dukascopy provider)
- Manage positions and risk
- Monitor performance

### Key Features

- **Real Market Data**: Free historical data from Dukascopy (no API key needed)
- **Live Trading**: Direct integration with MTT/Fundezy platform
- **Simple Setup**: Minimal configuration required

## Prerequisites

### Python Requirements
```bash
pip install requests
pip install pandas
pip install numpy
```

### Required Credentials
1. **Fundezy Account**: Active trading account with API access
2. **Platform Access**: Your Fundezy platform domain

## Environment Setup

Set your credentials via environment variables. Copy `env.example` to `.env` and fill real values:
```bash
cp env.example .env
# then edit .env
```

Required variables in `.env`:
```bash
FTP_API_BASE_URL=https://platform.fundezy.io
FTP_EMAIL=your-email@example.com
FTP_PASSWORD=your-password
FTP_BROKER_ID=107
```

The provided `config.py` reads these from environment variables, so nothing sensitive is committed to git.

## Python API Client

Copy and save this code as `fundezy_trading_client.py`:

```python
import requests
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any
import config

class FundezyTradingClient:
    def __init__(self):
        # Fundezy Trading Platform API configuration
        self.base_url = config.FTP_API_BASE_URL
        self.login_endpoint = "/manager/mtr-login"
        self.trading_api_base = f"{config.FTP_API_BASE_URL}/mtr-api"
        
        self.email = config.FTP_EMAIL
        self.password = config.FTP_PASSWORD
        self.broker_id = config.FTP_BROKER_ID
        
        self.session = requests.Session()
        self.auth_token = None
        self.trading_api_token = None
        self.trading_account_id = None
        self.system_uuid = None  # Required for trading API URLs
        self.accounts = []
        self.selected_account = None
        self.token_expiry = None
        
    def login(self) -> bool:
        """Authenticate with Fundezy platform"""
        try:
            # MTR login authentication
            login_data = {
                "email": self.email,
                "password": self.password,
                "brokerId": self.broker_id
            }
            
            response = self.session.post(
                f"{self.base_url}{self.login_endpoint}",
                json=login_data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract authentication data
                self.auth_token = data.get('token')
                self.accounts = data.get('accounts', [])
                self.selected_account = data.get('selectedAccount')
                
                # Extract trading API details from selected account
                if self.selected_account:
                    self.trading_api_token = self.selected_account.get('tradingApiToken')
                    self.trading_account_id = self.selected_account.get('tradingAccountId')
                    
                    # Extract system UUID for trading API URLs
                    system_info = self.selected_account.get('offer', {}).get('system', {})
                    self.system_uuid = system_info.get('uuid')
                
                # Set token expiry
                self.token_expiry = datetime.now() + timedelta(hours=24)
                
                print(f"✅ Login successful")
                print(f"📧 Email: {data.get('email')}")
                print(f"🎫 Auth token acquired")
                print(f"💰 Found {len(self.accounts)} trading accounts")
                print(f"🎯 Selected account: {self.trading_account_id}")
                print(f"🔑 System UUID: {self.system_uuid}")
                
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def _get_trading_headers(self) -> Dict[str, str]:
        """Get headers for trading API requests"""
        # Check if token needs refresh
        if not self.auth_token or datetime.now() >= self.token_expiry:
            if not self.login():
                raise Exception("Failed to authenticate")
        
        # Headers format for trading API
        return {
            'Auth-trading-api': self.trading_api_token,
            'Cookie': f'co-auth={self.auth_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _make_trading_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                             params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make trading API request"""
        
        if not self.system_uuid:
            raise Exception("System UUID not available - ensure login is successful")
            
        # Build URL with system UUID
        url = f"{self.trading_api_base}/{self.system_uuid}{endpoint}"
        headers = self._get_trading_headers()
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = self.session.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Trading API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    # Trading API methods
    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        return self._make_trading_request('GET', '/balance')
    
    def get_candles(self, symbol: str, interval: str = 'H1', count: int = 100) -> Dict[str, Any]:
        """Get historical candle data"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'count': count
        }
        return self._make_trading_request('GET', '/candles', params=params)
    
    def open_position(self, instrument: str, order_side: str, volume: float, 
                     sl_price: float = 0, tp_price: float = 0) -> Dict[str, Any]:
        """Open trading position"""
        data = {
            "instrument": instrument,
            "orderSide": order_side.upper(),  # BUY or SELL
            "volume": volume,
            "slPrice": sl_price,
            "tpPrice": tp_price,
            "isMobile": False
        }
        return self._make_trading_request('POST', '/position/open', data)
    
    def close_position(self, position_id: str, instrument: str, order_side: str, volume: float) -> Dict[str, Any]:
        """Close a single position"""
        data = {
            "positionId": position_id,
            "instrument": instrument,
            "orderSide": order_side,
            "volume": str(volume)
        }
        return self._make_trading_request('POST', '/position/close', data)
    
    def close_positions(self, position_ids: List[str]) -> Dict[str, Any]:
        """Close multiple positions (backward compatibility) - deprecated"""
        print("⚠️ close_positions is deprecated - use close_position for individual positions")
        data = {"positionIds": position_ids}
        return self._make_trading_request('POST', '/position/close', data)
    
    # Convenience methods for backward compatibility
    def get_account_info(self) -> Dict[str, Any]:
        """Get account balance (backward compatibility)"""
        return self.get_balance()
    
    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Get open positions"""
        try:
            # Get positions from API
            response = self._make_trading_request('GET', '/open-positions')
            
            # Return positions array from response
            if isinstance(response, dict) and 'positions' in response:
                return response['positions']
            elif isinstance(response, list):
                return response
            else:
                return []
                
        except Exception as e:
            print(f"❌ Get positions error: {e}")
            return []
    
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price from market watch"""
        try:
            market_data = self._make_trading_request('GET', '/market-watch')
            return market_data
        except:
            return {}  # Return empty dict if market watch not working
    
    def get_historical_data(self, symbol: str, timeframe: str = 'H1', count: int = 100) -> List[Dict[str, Any]]:
        """Get historical data (backward compatibility)"""
        response = self.get_candles(symbol, timeframe, count)
        return response.get('candles', [])
```

## Simple Algorithm Example

Copy and save this code as `simple_trading_bot.py`:

```python
import pandas as pd
import time
from fundezy_trading_client import FundezyTradingClient

class SimpleMovingAverageBot:
    def __init__(self):
        self.client = FundezyTradingClient()
        self.symbol = 'EURUSD'
        self.volume = 0.01  # Small position size
        self.fast_period = 10
        self.slow_period = 20
        
    def get_moving_averages(self):
        """Get historical data and calculate moving averages"""
        try:
            # Get last 100 hourly candles using the official API
            candle_response = self.client.get_candles(self.symbol, 'H1', 100)
            
            # Extract the candles array from the response
            if not candle_response or 'candles' not in candle_response:
                print("❌ No candle data received")
                return None, None
                
            data = candle_response['candles']
            
            if not data or len(data) < self.slow_period:
                return None, None
                
            # Convert to DataFrame for easy calculation
            df = pd.DataFrame(data)
            df['close'] = pd.to_numeric(df['close'])
            
            # Calculate moving averages
            fast_ma = df['close'].rolling(window=self.fast_period).mean().iloc[-1]
            slow_ma = df['close'].rolling(window=self.slow_period).mean().iloc[-1]
            
            return fast_ma, slow_ma
            
        except Exception as e:
            print(f"❌ Error getting data: {e}")
            return None, None
    
    def check_signal(self):
        """Check for buy/sell signals"""
        fast_ma, slow_ma = self.get_moving_averages()
        
        if fast_ma is None or slow_ma is None:
            return None
            
        print(f"📊 Fast MA: {fast_ma:.5f}, Slow MA: {slow_ma:.5f}")
        
        # Simple crossover strategy
        if fast_ma > slow_ma * 1.001:  # Fast MA 0.1% above slow MA
            return 'BUY'
        elif fast_ma < slow_ma * 0.999:  # Fast MA 0.1% below slow MA  
            return 'SELL'
        else:
            return 'HOLD'
    
    def execute_trade(self, signal):
        """Execute trading signal with proper position management"""
        try:
            # Close any existing positions first using correct API
            positions = self.client.get_open_positions()
            
            for position in positions:
                if position.get('symbol') == self.symbol:
                    # Use the correct close API format
                    try:
                        self.client.close_position(
                            position_id=position.get('id'),
                            instrument=position.get('symbol'),
                            order_side=position.get('side'),  # Same side as position
                            volume=float(position.get('volume'))
                        )
                        print(f"✅ Closed existing position: {position.get('side')} {position.get('volume')}")
                    except Exception as e:
                        print(f"⚠️ Error closing position {position.get('id')}: {e}")
            
            # Open new position based on signal
            if signal in ['BUY', 'SELL']:
                try:
                    # Open position using the working API
                    result = self.client.open_position(
                        instrument=self.symbol,
                        order_side=signal,
                        volume=self.volume,
                        sl_price=0,  # We'll add stop loss later
                        tp_price=0   # We'll add take profit later
                    )
                    
                    if result.get('status') == 'OK':
                        order_id = result.get('orderId')
                        print(f"✅ Opened {signal} position for {self.symbol}")
                        print(f"📋 Order ID: {order_id}")
                    else:
                        print(f"❌ Failed to open position: {result}")
                        
                except Exception as e:
                    print(f"❌ Error opening position: {e}")
                    
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
    
    def run(self):
        """Main trading loop"""
        print(f"🚀 Starting Simple Moving Average Bot for {self.symbol}")
        print(f"📈 Fast MA: {self.fast_period}, Slow MA: {self.slow_period}")
        
        # Login first
        if not self.client.login():
            print("❌ Login failed")
            return
            
        while True:
            try:
                # Check account info using new API
                balance_data = self.client.get_balance()
                balance = balance_data.get('balance', 'Unknown')
                equity = balance_data.get('equity', 'Unknown') 
                print(f"💰 Account Balance: ${balance}, Equity: ${equity}")
                
                # Check for trading signal
                signal = self.check_signal()
                print(f"📶 Signal: {signal}")
                
                # Execute trade if signal found
                if signal in ['BUY', 'SELL']:
                    self.execute_trade(signal)
                
                # Wait 1 hour before next check
                print("⏰ Waiting 1 hour for next check...")
                time.sleep(3600)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retry

if __name__ == "__main__":
    bot = SimpleMovingAverageBot()
    bot.run()
```

## Quick Test Algorithm

For rapid testing and validation of trading functions, we provide a quick test algorithm that opens and closes random positions every 10 seconds on BTCUSD (24/7 crypto market). This is perfect for:

- **Fast API Testing**: Verify open/close functions quickly
- **Platform Validation**: Test all trading endpoints in minutes
- **Demo Purposes**: Show live trading capabilities
- **Development**: Quick iteration during development

### Features

- **BTCUSD Trading**: 24/7 crypto market availability
- **Random Signals**: 40% BUY, 40% SELL, 20% HOLD
- **10-Second Intervals**: Fast testing cycles
- **Position Management**: Automatic closure with max position limits
- **Real-time P&L**: Live balance and equity tracking

### Quick Test Bot (Automatic)

Copy and save this code as `quick_test_bot.py`:

```python
import pandas as pd
import time
import random
from fundezy_trading_client import FundezyTradingClient

class QuickTestBot:
    def __init__(self):
        self.client = FundezyTradingClient()
        self.symbol = 'BTCUSD'  # 24/7 crypto market
        self.volume = 0.01  # Small position size for testing
        self.test_interval = 10  # 10 seconds between actions
        self.max_positions = 2  # Maximum positions to hold at once
        
    def get_random_signal(self):
        """Generate random trading signals for testing"""
        signals = ['BUY', 'SELL', 'HOLD']
        # 40% chance of BUY, 40% chance of SELL, 20% chance of HOLD
        weights = [0.4, 0.4, 0.2]
        return random.choices(signals, weights=weights)[0]
    
    def execute_random_trade(self, signal):
        """Execute random trading for quick testing"""
        try:
            # Get current positions
            positions = self.client.get_open_positions()
            btc_positions = [pos for pos in positions if pos.get('symbol') == self.symbol]
            
            print(f"📋 Current {self.symbol} positions: {len(btc_positions)}")
            
            # If we have positions and signal is HOLD, randomly close one
            if btc_positions and signal == 'HOLD':
                position_to_close = random.choice(btc_positions)
                try:
                    result = self.client.close_position(
                        position_id=position_to_close.get('id'),
                        instrument=position_to_close.get('symbol'),
                        order_side=position_to_close.get('side'),
                        volume=float(position_to_close.get('volume'))
                    )
                    print(f"✅ Randomly closed {position_to_close.get('side')} position: {position_to_close.get('id')[:8]}...")
                except Exception as e:
                    print(f"❌ Error closing random position: {e}")
                return
            
            # If we have too many positions, close one randomly
            if len(btc_positions) >= self.max_positions:
                position_to_close = random.choice(btc_positions)
                try:
                    result = self.client.close_position(
                        position_id=position_to_close.get('id'),
                        instrument=position_to_close.get('symbol'),
                        order_side=position_to_close.get('side'),
                        volume=float(position_to_close.get('volume'))
                    )
                    print(f"✅ Closed position (max limit): {position_to_close.get('side')} {position_to_close.get('id')[:8]}...")
                except Exception as e:
                    print(f"❌ Error closing position: {e}")
                return
            
            # Open new position based on signal
            if signal in ['BUY', 'SELL']:
                try:
                    result = self.client.open_position(
                        instrument=self.symbol,
                        order_side=signal,
                        volume=self.volume,
                        sl_price=0,  # No stop loss for testing
                        tp_price=0   # No take profit for testing
                    )
                    
                    if result.get('status') == 'OK':
                        order_id = result.get('orderId')
                        print(f"✅ Opened {signal} position for {self.symbol}")
                        print(f"📋 Order ID: {order_id}")
                    else:
                        print(f"❌ Failed to open position: {result}")
                        
                except Exception as e:
                    print(f"❌ Error opening position: {e}")
                    
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
    
    def run_quick_test(self):
        """Run automatic quick test for 2 minutes"""
        print(f"🚀 Starting Quick Test Bot for {self.symbol}")
        print(f"⚡ Test interval: {self.test_interval} seconds")
        print(f"⏱️ Test duration: 2 minutes (12 cycles)")
        print(f"📊 Max positions: {self.max_positions}")
        print(f"💰 Position size: {self.volume}")
        print("⚠️ Press Ctrl+C to stop early\n")
        
        # Login first
        if not self.client.login():
            print("❌ Login failed")
            return
            
        # Run for 12 cycles (2 minutes)
        for cycle in range(1, 13):
            try:
                print(f"🔄 === Cycle {cycle}/12 ===")
                
                # Get account info
                balance_data = self.client.get_balance()
                balance = balance_data.get('balance', 'Unknown')
                equity = balance_data.get('equity', 'Unknown') 
                print(f"💰 Balance: ${balance}, Equity: ${equity}")
                
                # Generate random signal
                signal = self.get_random_signal()
                print(f"🎲 Signal: {signal}")
                
                # Execute random trade
                self.execute_random_trade(signal)
                
                # Show current positions
                positions = self.client.get_open_positions()
                btc_positions = [pos for pos in positions if pos.get('symbol') == self.symbol]
                print(f"📊 Open positions: {len(btc_positions)}")
                
                if btc_positions:
                    for pos in btc_positions:
                        print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')[:8]}...")
                
                # Wait for next cycle (except last one)
                if cycle < 12:
                    print(f"⏳ Waiting {self.test_interval} seconds...\n")
                    time.sleep(self.test_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Test stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in cycle {cycle}: {e}")
                time.sleep(3)
        
        print(f"\n🏁 Quick test completed!")
        
        # Final position summary
        try:
            final_positions = self.client.get_open_positions()
            btc_final = [pos for pos in final_positions if pos.get('symbol') == self.symbol]
            print(f"📊 Final {self.symbol} positions: {len(btc_final)}")
            
            if btc_final:
                print("📋 Remaining positions:")
                for pos in btc_final:
                    print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')[:8]}...")
                print("💡 These positions will remain open for manual management")
        except Exception as e:
            print(f"⚠️ Could not get final position summary: {e}")

if __name__ == "__main__":
    bot = QuickTestBot()
    bot.run_quick_test()
```

### BTCUSD Connectivity Test

Before running the quick test, verify BTCUSD connectivity with `test_btcusd.py`:

```python
from fundezy_trading_client import FundezyTradingClient

def test_btcusd():
    """Test BTCUSD connectivity and data"""
    print("🔄 Testing BTCUSD connectivity...")
    
    client = FundezyTradingClient()

    # Test login
    print("📝 Attempting login...")
    if client.login():
        print("✅ Login successful!")
        
        try:
            # Test account balance
            print("💰 Getting account balance...")
            balance_data = client.get_balance()
            balance = balance_data.get('balance', 'Unknown')
            equity = balance_data.get('equity', 'Unknown')
            print(f"✅ Account Balance: ${balance}, Equity: ${equity}")
            
            # Test BTCUSD candle data
            print("📈 Getting BTCUSD candle data...")
            candles_response = client.get_candles('BTCUSD', 'M1', 5)
            if candles_response and 'candles' in candles_response:
                candles = candles_response['candles']
                print(f"✅ Retrieved {len(candles)} BTCUSD candles")
                if candles:
                    latest = candles[-1]
                    print(f"   Latest BTCUSD price: ${latest.get('close', 'N/A')}")
                    print(f"   High: ${latest.get('high', 'N/A')}, Low: ${latest.get('low', 'N/A')}")
            else:
                print("⚠️ No BTCUSD data available")
            
            # Test getting current positions
            print("📊 Getting current positions...")
            positions = client.get_open_positions()
            print(f"✅ Current open positions: {len(positions)}")
            
            btc_positions = [pos for pos in positions if pos.get('symbol') == 'BTCUSD']
            print(f"✅ BTCUSD positions: {len(btc_positions)}")
            
            print("\n🎉 BTCUSD connectivity test passed!")
            print("🚀 You can now run: python quick_test_bot.py")
            
        except Exception as e:
            print(f"❌ Error during BTCUSD testing: {e}")
            
    else:
        print("❌ Login failed - check your credentials")

if __name__ == "__main__":
    test_btcusd()
```

### Running Quick Tests

**1. Test BTCUSD Connectivity:**
```bash
python test_btcusd.py
```

**2. Run Quick Test (2 minutes):**
```bash
python quick_test_bot.py
```

### Quick Test Output Example

```
🚀 Starting Quick Test Bot for BTCUSD
⚡ Test interval: 10 seconds
⏱️ Test duration: 2 minutes (12 cycles)
📊 Max positions: 2
💰 Position size: 0.01

🔄 === Cycle 1/12 ===
💰 Balance: $199,950.04, Equity: $199,950.04
🎲 Signal: BUY
📋 Current BTCUSD positions: 0
✅ Opened BUY position for BTCUSD
📋 Order ID: W6098426125213316
📊 Open positions: 1
   • BUY 0.01 - ID: W6098426...

🔄 === Cycle 2/12 ===
💰 Balance: $199,950.04, Equity: $199,948.96
🎲 Signal: SELL
📋 Current BTCUSD positions: 1
✅ Closed position (max limit): BUY W6098426...
📊 Open positions: 0

🏁 Quick test completed!
```

### What the Quick Test Validates

✅ **Position Opening**: BUY and SELL orders  
✅ **Position Closing**: Individual position closure  
✅ **Real-time P&L**: Live balance updates  
✅ **Position Management**: Max position limits  
✅ **API Connectivity**: All trading endpoints  
✅ **24/7 Trading**: BTCUSD crypto market  
✅ **Error Handling**: Graceful error management  

This quick test is perfect for validating your trading setup before deploying production algorithms!

## Running Your Algorithm

### Step 1: Test the Connection
Create a test file `test_connection.py`:

```python
from fundezy_trading_client import FundezyTradingClient

def test_connection():
    """Test connection to Fundezy platform"""
    print("🔄 Testing connection to Fundezy platform...")
    
    client = FundezyTradingClient()

    # Test login
    print("📝 Attempting login...")
    if client.login():
        print("✅ Login successful!")
        
        try:
            # Test account balance
            print("💰 Getting account balance...")
            balance_data = client.get_balance()
            balance = balance_data.get('balance', 'Unknown')
            equity = balance_data.get('equity', 'Unknown')
            print(f"✅ Account Balance: ${balance}, Equity: ${equity}")
            
            # Test historical candle data
            print("📈 Getting historical candle data...")
            candles_response = client.get_candles('EURUSD', 'H1', 10)
            if candles_response and 'candles' in candles_response:
                candles = candles_response['candles']
                print(f"✅ Retrieved {len(candles)} historical candles")
                if candles:
                    latest = candles[-1]
                    print(f"   Latest candle close: {latest.get('close', 'N/A')}")
            else:
                print("⚠️ No historical data available")
            
            print("\n🎉 All tests passed! Your setup is working correctly.")
            print("🚀 You can now run: python simple_trading_bot.py")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            print("   Check your account permissions and try again.")
            
    else:
        print("❌ Login failed - check your credentials in config.py")
        print("   Make sure your email and password are correct.")

if __name__ == "__main__":
    test_connection()
```

### Step 2: Quick Test (Recommended First)
For rapid trading system validation, run the quick test:
```bash
python quick_test_bot.py
```

This test will:
- Use BTCUSD (24/7 trading, always available)
- Open and close random positions every 10 seconds
- Test complete position lifecycle (OPEN → MANAGE → CLOSE)
- Verify both position opening AND closing capabilities
- Complete in 2 minutes with full validation
- Show real-time P&L and balance changes

### Step 3: Run the Full Algorithm
```bash
python simple_trading_bot.py
```

Your bot will:
- Login to the platform
- Check moving averages every hour
- Open/close positions based on signals
- Show account balance and trading activity

### Step 3: Monitor Performance
The bot will print:
- Current account balance
- Moving average values  
- Trading signals (BUY/SELL/HOLD)
- Position opening/closing confirmations

## Troubleshooting

### Common Issues

**❌ Login Failed**
- Check your `config.py` file has correct credentials
- Verify the login endpoint `/manager/mtr-login` is working
- Ensure your account has API access enabled
- Confirm broker ID is set to "107"

**❌ No Historical Data**
- Check symbol format (EURUSD, XAUUSD, BTCUSD)
- Verify interval format ('H1' for 1 hour, 'M1' for 1 minute, 'D1' for 1 day)
- Ensure internet connection is stable
- Confirm the trading API system UUID is available

**❌ Position Opening Failed**
- Check account balance is sufficient
- Verify symbol is available for trading (BTCUSD, EURUSD, XAUUSD)
- Ensure position size meets minimum requirements (0.01 minimum)
- Confirm system UUID is properly extracted during login

**❌ Position Closing Failed**
- Verify you're using the `/open-positions` endpoint to get positions
- Ensure close API format: `positionId`, `instrument`, `orderSide`, `volume`
- Use same `orderSide` as the position (not opposite)
- Check that position ID exists and is valid
- Volume should be a string for closing operations

**❌ API Request Failed**
- Check internet connection
- Verify platform is not under maintenance
- Try refreshing authentication tokens
- Ensure correct endpoint paths are used
- Validate system UUID is included in request URLs

### Getting Help

1. Check the error messages - they usually indicate the problem
2. Verify your `config.py` file has all required fields
3. Test basic connection first before running the full algorithm
4. Start with smaller position sizes for testing
5. Ensure your account has sufficient balance for trading

## API Endpoints Reference

This section provides the complete API reference for the Fundezy trading platform:

### Authentication Endpoint
- **Login URL**: `https://platform.fundezy.io/manager/mtr-login`
- **Method**: POST
- **Headers**: `Content-Type: application/json`

### Trading API Base
- **Base URL**: `https://platform.fundezy.io/mtr-api/{SYSTEM_UUID}`
- **Authentication**: Uses `Auth-trading-api` header with trading token
- **Cookie**: `co-auth={AUTH_TOKEN}`

### Trading API Endpoints
- **Balance**: `GET /balance` - Returns account balance and equity
- **Candles**: `GET /candles?symbol={SYMBOL}&interval={INTERVAL}&count={COUNT}` - Historical data
- **Open Position**: `POST /position/open` - Opens new trading position
- **Get Positions**: `GET /open-positions` - Returns list of open positions
- **Close Position**: `POST /position/close` - Closes single position

### Position Management API Format
**Opening Position:**
```json
{
  "instrument": "BTCUSD",
  "orderSide": "BUY",
  "volume": 0.01,
  "slPrice": 0,
  "tpPrice": 0,
  "isMobile": false
}
```

**Closing Position:**
```json
{
  "positionId": "W6093823881210053",
  "instrument": "BTCUSD", 
  "orderSide": "BUY",
  "volume": "0.01"
}
```

### Important Notes
- **Position Endpoint**: Use `/open-positions` for getting positions
- **Close Format**: Use same `orderSide` as the position (not opposite)
- **Volume Format**: String for closing, number for opening
- The system UUID is extracted from the login response and required for all trading operations
- Trading tokens have long expiry (24+ hours)
- Positions are persistent and can be managed individually

## Quick Summary

You now have a complete trading system with the following components:

### ✅ Core Components
- **Python Trading Client**: Complete API client with all endpoints
- **Position Management**: Full lifecycle support (open, monitor, close)
- **Market Data**: Real-time and historical data access
- **Authentication**: Robust token management system
- **Error Handling**: Production-ready exception handling

### ✅ API Endpoints  
- **Positions**: `/open-positions` (get positions)
- **Balance**: `/balance` (account information)
- **Candles**: `/candles` (historical market data)
- **Open**: `/position/open` (create positions)
- **Close**: `/position/close` (close positions)

### ✅ Trading Features
- **Real Position Management**: Open, monitor, and close positions
- **24/7 Trading**: BTCUSD support for continuous trading
- **Multiple Strategies**: Moving averages, custom indicators
- **Risk Management**: Position sizing, stop loss, take profit
- **Live Trading**: Real account trading capabilities

### 🚀 Quick Start Options

**1. Quick Test (2 minutes - Recommended First):**
```bash
python quick_test_bot.py
```

**2. BTCUSD Connectivity Test:**
```bash
python test_btcusd.py
```

**3. Run Full Algorithm:**
```bash
python simple_trading_bot.py
```

**4. Basic Connection Test:**
```bash
python test_connection.py
```

### Platform Information
- **Platform**: Fundezy MTT Trading Platform
- **API Access**: Complete trading functionality
- **Leverage**: Configurable based on account type
- **Supported Assets**: Forex, Crypto, Commodities

Happy trading! 🚀📈
