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
