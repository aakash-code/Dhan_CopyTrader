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
