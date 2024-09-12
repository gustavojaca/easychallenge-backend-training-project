import { createHash } from 'node:crypto';
import { v5 as uuidv5 } from 'uuid';

import { CONFIG } from './config.js';

export const solveChallenge = (challenge) => {
    const challengeUUID = uuidv5(challenge, CONFIG.SOLUTION_NAMESPACE);
    return createHash(CONFIG.SOLUTION_HASHING_ALGORITHM).update(challengeUUID).digest('hex');
};
