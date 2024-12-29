import express from 'express';
import PresenceController from './controllers/PresenceController.js';

export const router = express.Router();

router.get('/', (req, res) => {
    const presenceData = PresenceController.getPresenceData();

    const formattedData = Array.isArray(presenceData) ? presenceData : [presenceData];

    res.render('index', { presenceData: formattedData });
});
