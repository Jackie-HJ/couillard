export const TOTALS_DERIVATIONS: [
    number, string, "expanded" | "simple" | "money" | "si", string, boolean
][] = [
    // conversion factor, unit, unit type, suffix (i.e. "Saved"), show description,
    [ 0.10, "",             "money",    "Saved",     true  ],
    [ 1.52, "lbs CO2",      "expanded", "Saved",     true  ],
    [ 1000, "Wh",           "si",       "Generated", false ],
];

export const FORMATTING_LOCALE: string = "en-US";
export const CURRENCY: string = "USD";
