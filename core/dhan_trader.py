import json
import logging
import time
from dhanhq import dhanhq
from .encryption import EncryptionManager

class DhanTrader:
    """Refactored Dhan trading logic for web application"""
    
    def __init__(self):
        self.config = self.load_config()
        self.encryption_manager = EncryptionManager()
        self.master_connection = None
        self.child_connections = {}
        self.master_connected = False
        self.connected_children = []
        self.is_initialized = False
        self.is_active = False
        
        # Set up logging
        logging.basicConfig(
            filename='logcopytrade.log',
            format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
            level=logging.INFO
        )
        
        self.initialize_connections()
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config if file doesn't exist
            return {
                "MASTER": {"client_id": "", "access_token": ""},
                "CHILD": {},
                "DONOTPROCESSPROD": ["BO", "CO"]
            }
    
    def save_config(self):
        """Save configuration to config.json"""
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_dhan_connection(self, client_id, encrypted_token):
        """Create a Dhan API connection"""
        try:
            decrypted_token = self.encryption_manager.decrypt_token(encrypted_token)
            dhan = dhanhq(client_id=client_id, access_token=decrypted_token)
            
            # Test connection with fund limits
            test = dhan.get_fund_limits()
            if test.get('status') != 'success':
                raise Exception(f"Connection test failed: {test}")
            
            logging.info(f"Successfully connected to account {client_id}")
            return dhan
        except Exception as e:
            logging.error(f"Failed to connect to {client_id}: {e}")
            raise
    
    def initialize_connections(self):
        """Initialize all trading connections"""
        try:
            # Connect to master account
            master_config = self.config.get('MASTER', {})
            if master_config.get('client_id') and master_config.get('access_token'):
                self.master_connection = self.create_dhan_connection(
                    master_config['client_id'],
                    master_config['access_token']
                )
                self.master_connected = True
                logging.info(f"Master account {master_config['client_id']} connected")
            
            # Connect to child accounts
            children = self.config.get('CHILD', {})
            self.connected_children = []
            
            for name, child_config in children.items():
                if child_config.get('enabled') == 'Y' and child_config.get('client_id'):
                    try:
                        connection = self.create_dhan_connection(
                            child_config['client_id'],
                            child_config['access_token']
                        )
                        self.child_connections[name] = {
                            'connection': connection,
                            'client_id': child_config['client_id'],
                            'multiplier': child_config.get('multiplier', 1.0)
                        }
                        self.connected_children.append(name)
                        logging.info(f"Child account {child_config['client_id']} connected")
                    except Exception as e:
                        logging.error(f"Failed to connect child account {name}: {e}")
            
            self.is_initialized = True
            logging.info("Trading system initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize trading system: {e}")
            self.is_initialized = False
    
    def get_account_margins(self, dhan_connection):
        """Get margin information for a specific account"""
        try:
            margin = dhan_connection.get_fund_limits()
            if margin['status'] == 'success':
                funds = margin['data']
                return {
                    'available': funds.get('equity_amount', 0) + funds.get('commodity_amount', 0),
                    'used': funds.get('utilised_amount', 0),
                    'cash': funds.get('opening_balance', 0),
                    'status': 'success'
                }
        except Exception as e:
            logging.error(f"Error fetching margins: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def get_all_margins(self):
        """Get margin information for all connected accounts"""
        margins = {}
        
        # Master account margins
        if self.master_connection:
            master_config = self.config.get('MASTER', {})
            client_id = master_config.get('client_id', 'MASTER')
            margins[client_id] = self.get_account_margins(self.master_connection)
            margins[client_id]['type'] = 'master'
        
        # Child account margins
        for name, child_info in self.child_connections.items():
            client_id = child_info['client_id']
            margins[client_id] = self.get_account_margins(child_info['connection'])
            margins[client_id]['type'] = 'child'
            margins[client_id]['multiplier'] = child_info['multiplier']
            margins[client_id]['name'] = name
        
        return margins
    
    def start_trading(self):
        """Start the trading system"""
        if self.is_initialized:
            self.is_active = True
            logging.info("Trading system started")
            return True
        return False
    
    def stop_trading(self):
        """Stop the trading system"""
        self.is_active = False
        logging.info("Trading system stopped")
    
    def add_child_account(self, name, client_id, encrypted_token, multiplier=1.0, enabled='Y'):
        """Add a new child account"""
        try:
            # Test connection first
            connection = self.create_dhan_connection(client_id, encrypted_token)
            
            # Add to configuration
            self.config['CHILD'][name] = {
                'client_id': client_id,
                'access_token': encrypted_token,
                'multiplier': multiplier,
                'enabled': enabled
            }
            
            # Add to active connections
            if enabled == 'Y':
                self.child_connections[name] = {
                    'connection': connection,
                    'client_id': client_id,
                    'multiplier': multiplier
                }
                self.connected_children.append(name)
            
            self.save_config()
            logging.info(f"Added child account {name} - {client_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to add child account {name}: {e}")
            raise
    
    def remove_child_account(self, name):
        """Remove a child account"""
        try:
            # Remove from config
            if name in self.config['CHILD']:
                del self.config['CHILD'][name]
            
            # Remove from active connections
            if name in self.child_connections:
                del self.child_connections[name]
            
            if name in self.connected_children:
                self.connected_children.remove(name)
            
            self.save_config()
            logging.info(f"Removed child account {name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to remove child account {name}: {e}")
            return False
    
    def update_master_account(self, client_id, encrypted_token):
        """Update master account configuration"""
        try:
            # Test connection first
            connection = self.create_dhan_connection(client_id, encrypted_token)
            
            # Update configuration
            self.config['MASTER'] = {
                'client_id': client_id,
                'access_token': encrypted_token
            }
            
            # Update active connection
            self.master_connection = connection
            self.master_connected = True
            
            self.save_config()
            logging.info(f"Updated master account {client_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to update master account: {e}")
            raise