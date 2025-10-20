import pandas as pd
import time
import random
from fundezy_trading_client import FundezyTradingClient

class QuickTestTradingBot:
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
                    print(f"✅ Randomly closed {position_to_close.get('side')} position: {position_to_close.get('id')}")
                    print(f"   Volume: {position_to_close.get('volume')}")
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
                    print(f"✅ Closed position (max limit): {position_to_close.get('side')} {position_to_close.get('id')}")
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
                        print(f"💱 Volume: {self.volume}")
                    else:
                        print(f"❌ Failed to open position: {result}")
                        
                except Exception as e:
                    print(f"❌ Error opening position: {e}")
                    
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
    
    def get_current_price_info(self):
        """Get current BTCUSD price information"""
        try:
            # Try to get recent candle data for price info
            candle_response = self.client.get_candles(self.symbol, 'M1', 1)
            if candle_response and 'candles' in candle_response:
                candles = candle_response['candles']
                if candles:
                    latest = candles[-1]
                    return f"Current {self.symbol}: {latest.get('close', 'N/A')}"
            return f"Current {self.symbol}: Price data unavailable"
        except:
            return f"Current {self.symbol}: Unable to fetch price"
    
    def run_quick_test(self, duration_minutes=5):
        """Run quick test for specified duration"""
        print(f"🚀 Starting Quick Test Trading Bot for {self.symbol}")
        print(f"⚡ Test interval: {self.test_interval} seconds")
        print(f"⏱️ Test duration: {duration_minutes} minutes")
        print(f"📊 Max positions: {self.max_positions}")
        print(f"💰 Position size: {self.volume}")
        
        # Login first
        if not self.client.login():
            print("❌ Login failed")
            return
            
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        iteration = 0
        
        while time.time() < end_time:
            try:
                iteration += 1
                remaining_time = int(end_time - time.time())
                
                print(f"\n🔄 === Test Iteration {iteration} (⏱️ {remaining_time}s remaining) ===")
                
                # Get account info
                balance_data = self.client.get_balance()
                balance = balance_data.get('balance', 'Unknown')
                equity = balance_data.get('equity', 'Unknown') 
                print(f"💰 Balance: ${balance}, Equity: ${equity}")
                
                # Get price info
                price_info = self.get_current_price_info()
                print(f"📈 {price_info}")
                
                # Generate random signal
                signal = self.get_random_signal()
                print(f"🎲 Random Signal: {signal}")
                
                # Execute random trade
                self.execute_random_trade(signal)
                
                # Show current positions
                positions = self.client.get_open_positions()
                btc_positions = [pos for pos in positions if pos.get('symbol') == self.symbol]
                print(f"📊 Open {self.symbol} positions: {len(btc_positions)}")
                
                if btc_positions:
                    for pos in btc_positions:
                        print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')}")
                
                # Wait for next iteration
                if time.time() < end_time:
                    print(f"⏳ Waiting {self.test_interval} seconds...")
                    time.sleep(self.test_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Test stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in test iteration: {e}")
                time.sleep(5)  # Wait 5 seconds before retry
        
        print(f"\n🏁 Quick test completed!")
        
        # Final position summary
        try:
            final_positions = self.client.get_open_positions()
            btc_final = [pos for pos in final_positions if pos.get('symbol') == self.symbol]
            print(f"📊 Final {self.symbol} positions: {len(btc_final)}")
            
            if btc_final:
                print("🧹 Would you like to close all test positions? (You can do this manually later)")
                for pos in btc_final:
                    print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')}")
        except Exception as e:
            print(f"⚠️ Could not get final position summary: {e}")
    
    def run_continuous(self):
        """
        Run continuous random trading (until stopped)
        
        Note: Tokens are automatically refreshed for long-running operations.
        This bot can run indefinitely without manual token management!
        """
        print(f"🚀 Starting Continuous Random Trading Bot for {self.symbol}")
        print(f"⚡ Trading interval: {self.test_interval} seconds")
        print(f"📊 Max positions: {self.max_positions}")
        print(f"💰 Position size: {self.volume}")
        print("⚠️ Press Ctrl+C to stop")
        
        # Login first
        if not self.client.login():
            print("❌ Login failed")
            return
            
        iteration = 0
        
        while True:
            try:
                iteration += 1
                print(f"\n🔄 === Trading Cycle {iteration} ===")
                
                # Get account info
                balance_data = self.client.get_balance()
                balance = balance_data.get('balance', 'Unknown')
                equity = balance_data.get('equity', 'Unknown') 
                print(f"💰 Balance: ${balance}, Equity: ${equity}")
                
                # Get price info
                price_info = self.get_current_price_info()
                print(f"📈 {price_info}")
                
                # Generate random signal
                signal = self.get_random_signal()
                print(f"🎲 Random Signal: {signal}")
                
                # Execute random trade
                self.execute_random_trade(signal)
                
                # Show current positions
                positions = self.client.get_open_positions()
                btc_positions = [pos for pos in positions if pos.get('symbol') == self.symbol]
                print(f"📊 Open {self.symbol} positions: {len(btc_positions)}")
                
                # Wait for next cycle
                print(f"⏳ Waiting {self.test_interval} seconds...")
                time.sleep(self.test_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in trading cycle: {e}")
                time.sleep(5)  # Wait 5 seconds before retry

    def run_auto_quick_test(self):
        """Run automatic quick test (3 cycles - faster testing)"""
        print(f"🚀 Starting Auto Quick Test Bot for {self.symbol}")
        print(f"⚡ Test interval: {self.test_interval} seconds")
        print(f"⏱️ Test duration: 30 seconds (3 cycles)")
        print(f"📊 Max positions: {self.max_positions}")
        print(f"💰 Position size: {self.volume}")
        print("⚠️ Press Ctrl+C to stop early\n")
        
        # Login first
        if not self.client.login():
            print("❌ Login failed")
            return
            
        # Run for 3 cycles (30 seconds) - designed to test both open and close
        for cycle in range(1, 4):
            try:
                print(f"🔄 === Cycle {cycle}/3 ===")
                
                # Get account info
                balance_data = self.client.get_balance()
                balance = balance_data.get('balance', 'Unknown')
                equity = balance_data.get('equity', 'Unknown') 
                print(f"💰 Balance: ${balance}, Equity: ${equity}")
                
                # Generate strategic signal to ensure both open and close operations
                if cycle == 1:
                    signal = 'BUY'  # First cycle: always open a position
                elif cycle == 2:
                    signal = 'BUY'  # Second cycle: open another or close if at limit
                else:  # cycle == 3
                    signal = 'HOLD'  # Third cycle: force close a position
                
                print(f"🎲 Signal: {signal}")
                
                # Execute trade
                self.execute_random_trade(signal)
                
                # Show current positions
                positions = self.client.get_open_positions()
                btc_positions = [pos for pos in positions if pos.get('symbol') == self.symbol]
                print(f"📊 Open positions: {len(btc_positions)}")
                
                if btc_positions:
                    for pos in btc_positions:
                        print(f"   • {pos.get('side')} {pos.get('volume')} - ID: {pos.get('id')[:8]}...")
                
                # Wait for next cycle (except last one)
                if cycle < 3:
                    print(f"⏳ Waiting {self.test_interval} seconds...\n")
                    time.sleep(self.test_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Test stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in cycle {cycle}: {e}")
                time.sleep(3)
        
        print(f"\n🏁 Auto test completed!")
        
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
    bot = QuickTestTradingBot()
    
    print("🎯 Choose test mode:")
    print("1. Auto quick test (30 seconds)")
    print("2. Quick test (5 minutes)")
    print("3. Extended test (10 minutes)")
    print("4. Continuous trading (until stopped)")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        bot.run_auto_quick_test()
    elif choice == "2":
        bot.run_quick_test(duration_minutes=5)
    elif choice == "3":
        bot.run_quick_test(duration_minutes=10)
    elif choice == "4":
        bot.run_continuous()
    else:
        print("Invalid choice. Running 2-minute auto test...")
        bot.run_auto_quick_test()
