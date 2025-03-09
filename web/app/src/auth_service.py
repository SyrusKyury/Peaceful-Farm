from flask import request, session, redirect
from src.settings_system import SettingsSystem
from src.service import Service
import hashlib
import hmac

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
            
            if (stored_username and stored_password and 
                hmac.compare_digest(stored_username, username) and 
                hmac.compare_digest(stored_password, password)):
                return True
        return False


    def check_hash(self, hash_value):
        for account in self.accounts:
            stored_username = account.get('username')
            stored_password = account.get('password')
            
            if stored_username and stored_password:
                expected_hash = self.generate_hash(stored_username, stored_password)
                if hmac.compare_digest(expected_hash, hash_value):
                    return True
        return False


    def generate_hash(self, username, password):
        return hashlib.sha256(f"{username}:{password}".encode()).hexdigest()


    def requires_auth(self, f):
        def decorated(*args, **kwargs):
            if not self.require_auth:
                return f(*args, **kwargs)
            
            auth = session.get('auth')
            if not auth or not isinstance(auth, str) or not self.check_hash(auth):
                return redirect('/login')
            
            return f(*args, **kwargs)
        
        decorated.__name__ = f.__name__  # Necessario per Flask
        return decorated


    def requires_api_key(self, f):
        def decorated(*args, **kwargs):
            api_key = request.json.get('api_key') if request.is_json else None
            
            if not api_key or not isinstance(api_key, str) or not hmac.compare_digest(api_key, self.api_key):
                return "Unauthorized client", 401
            
            return f(*args, **kwargs)
        
        decorated.__name__ = f.__name__  # Necessario per Flask
        return decorated