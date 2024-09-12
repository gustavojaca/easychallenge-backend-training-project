import { randomBytes, createHash } from 'node:crypto';
import { v5 as uuidv5 } from 'uuid';

import { CONFIG } from './config.js';

export const generateChallenge = () => {
    const challenge = generateChallengeStr();
    const solution = resolveChallenge(challenge);
    return {
        challenge,
        solution,
    };
};

const generateChallengeStr = () => {
    return randomBytes(CONFIG.CHALLENGE_LENGTH).toString('hex');
};

const resolveChallenge = (challenge) => {
    const challengeUUID = uuidv5(challenge, CONFIG.SOLUTION_NAMESPACE);
    return createHash(CONFIG.SOLUTION_HASHING_ALGORITHM).update(challengeUUID).digest('hex');
};
