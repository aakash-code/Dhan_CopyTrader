# Quick Setup Guide

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/dhan-copy-trading.git
cd dhan-copy-trading
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Dhan API Access
1. Login to [Dhan Web Platform](https://web.dhan.co)
2. Go to **Profile** → **DhanHQ Trading APIs**
3. Click **"Request Access"** (first time users)
4. Generate **Access Token** for each trading account
5. Note down your **Client ID** and **Access Token**

### 4. Setup Configuration

#### Step 4a: Encrypt Your Access Tokens
```bash
python encrypt_token.py
```
- Enter each access token when prompted
- Copy the encrypted values

#### Step 4b: Create Configuration File
```bash
cp configTemplate.json config.json
```

Edit `config.json` with your details:
```json
{
    "MASTER": {
        "client_id": "YOUR_MASTER_CLIENT_ID",
        "access_token": "ENCRYPTED_TOKEN_FROM_STEP_4A"
    },
    "CHILD": {
        "CHILD1": {
            "client_id": "CHILD_CLIENT_ID",
            "access_token": "ENCRYPTED_TOKEN_FROM_STEP_4A",
            "multiplier": 1,
            "enabled": "Y"
        }
    }
}
```

### 5. Run the System
```bash
python dhan_copytrader.py
```

## ⚠️ Important Notes

- **Test with small quantities** first
- **Ensure sufficient margins** in all accounts  
- **Monitor logs** for any issues
- **Keep access tokens secure** and never share them

## 📊 Features

✅ Real-time order copying  
✅ Multiple child accounts  
✅ Quantity multipliers  
✅ Order management (create/update/cancel)  
✅ Margin monitoring  
✅ Comprehensive logging  

## 🆘 Need Help?

- Check `logcopytrade.log` for detailed logs
- Ensure all accounts have API access enabled
- Verify client IDs and access tokens are correct
- Test individual account connections first

# 🚀 Dhan Copy Trading System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dhan API](https://img.shields.io/badge/Dhan-API%20Integrated-orange.svg)](https://dhanhq.co/docs/v2/)

An advanced **automated copy trading system** that replicates trades from a master Dhan account to multiple child accounts in real-time. Perfect for fund managers, family offices, or traders managing multiple accounts.

## ✨ Key Features

🔄 **Real-time Order Replication** - Instantly copies orders across accounts  
👥 **Multi-Account Support** - Manage unlimited child accounts  
⚖️ **Custom Multipliers** - Different position sizes per account  
📊 **Live Margin Monitoring** - Real-time fund tracking  
🔐 **Secure Token Management** - Encrypted credential storage  
📝 **Comprehensive Logging** - Detailed audit trail  
🎛️ **Smart Filtering** - Exclude specific product types  
⚡ **Auto Order Management** - Handles create, modify, cancel operations  

## 📋 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/dhan-copy-trading.git
cd dhan-copy-trading

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Setup configuration
python encrypt_token.py
cp configTemplate.json config.json
# Edit config.json with your details

# 4. Run the system
python dhan_copytrader.py
```

📖 **[Complete Setup Guide →](SETUP.md)**

## 🏗️ System Architecture

```
Master Account (Dhan) → Order Placed
         ↓
Copy Trading Engine
         ↓
Child Account 1 (Multiplier: 1.0) → Same quantity
Child Account 2 (Multiplier: 0.5) → Half quantity
Child Account 3 (Multiplier: 2.0) → Double quantity
```

## 📊 Dashboard View

```
---Client ID--------Available--------Used---------Cash Available-----------
MASTER123    :      500,000       50,000        450,000
CHILD001     :      250,000       25,000        225,000  
CHILD002     :      100,000       10,000         90,000
--------------------------------------------------------------------
```

## ⚙️ Configuration

### Basic Configuration (`config.json`)

```json
{
    "MASTER": {
        "client_id": "YOUR_MASTER_CLIENT_ID",
        "access_token": "encrypted_access_token"
    },
    "CHILD": {
        "PORTFOLIO_1": {
            "client_id": "CHILD_CLIENT_ID_1",
            "access_token": "encrypted_access_token",
            "multiplier": 1.0,
            "enabled": "Y"
        },
        "PORTFOLIO_2": {
            "client_id": "CHILD_CLIENT_ID_2", 
            "access_token": "encrypted_access_token",
            "multiplier": 0.5,
            "enabled": "Y"
        }
    },
    "DONOTPROCESSPROD": ["BO", "CO"]
}
```

### Advanced Settings

- **`multiplier`**: Controls position sizing (1.0 = same, 0.5 = half, 2.0 = double)
- **`enabled`**: "Y" to activate account, "N" to disable
- **`DONOTPROCESSPROD`**: Product types to exclude from copying

## 🔧 API Integration

### Supported Operations

| Operation | Master Account | Child Accounts |
|-----------|----------------|----------------|
| Place Order | ✅ Monitored | ✅ Replicated |
| Modify Order | ✅ Detected | ✅ Updated |
| Cancel Order | ✅ Tracked | ✅ Cancelled |
| Margin Check | ✅ Real-time | ✅ Real-time |

### Supported Order Types

- ✅ **MARKET** - Market orders
- ✅ **LIMIT** - Limit orders  
- ✅ **STOP_LOSS** - Stop loss orders
- ✅ **STOP_LOSS_MARKET** - Stop loss market orders

### Supported Product Types

- ✅ **CNC** - Cash and Carry
- ✅ **INTRA** - Intraday
- ✅ **MARGIN** - Margin trading
- ❌ **BO/CO** - Bracket/Cover orders (configurable)

## 📈 Benefits

### For Fund Managers
- **Scale Operations**: Manage multiple client accounts efficiently
- **Risk Management**: Individual multipliers for different risk profiles
- **Compliance**: Detailed logging for regulatory requirements
- **Cost Effective**: Reduce manual order placement time

### For Family Offices  
- **Centralized Trading**: One strategy, multiple family accounts
- **Proportional Allocation**: Custom sizing per family member
- **Automated Execution**: No manual intervention required

### For Individual Traders
- **Account Segregation**: Separate different strategies
- **Position Sizing**: Different risk levels per account
- **Backup Trading**: Continue trading if one account faces issues

## 🔒 Security Features

- 🔐 **Encrypted Storage** - All access tokens encrypted with Fernet
- 🔑 **Environment Variables** - Encryption keys stored securely  
- 🚫 **No Plain Text** - Zero sensitive data in plain text
- 📝 **Audit Trail** - Complete logging of all activities
- 🛡️ **Input Validation** - Comprehensive parameter checking

## 📊 Monitoring & Analytics

### Real-time Metrics
- Order execution status
- Account margin utilization  
- Success/failure rates
- Latency measurements

### Log Analysis
```bash
# View recent activity
tail -f logcopytrade.log

# Search for errors
grep "ERROR" logcopytrade.log

# Monitor specific account
grep "CLIENT123" logcopytrade.log
```

## 🚨 Risk Management

### Built-in Safeguards
- **Margin Checks** - Validates available funds before order placement
- **Product Filtering** - Exclude high-risk product types
- **Error Handling** - Graceful failure handling without system crash
- **Order Validation** - Verifies all parameters before execution

### Recommended Practices
- ⚠️ **Start Small** - Test with minimal quantities
- 📊 **Monitor Margins** - Ensure sufficient funds in all accounts
- 🔍 **Check Logs** - Regular log monitoring for issues
- 🛑 **Emergency Stop** - Keep manual override capability

## 🎯 Use Cases

### Portfolio Management
```python
# Example: Managing 3 risk profiles
CONSERVATIVE = {"multiplier": 0.3}  # 30% allocation
MODERATE = {"multiplier": 0.6}      # 60% allocation  
AGGRESSIVE = {"multiplier": 1.0}    # 100% allocation
```

### Strategy Testing
```python
# Example: A/B testing different position sizes
STRATEGY_A = {"multiplier": 1.0}    # Full position
STRATEGY_B = {"multiplier": 0.5}    # Half position
```

## 🛠️ Development

### Project Structure
```
dhan-copy-trading/
├── dhan_copytrader.py      # Main trading engine
├── encrypt_token.py        # Token encryption utility
├── config.json            # Account configuration (not tracked)
├── configTemplate.json    # Configuration template
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not tracked)
├── logs/                  # Log files directory
└── README.md              # This file
```

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📞 Support

### Documentation
- 📖 **[Setup Guide](SETUP.md)** - Detailed installation instructions
- 🔧 **[Configuration Guide](CONFIG.md)** - Advanced configuration options
- 🚨 **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

### Community
- 💬 **[Discussions](../../discussions)** - Ask questions and share experiences
- 🐛 **[Issues](../../issues)** - Report bugs and request features
- 📧 **Email Support** - [your-email@domain.com](mailto:your-email@domain.com)

### Resources
- 📚 **[Dhan API Documentation](https://dhanhq.co/docs/v2/)**
- 🐍 **[DhanHQ Python SDK](https://github.com/dhan-oss/DhanHQ-py)**
- 📈 **[Trading Best Practices](https://github.com/yourusername/trading-best-practices)**

## ⚖️ Legal & Compliance

### Disclaimer
- **Educational Purpose**: This software is primarily for educational and research purposes
- **Trading Risks**: Automated trading involves significant financial risks
- **User Responsibility**: Users are solely responsible for their trading decisions
- **No Warranty**: Software provided "as-is" without any warranty
- **Regulatory Compliance**: Ensure compliance with local trading regulations

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/dhan-copy-trading&type=Date)](https://star-history.com/#yourusername/dhan-copy-trading&Date)

---

**⭐ If this project helped you, please give it a star!**

**🔄 Share with fellow traders who might benefit from automated copy trading**

**💡 Have ideas for improvements? Open an issue or submit a PR!**
