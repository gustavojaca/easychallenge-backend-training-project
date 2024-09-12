import { loadApiKeys } from './api-keys-loader.js';
import { solveChallenge } from './challenge-solver.js';
import { CONFIG } from './config.js';
import * as url from 'node:url';
import { randChoice } from './utils.js';

export const runClient = async ({ apiKey = undefined, silent = false } = {}) => {
    let challenge;
    try {
        const response = await fetch(`${CONFIG.CLIENT_HANDLER_API_URI}/challenge`, {
            headers: apiKey
                ? {
                      'x-api-key': apiKey,
                  }
                : {},
        });
        const jsonResponse = await response.json();
        if (!response.ok) throw Error(jsonResponse.message);
        challenge = jsonResponse.challenge;
    } catch (error) {
        if (!silent) console.error(`Error when submitting challenge: ${error}`);
        return false;
    }

    if (!silent) console.log(`Challenge: ${challenge}`);

    const solution = solveChallenge(challenge);

    if (!silent) console.log(`Solution: ${solution}`);

    try {
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        };
        if (apiKey) headers['x-api-key'] = apiKey;
        const response = await fetch(`${CONFIG.CLIENT_HANDLER_API_URI}/challenge`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ challenge, solution }),
        });
        const jsonResponse = await response.json();
        if (!response.ok) throw Error(jsonResponse.message);
        if (!silent) console.error(`Challenge submitted. Result is: ${jsonResponse.correct ? 'CORRECT' : 'INCORRECT'}`);
        return jsonResponse.correct;
    } catch (error) {
        if (!silent) console.error(`Error when submitting challenge: ${error}`);
        return false;
    }
};

const main = () => {
    const apiKeys = loadApiKeys();
    const apiKey = randChoice(apiKeys);
    runClient({ apiKey: apiKey });
};

// If called as main
if (import.meta.url.startsWith('file:')) {
    const modulePath = url.fileURLToPath(import.meta.url);
    if (process.argv[1] === modulePath) {
        main();
    }
}
