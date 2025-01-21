const express = require('express')
const { Sequelize, Model, DataTypes } = require('sequelize');
const { v4: uuidv4 } = require('uuid');

const sequelize = new Sequelize('postgres://user:password@localhost:5432/dbname');


class OneTimeLink extends Model{}
OneTimeLink.init({
    token : {
        type: DataTypes.STRING?
        primaryKey : true
    },
    userId : DataTypes.STRING,
    expiry: DataTypes.DATE,
    used: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    }
}, { sequelize });


class OTLManager{
    constructor(baseUrl, expiryHours = 24) {
        this.baseUrl = baseUrl;
        this.expiryHours = expiryHours;
    }

    async generateOTL(userId){
        const token = uuidv4();
        const expiry = new Date();
        expiry.setHours(expiry.getHours() + this.expiryHours);
        
        await OneTimeLink.create({
            token,
            userId,
            expiry
        });

        return `${this.baseUrl}/reset-password/${token}`;
    }

    async verifyOTL(token) {
        const otl = await OneTimeLink.findOne({
            where: {
                token,
                used : false,
                expiry : {
                    [Sequelize.Op.gt]: new Date()
                }
            }
        });

        if (otl) {
             otl.used = true;
             await otl.save();
             return otl.userId;
        }
        return null;
    }
}