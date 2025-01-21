const express = require('express');
const crypto = require('crypto');
const Redis = require('ioredis');
const redis = new Redis();

class OTCManager {
    constructor(expiryMinutes = 30) {
        this.expirySeconds = expiryMinutes * 60;
    }

    generateOTC(length = 8) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const otc = Array.from(crypto.randomFillSync(new Uint32Array(length)))
                .map(x => chars[x % chars.length])
                .join('');

        // stockage dans redis
        redis.setex(`otc:${otc}`, this.expirySeconds, 'valid');
        return otc;
    }

    async verifyOTC(code){
        const key = `otc:${code}`;
        const isValid = await redis.get(key);
        if(isValid) {
             await redis.del(key);
             return true;
        }
        return false;
    }
}