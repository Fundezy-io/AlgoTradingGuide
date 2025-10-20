from fundezy_trading_client import FundezyTradingClient

def test_connection():
    """Test connection to Fundezy platform"""
    print("🔄 Testing connection to Fundezy platform...")
    
    client = FundezyTradingClient()

    # Test login
    print("📝 Attempting login...")
    if client.login():
        print("✅ Login successful!")
        print(f"📧 Email: {client.email}")
        print(f"🎫 Auth token acquired")
        print(f"💰 Found {len(client.accounts)} trading accounts")
        print(f"🎯 Selected account: {client.selected_account}")
        print(f"🔑 System UUID: {client.system_uuid}")
        
        # Show token status
        token_status = client.get_token_status()
        print(f"⏰ Token expires in: {token_status['expires_in_minutes']:.1f} minutes")
        
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
            print("🚀 You can now run: python quick_test_bot.py")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            print("   Check your account permissions and try again.")
            
    else:
        print("❌ Login failed - check your credentials in config.py")
        print("   Make sure your email and password are correct.")

if __name__ == "__main__":
    test_connection()
