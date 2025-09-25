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
