const express = require('express');
const { authenticator } = require('otplib');
const app = express();

class OTPManager {
     constructor (){
          
        this.secret = authentificator.generateSecret(); // Génération d'une clé secrète
     }

     generateOTP() {
         return authentificator.generateOTP(this.secret); // Génration d'un code otp
     }

     verifyOTP(token){
         return authenticator.verify({ token, secret: this.secret});
     }
}


app.post('/generate-otp', (req, res) => {
      const otpManager = new OTPManager();
      const otp = otpManager.generateOTP();
      res.json({ otp });
})