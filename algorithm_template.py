"""
Template Trading Algorithm for Fundezy Platform
===============================================

This template provides all the basic necessary coding for API connection and trading.
Rename this file and add your own trading algorithm logic.

Usage:
1. Rename this file to your algorithm name (e.g., my_strategy.py)
2. Modify the trading logic in the run_algorithm() method
3. Customize the symbol, timeframe, and parameters as needed
4. Run: python your_renamed_file.py

"""

import time
import pandas as pd
from datetime import datetime
from fundezy_trading_client import FundezyTradingClient


class YourTradingAlgorithm:
    def __init__(self):
        """Initialize your trading algorithm"""
        # API Client
        self.client = FundezyTradingClient()
        
        # Trading Parameters - Customize these for your strategy
        self.symbol = 'BTCUSD'  # Trading symbol (BTCUSD, EURUSD, XAUUSD, etc.)
        self.timeframe = 'M1'   # Timeframe (M1, M5, M15, H1, H4, D1)
        self.volume = 0.01      # Position size
        self.max_positions = 3  # Maximum open positions
        
        # Algorithm Parameters - Add your own parameters here
        self.stop_loss_pips = 50     # Stop loss in pips (0 = no stop loss)
        self.take_profit_pips = 100  # Take profit in pips (0 = no take profit)
        self.trading_enabled = True  # Enable/disable trading
        
        # Data storage
        self.candles_history = []
        self.positions = []
        self.account_balance = 0
        self.account_equity = 0
        
        print(f"🤖 {self.__class__.__name__} initialized")
        print(f"📊 Symbol: {self.symbol}")
        print(f"⏰ Timeframe: {self.timeframe}")
        print(f"💰 Position Size: {self.volume}")
        print(f"📈 Max Positions: {self.max_positions}")
    
    def connect_and_authenticate(self):
        """Connect to Fundezy platform and authenticate"""
        print("🔐 Connecting to Fundezy platform...")
        
        if self.client.login():
            print("✅ Authentication successful!")
            return True
        else:
            print("❌ Authentication failed!")
            return False
    
    def get_account_info(self):
        """Get current account balance and equity"""
        try:
            balance_data = self.client.get_balance()
            self.account_balance = balance_data.get('balance', 0)
            self.account_equity = balance_data.get('equity', 0)
            
            print(f"💰 Balance: ${self.account_balance}")
            print(f"💵 Equity: ${self.account_equity}")
            
            return True
        except Exception as e:
            print(f"❌ Error getting account info: {e}")
            return False
    
    def get_market_data(self, count=100):
        """Get historical market data"""
        try:
            print(f"📈 Getting {count} candles for {self.symbol}...")
            
            response = self.client.get_candles(self.symbol, self.timeframe, count)
            
            if response and 'candles' in response:
                self.candles_history = response['candles']
                print(f"✅ Retrieved {len(self.candles_history)} candles")
                
                if self.candles_history:
                    latest = self.candles_history[-1]
                    print(f"📊 Latest {self.symbol} price: {latest.get('close', 'N/A')}")
                
                return True
            else:
                print("⚠️ No market data available")
                return False
                
        except Exception as e:
            print(f"❌ Error getting market data: {e}")
            return False
    
    def get_current_positions(self):
        """Get current open positions"""
        try:
            all_positions = self.client.get_open_positions()
            # Filter positions for our symbol
            self.positions = [pos for pos in all_positions if pos.get('symbol') == self.symbol]
            
            print(f"📊 Open {self.symbol} positions: {len(self.positions)}")
            
            if self.positions:
                for pos in self.positions:
                    print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')[:8]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error getting positions: {e}")
            return False
    
    def analyze_market(self):
        """
        Analyze market data and generate trading signals
        
        This is where you implement your trading strategy!
        Return: 'BUY', 'SELL', or 'HOLD'
        """
        
        if not self.candles_history or len(self.candles_history) < 2:
            return 'HOLD'
        
        # Example: Simple moving average strategy (REPLACE WITH YOUR LOGIC)
        # ------------------------------------------------------------------
        
        # Get recent prices
        prices = [float(candle.get('close', 0)) for candle in self.candles_history[-20:]]
        
        if len(prices) < 20:
            return 'HOLD'
        
        # Calculate simple moving averages
        sma_5 = sum(prices[-5:]) / 5
        sma_20 = sum(prices[-20:]) / 20
        current_price = prices[-1]
        
        print(f"📊 Current Price: {current_price}")
        print(f"📈 SMA(5): {sma_5:.5f}")
        print(f"📈 SMA(20): {sma_20:.5f}")
        
        # Simple strategy: Buy when SMA5 > SMA20, Sell when SMA5 < SMA20
        if sma_5 > sma_20 and len(self.positions) < self.max_positions:
            signal = 'BUY'
        elif sma_5 < sma_20 and len(self.positions) < self.max_positions:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        
        print(f"🎯 Signal: {signal}")
        
        # TODO: REPLACE THE ABOVE WITH YOUR OWN TRADING LOGIC
        # Examples:
        # - RSI indicators
        # - MACD crossovers
        # - Bollinger Bands
        # - Custom indicators
        # - Machine learning models
        # - etc.
        
        return signal
    
    def execute_trade(self, signal):
        """Execute trading based on signal"""
        
        if not self.trading_enabled:
            print("⚠️ Trading disabled")
            return
        
        if signal == 'HOLD':
            print("⏸️ Holding position")
            return
        
        # Check if we already have max positions
        if len(self.positions) >= self.max_positions:
            print(f"⚠️ Max positions ({self.max_positions}) reached")
            return
        
        try:
            # Calculate stop loss and take profit (optional)
            sl_price = 0  # Set to 0 for no stop loss
            tp_price = 0  # Set to 0 for no take profit
            
            # Open position
            result = self.client.open_position(
                instrument=self.symbol,
                order_side=signal,
                volume=self.volume,
                sl_price=sl_price,
                tp_price=tp_price
            )
            
            if result.get('status') == 'OK':
                order_id = result.get('orderId')
                print(f"✅ Opened {signal} position for {self.symbol}")
                print(f"📋 Order ID: {order_id}")
                print(f"💱 Volume: {self.volume}")
            else:
                print(f"❌ Failed to open position: {result}")
                
        except Exception as e:
            print(f"❌ Error executing trade: {e}")
    
    def close_position(self, position):
        """Close a specific position"""
        try:
            result = self.client.close_position(
                position_id=position.get('id'),
                instrument=position.get('symbol'),
                order_side=position.get('side'),
                volume=float(position.get('volume'))
            )
            
            print(f"✅ Closed {position.get('side')} position: {position.get('id')[:8]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error closing position: {e}")
            return False
    
    def manage_positions(self):
        """
        Manage existing positions (stop loss, take profit, trailing stops, etc.)
        
        Add your position management logic here!
        """
        
        if not self.positions:
            return
        
        print(f"🔧 Managing {len(self.positions)} positions...")
        
        # Example: Close positions based on your criteria
        # TODO: IMPLEMENT YOUR POSITION MANAGEMENT LOGIC
        
        for position in self.positions:
            # Example logic - you can modify this
            position_age = time.time()  # Calculate position age if needed
            
            # Add your position management rules here:
            # - Trailing stops
            # - Time-based exits
            # - Profit target adjustments
            # - Risk management rules
            
            pass  # Remove this and add your logic
    
    def run_algorithm(self):
        """
        Main algorithm loop
        
        Customize the frequency and logic as needed for your strategy
        
        Note: The FundezyTradingClient automatically handles token refresh
        for long-running algorithms. No additional code needed!
        """
        print(f"🚀 Starting {self.__class__.__name__}")
        print("⚠️ Press Ctrl+C to stop\n")
        
        # Connect to platform
        if not self.connect_and_authenticate():
            return
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n🔄 === Algorithm Iteration {iteration} ===")
                print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Step 1: Get account information
                if not self.get_account_info():
                    continue
                
                # Step 2: Get current market data
                if not self.get_market_data():
                    continue
                
                # Step 3: Get current positions
                if not self.get_current_positions():
                    continue
                
                # Step 4: Analyze market and generate signal
                signal = self.analyze_market()
                
                # Step 5: Execute trades based on signal
                self.execute_trade(signal)
                
                # Step 6: Manage existing positions
                self.manage_positions()
                
                # Step 7: Wait before next iteration
                print(f"⏳ Waiting 60 seconds before next iteration...")
                time.sleep(60)  # Wait 1 minute - adjust as needed for your strategy
                
        except KeyboardInterrupt:
            print("\n🛑 Algorithm stopped by user")
        except Exception as e:
            print(f"\n❌ Algorithm error: {e}")
        finally:
            print("🏁 Algorithm finished")


