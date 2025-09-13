from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from flask_socketio import SocketIO, emit
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
import json
import os
import threading
import time
from core.dhan_trader import DhanTrader
from core.encryption import EncryptionManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Initialize extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the trading dashboard.'

csrf = CSRFProtect(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Simple user model (in production, use a proper database)
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

# Simple user store (in production, use a proper database)
users = {'admin': 'admin123'}  # username: password

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    client_id = StringField('Client ID', validators=[DataRequired()])
    access_token = TextAreaField('Access Token', validators=[DataRequired()])
    multiplier = FloatField('Multiplier', default=1.0, validators=[DataRequired()])
    enabled = SelectField('Enabled', choices=[('Y', 'Yes'), ('N', 'No')], default='Y')
    submit = SubmitField('Save Account')

class MasterAccountForm(FlaskForm):
    client_id = StringField('Client ID', validators=[DataRequired()])
    access_token = TextAreaField('Access Token', validators=[DataRequired()])
    submit = SubmitField('Save Master Account')

# Global trader instance
trader = None

def initialize_trader():
    """Initialize the trading system"""
    global trader
    try:
        trader = DhanTrader()
        return True
    except Exception as e:
        print(f"Failed to initialize trader: {e}")
        return False

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/accounts')
@login_required
def accounts():
    """Account management page"""
    return render_template('accounts.html')

@app.route('/trading')
@login_required
def trading():
    """Trading monitor page"""
    return render_template('trading.html')

@app.route('/settings')
@login_required
def settings():
    """Settings and configuration page"""
    return render_template('settings.html')

# API Routes
@app.route('/api/accounts/master', methods=['GET', 'POST'])
@login_required
def api_master_account():
    if request.method == 'GET':
        # Return current master account info (without sensitive data)
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                master = config.get('MASTER', {})
                return jsonify({
                    'client_id': master.get('client_id', ''),
                    'connected': trader is not None and trader.master_connected if trader else False
                })
        except:
            return jsonify({'client_id': '', 'connected': False})
    
    elif request.method == 'POST':
        # Update master account
        data = request.json
        try:
            # Update configuration
            config = {}
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
            except:
                pass
            
            # Encrypt the token
            encryption_manager = EncryptionManager()
            encrypted_token = encryption_manager.encrypt_token(data['access_token'])
            
            config['MASTER'] = {
                'client_id': data['client_id'],
                'access_token': encrypted_token
            }
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            # Reinitialize trader
            initialize_trader()
            
            return jsonify({'success': True, 'message': 'Master account updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/accounts/children', methods=['GET', 'POST'])
@login_required
def api_child_accounts():
    if request.method == 'GET':
        # Return child accounts
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                children = config.get('CHILD', {})
                # Remove sensitive data
                safe_children = {}
                for name, account in children.items():
                    safe_children[name] = {
                        'client_id': account.get('client_id', ''),
                        'multiplier': account.get('multiplier', 1.0),
                        'enabled': account.get('enabled', 'Y'),
                        'connected': trader is not None and name in trader.connected_children if trader else False
                    }
                return jsonify(safe_children)
        except:
            return jsonify({})
    
    elif request.method == 'POST':
        # Add new child account
        data = request.json
        try:
            # Validate required fields
            if not all(k in data for k in ['name', 'client_id', 'access_token']):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
            # Check if account name already exists
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    if data['name'] in config.get('CHILD', {}):
                        return jsonify({'success': False, 'error': 'Account name already exists'}), 400
            except:
                pass
            
            # Encrypt the token
            encryption_manager = EncryptionManager()
            encrypted_token = encryption_manager.encrypt_token(data['access_token'])
            
            # Add account using trader if available
            if trader:
                success = trader.add_child_account(
                    name=data['name'],
                    client_id=data['client_id'],
                    encrypted_token=encrypted_token,
                    multiplier=float(data.get('multiplier', 1.0)),
                    enabled=data.get('enabled', 'Y')
                )
                if success:
                    return jsonify({'success': True, 'message': 'Child account added successfully'})
                else:
                    return jsonify({'success': False, 'error': 'Failed to add child account'}), 400
            else:
                return jsonify({'success': False, 'error': 'Trading system not initialized'}), 500
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/accounts/children/<name>', methods=['PUT', 'DELETE'])
@login_required
def api_child_account_detail(name):
    if request.method == 'PUT':
        # Update existing child account
        data = request.json
        try:
            # Check if account exists
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    if name not in config.get('CHILD', {}):
                        return jsonify({'success': False, 'error': 'Account not found'}), 404
            except:
                return jsonify({'success': False, 'error': 'Configuration file not found'}), 500
            
            # Remove old account
            if trader:
                trader.remove_child_account(name)
            
            # Encrypt the token if provided
            encrypted_token = None
            if 'access_token' in data and data['access_token']:
                encryption_manager = EncryptionManager()
                encrypted_token = encryption_manager.encrypt_token(data['access_token'])
            else:
                # Keep existing token if not provided
                existing_account = config['CHILD'][name]
                encrypted_token = existing_account.get('access_token')
            
            # Add updated account
            if trader:
                success = trader.add_child_account(
                    name=name,
                    client_id=data.get('client_id', config['CHILD'][name]['client_id']),
                    encrypted_token=encrypted_token,
                    multiplier=float(data.get('multiplier', config['CHILD'][name].get('multiplier', 1.0))),
                    enabled=data.get('enabled', config['CHILD'][name].get('enabled', 'Y'))
                )
                if success:
                    return jsonify({'success': True, 'message': 'Child account updated successfully'})
                else:
                    return jsonify({'success': False, 'error': 'Failed to update child account'}), 400
            else:
                return jsonify({'success': False, 'error': 'Trading system not initialized'}), 500
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    elif request.method == 'DELETE':
        # Delete child account
        try:
            # Check if account exists
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    if name not in config.get('CHILD', {}):
                        return jsonify({'success': False, 'error': 'Account not found'}), 404
            except:
                return jsonify({'success': False, 'error': 'Configuration file not found'}), 500
            
            # Remove account using trader
            if trader:
                success = trader.remove_child_account(name)
                if success:
                    return jsonify({'success': True, 'message': 'Child account deleted successfully'})
                else:
                    return jsonify({'success': False, 'error': 'Failed to delete child account'}), 400
            else:
                return jsonify({'success': False, 'error': 'Trading system not initialized'}), 500
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/margins')
@login_required
def api_margins():
    """Get current margin information for all accounts"""
    if trader and trader.is_initialized:
        return jsonify(trader.get_all_margins())
    return jsonify({})

@app.route('/api/trading/status')
@login_required
def api_trading_status():
    """Get current trading status"""
    if trader:
        return jsonify({
            'active': trader.is_active if hasattr(trader, 'is_active') else False,
            'master_connected': trader.master_connected if hasattr(trader, 'master_connected') else False,
            'children_count': len(trader.connected_children) if hasattr(trader, 'connected_children') else 0,
            'last_update': time.time()
        })
    return jsonify({'active': False, 'master_connected': False, 'children_count': 0})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        emit('status', {'message': 'Connected to trading system'})
        # Start sending live updates
        start_live_updates()
    else:
        return False

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

def start_live_updates():
    """Start background thread for live updates"""
    if not hasattr(app, '_live_updates_thread'):
        app._live_updates_thread = threading.Thread(target=live_updates_worker)
        app._live_updates_thread.daemon = True
        app._live_updates_thread.start()

def live_updates_worker():
    """Background worker for live updates"""
    while True:
        try:
            if trader and trader.is_initialized:
                # Emit margin updates
                margins = trader.get_all_margins()
                socketio.emit('margin_update', margins)
                
                # Emit trading status
                status = {
                    'active': getattr(trader, 'is_active', False),
                    'master_connected': getattr(trader, 'master_connected', False),
                    'children_count': len(getattr(trader, 'connected_children', [])),
                    'timestamp': time.time()
                }
                socketio.emit('status_update', status)
                
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            print(f"Live update error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    # Initialize the trading system
    initialize_trader()
    
    # Run the application
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)