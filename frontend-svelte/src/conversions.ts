export const TOTALS_DERIVATIONS: [
    number, string, "simple" | "money" | "si", boolean
][] = [
    // conversion factor, unit, unit type, show description,
    [ 0.10, "Saved",         "money",  true  ],
    [ 1.52, "lbs CO2 Saved", "simple", true  ],
    [ 1000, "Wh Generated",  "si",     false ],
];

export const FORMATTING_LOCALE: string = "en-US";
export const CURRENCY: string = "USD";
