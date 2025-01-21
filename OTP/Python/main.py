from flask import Flask, request #importation des modules Flask et request
import pyotp
from datetime import datetime

app = Flask(__name__) 

class OTPManager:
    def __init__(self):
        # Génération d'une clé secrète unique
        self.secret = pyotp.random_base32()
        # Création d'un générateur TOTP avec une durée de 30 secondes
        self.totp = pyotp.TOTP(self.secret, interval=30)
        
    def generate_otp(self):
        return self.totp.now()
    
    def verify_otp(self, otp):
        return self.totp.verify(otp)
    

@app.route('/generate-otp', methods=['POST'])
def generate_otp():
    otp_manager = OTPManager()
    otp = otp_manager.generate_otp()
    
    # Ici, vous enverriez normalement l'OTP par SMS
    return {"otp" : otp}