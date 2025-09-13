import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables from .env
load_dotenv()

key = os.environ.get('key')
if key:
    mysecret = key.encode()
else:
    # Generate new key for first time
    mysecret = Fernet.generate_key()
    with open(".env", "a") as envf:
        envf.write(f"\nkey={mysecret.decode()}")
    print("New key generated and saved to .env")

f = Fernet(mysecret)
access_token = input("Enter Dhan access token to encrypt: ")

# Encrypt the access token
password = str(access_token).encode()
encrypted = f.encrypt(password)

print(f"Encrypted access token: {encrypted.decode()}")
print("\nUse this encrypted value in your config.json file")
print("To decrypt: use the deCryptPwd() function in the main script")
