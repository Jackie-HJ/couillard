import { readable, derived, writable, get } from 'svelte/store';

import getData from './getData';
import { type PanelData } from './getData';

export const panelName = writable("all");

export const dbData = readable(getData());

export const LBS_CO2_PER_KWH = 1.52;
export const DOLLARS_SAVED_PER_KWH = 0.10;

const TOTALS_PANEL_WHITELIST = null;

function calcTotal(data: { [key: string]: PanelData }, panelFilter: string) {
    let total = 0;
    for (const [panelName, xy] of Object.entries(data)) {
        if (TOTALS_PANEL_WHITELIST !== null) {
            if (!TOTALS_PANEL_WHITELIST.includes(panelName)) {
                continue;
            }
        }
        if((panelFilter === "all") || panelFilter == panelName) {
            total += (+xy.old_data) || 0;
            for (const output of xy.y) {
                total += (+output) || 0;
            }
        }
    }
    return total;
}

//export const totalData = derived(dbData, promise => promise.then(data => calcTotal(data, get(selectedPanelStore))));
export const totalData = derived(
    [dbData, panelName], 
    async ([$dbData, $panelName]) => {
       return calcTotal(await $dbData, $panelName);
    }
);

export const readyToAnimate = writable(false);
