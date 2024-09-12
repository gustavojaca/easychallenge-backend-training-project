import { CONFIG } from './config.js';

export const preloadChallenges = async (cache, preoadSize) => {
    console.log(`Preloading ${preoadSize} challenges`);
    const promises = [];
    for (let i = 0; i < preoadSize; i++) {
        const promise = fetch(`${CONFIG.CHALLENGE_GENERATOR_API_URI}/challenge`)
            .then(async (res) => {
                const data = await res.json();
                cache.put(data.challenge, data.solution);
            })
            .catch(console.error);
        promises.push(promise);
    }
    await Promise.all(promises);
};
