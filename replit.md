# Dhan Copy Trading System

## Overview
This is a Python-based automated copy trading system that replicates trades from a master Dhan account to multiple child accounts in real-time. The system is designed for fund managers, family offices, or traders managing multiple accounts.

## Project Architecture
- **Main Application**: `Dhan_CopyTrader.py` - Core copy trading engine
- **Encryption Utility**: `dhan_encrypt_utility.py` - Token encryption utility
- **Configuration**: `config.json` - Account settings (ignored from git for security)
- **Environment**: `.env` - Encryption keys (ignored from git for security)

## Recent Changes (2025-09-13)
- ✅ Set up Python 3.11 environment with required dependencies
- ✅ Fixed security vulnerability by removing encryption key from console output
- ✅ Updated .gitignore to protect sensitive files (.env, config.json, logs)
- ✅ Improved error messages to guide users through setup process
- ✅ Created workflow configuration for console-based monitoring
- ✅ Generated encryption key and template configuration files

## Current State
The application is successfully configured and runs in the Replit environment. It currently uses placeholder credentials and will exit with a connection error until valid Dhan API credentials are provided.

## User Setup Instructions
1. **Get Dhan API Credentials**:
   - Login to [Dhan Web Platform](https://web.dhan.co)
   - Go to Profile → DhanHQ Trading APIs
   - Generate Access Token for each trading account
   - Note down Client ID and Access Token

2. **Encrypt Your Tokens**:
   ```bash
   python dhan_encrypt_utility.py
   ```
   - Enter each access token when prompted
   - Copy the encrypted values

3. **Configure Accounts**:
   - Edit `config.json` (already created from template)
   - Replace `YOUR_DHAN_CLIENT_ID` with your actual client IDs
   - Replace `encrypted_access_token_here` with encrypted tokens from step 2
   - Adjust multipliers and enable/disable child accounts as needed

4. **Run the System**:
   - The workflow "Dhan Copy Trader" is already configured
   - It will automatically start when you run the project
   - Monitor logs in the console output

## Key Features
- Real-time order replication
- Multiple child account support
- Custom quantity multipliers per account
- Secure encrypted token storage
- Comprehensive logging and error handling
- Margin monitoring across all accounts

## Security Features
- All access tokens are encrypted using Fernet encryption
- Encryption keys stored in .env (git-ignored)
- Configuration files excluded from version control
- No sensitive data printed to console

## Technical Notes
- Uses dhanhq Python SDK for API integration
- Live feed functionality is currently disabled (not available in current package version)
- Fallback mode allows manual testing and monitoring
- Console-based interface for monitoring trading activity

## Files Structure
```
.
├── Dhan_CopyTrader.py          # Main application
├── dhan_encrypt_utility.py     # Token encryption utility
├── dhan_config_template.json   # Configuration template
├── config.json                 # Actual configuration (git-ignored)
├── .env                        # Encryption keys (git-ignored)
├── logcopytrade.log           # Application logs (git-ignored)
├── dhan_requirements.txt      # Python dependencies
└── README.md                  # Detailed project documentation
```

## Dependencies Installed
- dhanhq==2.0.2 (Dhan API SDK)
- cryptography==45.0.7 (Token encryption)
- python-dotenv==1.1.1 (Environment variable management)
- requests==2.32.5 (HTTP client)
- Plus supporting packages (pandas, numpy, etc.)