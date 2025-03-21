from flask import request, jsonify
from src.settings_system import SettingsSystem
from src.service import Service
from src.user import User
from functools import wraps

class AuthService(Service):

    def __init__(self, settings_system: SettingsSystem):
        super().__init__(settings_system)
    

    def update_settings(self):
        self.accounts = self.settings_system.get_setting('ACCOUNTS')
        self.require_auth = self.settings_system.get_setting('REQUIRE_AUTH')
        self.api_key = self.settings_system.get_setting('API_KEY')


    def check_credentials(self, username, password):
        for account in self.accounts:
            stored_username = account.get('username')
            stored_password = account.get('password')
            
            if stored_username and stored_password and stored_username == username and stored_password == password:
                return True
            
        return False
    

    def requires_api_key(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.json.get('api_key') if request.is_json else None
            
            if not api_key or api_key != self.api_key:
                return jsonify({'error': 'Unauthorized'}), 401
                        
            return f(*args, **kwargs)
        
        return decorated
    

    def load_user(self, username : str) -> User:
        return User(username) if any(account.get('username') == username for account in self.accounts) else None