def main():
    """Main function to run your algorithm"""
    
    # Create and run your algorithm
    algorithm = YourTradingAlgorithm()
    algorithm.run_algorithm()


if __name__ == "__main__":
    main()


"""
CUSTOMIZATION GUIDE:
===================

1. RENAME THIS FILE:
   - Rename to something like: my_strategy.py, scalper_bot.py, etc.

2. CUSTOMIZE PARAMETERS:
   - Change symbol, timeframe, volume in __init__()
   - Add your own algorithm parameters

3. IMPLEMENT YOUR STRATEGY:
   - Modify analyze_market() method with your trading logic
   - Add indicators, signals, and decision logic

4. POSITION MANAGEMENT:
   - Implement position management in manage_positions()
   - Add stop loss, take profit, trailing stops

5. TIMING:
   - Adjust the sleep interval in run_algorithm()
   - Consider market hours and your strategy frequency

6. RISK MANAGEMENT:
   - Add portfolio size limits
   - Implement drawdown protection
   - Add correlation checks for multiple symbols

7. LOGGING:
   - Add file logging for trade history
   - Implement performance tracking
   - Add error logging

8. TESTING:
   - Start with small position sizes
   - Test on demo account first
   - Validate your logic thoroughly

EXAMPLE STRATEGIES TO IMPLEMENT:
===============================

1. Moving Average Crossover
2. RSI Overbought/Oversold
3. MACD Signal Line Cross
4. Bollinger Bands Mean Reversion
5. Breakout Trading
6. Grid Trading
7. Scalping Strategies
8. Swing Trading
9. News-Based Trading
10. Machine Learning Models

Happy Algorithm Trading! 🚀📈
"""
