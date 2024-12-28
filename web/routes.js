import express from 'express';
import PresenceController from './controllers/PresenceController.js';

export const router = express.Router();

router.get('/', (req, res) => {
    // Fetch the latest presence data
    const presenceData = PresenceController.getPresenceData();

    // Ensure data is in an array format for Handlebars
    const formattedData = Array.isArray(presenceData) ? presenceData : [presenceData];

    // Render the template with the presence data
    res.render('index', { presenceData: formattedData });
});
