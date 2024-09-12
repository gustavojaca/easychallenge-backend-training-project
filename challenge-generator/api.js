import express from 'express';
import { generateChallenge } from './challenge-builder.js';
import { CONFIG } from './config.js';

const app = express();

app.use(express.json());

app.get('/challenge', (req, res) => {
    const challenge = generateChallenge();
    if (CONFIG.SLOW_MODE_ENABLED) {
        setTimeout(() => res.send(challenge), CONFIG.SLOW_MODE_TIMER);
    } else {
        res.send(challenge);
    }
});

app.listen(CONFIG.API_PORT, () => {
    console.log(`challenge-generator listening on port ${CONFIG.API_PORT}`);
});
