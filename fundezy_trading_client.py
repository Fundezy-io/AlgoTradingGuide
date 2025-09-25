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
