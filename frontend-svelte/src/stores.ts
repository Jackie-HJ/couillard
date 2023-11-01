import { readable } from 'svelte/store';

import getData from './getData';

export const dbData = readable(await getData());
