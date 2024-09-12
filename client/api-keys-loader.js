import * as fs from 'node:fs';
import { CONFIG } from './config.js';

export const loadApiKeys = () => {
    const lines = fs.readFileSync(CONFIG.API_KEYS_TXT_FILE).toString().split('\n');
    return lines.filter((x) => !(x.startsWith('//') || x.length == 0));
};
