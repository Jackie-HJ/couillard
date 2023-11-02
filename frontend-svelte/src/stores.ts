import { readable, derived } from 'svelte/store';

import getData from './getData';
import { type PanelData } from './getData';

export const dbData = readable(await getData());

const LBS_CO2_PER_KWH = 1.52;
const DOLLARS_SAVED_PER_KWH = 0.10;

function calcTotal(data: { [key: string]: PanelData }) {
    let total = 0;
    for (const [_panelName, xy] of Object.entries(data)) {
        for (const output of xy.y) {
            total += output;
        }
    }
    return {
        original: total,
        derived: [
            // conversion factor, unit, show description
            [0.10, "$Saved",       true],
            [1.52, "lbs CO2 Saved", true],
            [1,    "kWh Generated", false],
        ],
    };
}

export const totalData = derived(dbData, calcTotal);
