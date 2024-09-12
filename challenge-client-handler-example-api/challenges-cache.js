export class ChallengesCache {
    #cache;

    constructor() {
        this.#cache = new Map();
    }

    put(challenge, solution) {
        this.#cache.set(challenge, solution);
    }

    get(challenge) {
        return this.#cache.get(challenge);
    }

    has(challenge) {
        return this.#cache.has(challenge);
    }

    getRandomChallenge() {
        const items = Array.from(this.#cache);
        return items[Math.floor(Math.random() * items.length)][0];
    }

    print() {
        const rows = [];
        this.#cache.forEach((value, key, map) => {
            rows.push({
                Challenges: key,
                Solutions: value,
            });
        });
        console.log('\nCache content:');
        console.table(rows);
    }
}
