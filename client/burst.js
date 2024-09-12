import { loadApiKeys } from './api-keys-loader.js';
import { runClient } from './client.js';
import { randChoice } from './utils.js';

const NUM_ITERATIONS = 1; // 1 iteration condiders scaling from 1 to MAX_BURST_MULTIPLIER to 1 back again
const MAX_BURST_MULTIPLIER = 25;
const BASE_CONCURRENT_REQUESTS = 100;

const BURST_OPERATIONS = {
    ADD: 'ADD',
    SUBSTRACT: 'SUBSTRACT',
};

const API_KEYS = loadApiKeys();

const summonClient = () => {
    return new Promise(async (resolve, reject) => {
        const success = await runClient({ silent: true, apiKey: randChoice(API_KEYS) });
        resolve({
            success,
        });
    });
};

const main = async () => {
    const stats = {
        totalSuccesses: 0,
        totalErrors: 0,
        errorsSinceLastBurst: 0,
    };

    let burstMultiplier = 1;
    let burstOperation = BURST_OPERATIONS.ADD;
    const totalIterations = NUM_ITERATIONS * MAX_BURST_MULTIPLIER * 2 - 1;

    for (let i = 0; i < totalIterations; i++) {
        const numRequests = BASE_CONCURRENT_REQUESTS * burstMultiplier;
        console.log(`\nStarting burst #${i + 1} with ${numRequests} requests (x${burstMultiplier} multipler)`);

        const requests = [];
        for (let i = 0; i < numRequests; i++) {
            requests.push(summonClient());
        }

        const resutls = await Promise.all(requests);

        stats.errorsSinceLastBurst = 0;
        for (const result of resutls) {
            if (result.success) {
                stats.totalSuccesses += 1;
            } else {
                stats.totalErrors += 1;
                stats.errorsSinceLastBurst += 1;
            }
        }

        console.table(stats);

        if (burstOperation === BURST_OPERATIONS.ADD) {
            burstMultiplier += 1;
        }
        if (burstOperation === BURST_OPERATIONS.SUBSTRACT) {
            burstMultiplier -= 1;
        }

        if (burstMultiplier >= MAX_BURST_MULTIPLIER) {
            burstOperation = BURST_OPERATIONS.SUBSTRACT;
        }
        if (burstMultiplier <= 1) {
            burstOperation = BURST_OPERATIONS.ADD;
        }
    }
};

main();
