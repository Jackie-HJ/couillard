import { readable, derived } from 'svelte/store';

import getData from './getData';
import { type PanelData } from './getData';

export const dbData = readable(getData());

const LBS_CO2_PER_KWH = 1.52;
const DOLLARS_SAVED_PER_KWH = 0.10;

const TOTALS_PANEL_WHITELIST = ["Kelly Lane"];

function calcTotal(data: { [key: string]: PanelData }) {
    let total = 0;
    for (const [panelName, xy] of Object.entries(data)) {
        if (TOTALS_PANEL_WHITELIST !== null) {
            if (!TOTALS_PANEL_WHITELIST.includes(panelName)) {
                continue;
            }
        }
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

export const totalData = derived(dbData, promise => promise.then(calcTotal));
