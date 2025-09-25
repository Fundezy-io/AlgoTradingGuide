import pandas as pd
import time
import random
from fundezy_trading_client import FundezyTradingClient

class AutoQuickTestBot:
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
    
    def run_auto_test(self):
        """Run automatic quick test for 2 minutes"""
        print(f"🚀 Starting Auto Quick Test Bot for {self.symbol}")
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
    bot = AutoQuickTestBot()
    bot.run_auto_test()
