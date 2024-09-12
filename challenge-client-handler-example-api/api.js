import express from 'express';
import { CONFIG } from './config.js';
import { ChallengesCache } from './challenges-cache.js';
import { preloadChallenges } from './helpers.js';

const challengesCache = new ChallengesCache();

const app = express();

app.use(express.json());

app.use((req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    console.log('Api key', apiKey);
    // We are not validating api key yet
    if (!apiKey) {
        console.log('error');
        return res.status(401).json({ message: 'API key missing' });
    }
    next();
});

app.get('/challenge', (req, res) => {
    console.log(`Challenge requested`);
    res.send({
        challenge: challengesCache.getRandomChallenge(),
    });
});

app.post('/challenge', (req, res) => {
    const challenge = req.body?.challenge;
    const proposedSolution = req.body?.solution;
    console.log(`Challenge submition received: ${challenge}`);

    if (!challenge || !proposedSolution || !challengesCache.has(challenge)) {
        return res.send({ correct: false });
    }

    const solution = challengesCache.get(challenge);

    res.send({
        correct: challengesCache.get(challenge) === proposedSolution,
    });
});

app.listen(CONFIG.API_PORT, async () => {
    await preloadChallenges(challengesCache, CONFIG.PRELOAD_CACHE_SIZE);
    challengesCache.print();
    console.log(`challenge-generator listening on port ${CONFIG.API_PORT}`);
});
