from flask import Flask
import secrets
import string
import redis
from datetime import timedelta

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class OTCManager:
    def __init__(self, expiry_minutes=30):
        self.expiry = timedelta(minutes=expiry_minutes)
        
    def generate_otc(self, length=8):
        
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(length)) # Génération d'un code alphanumérique
        
        # stockage dans redis 
        redis_client.setex(
            f"otc:{code}",
            self.expiry,
            "valid"
        )
        
        return code
    
    def verify_otc(self, code):
        key = f"otc:{code}"
        is_valid = redis_client.get(key)
        if is_valid:
            redis_client.delete(key)
            return True
        return False
    

@app.route('/generate-otc', methods=['POST'])
def generate_otc():
    otc_manager = OTCManager()
    otc = otc_manager.generate_otc()
    return {'otc': otc}