import { initializeApp } from "firebase/app";
import type { CollectionReference } from "firebase/firestore";
import {
    collection, type DocumentData, type Firestore, getDocs, getFirestore
} from "firebase/firestore/lite";

const firebaseConfig = {
    apiKey: "AIzaSyAaZSAsa9-7O_ffxqPPVbUsMZ13eDXH7TU",
    authDomain: "helios-9d435.firebaseapp.com",
    projectId: "helios-9d435",
    storageBucket: "helios-9d435.appspot.com",
    messagingSenderId: "768984637940",
    appId: "1:768984637940:web:90dee43f1fc4aeafbdd9a1",
    measurementId: "G-4FBRG6M1VB"
};

// { <panelName>: [<date-format>, <source-timezone-offset>] }
const DATE_PATTERNS = {
    "__default__": ["MM-DD-YYYY", 5],
};

interface PanelData {
    readonly x: readonly Date[];
    readonly y: readonly number[];
}

export default async function getData(): Promise<{ [key: string]: PanelData }> {
    const app = initializeApp(firebaseConfig);
    let db = getFirestore(app);
    let col = collection(db, "Solar Arrays");
    let panelDataObjs = await assemblePanelDataObjects(col);
    return panelDataObjs;
};

function basename(path: string): string | undefined {
    for (let i = path.length - 1; i >= 0; i--) {
        if (path[i] === "/") {
            return path.slice(i + 1);
        }
    }
}

function parseGenericDate(date: string, patterns: [string, number]): Date {
    let [pattern, sourceTimezoneOffsetHrs ] = patterns;
    let sourceTimezoneOffset = sourceTimezoneOffsetHrs * 60;
    let cursor = 0;
    let got = { month: '', day: '', year: '' };
    for (const tok of pattern) {
        let ch = date[cursor++];
        switch (tok) {
            case 'Y': case 'y':
                got.year += ch;
                break;
            case 'M': case 'm':
                got.month += ch;
                break;
            case 'D': case 'd':
                got.day += ch;
                break;
            default:
                if (ch !== tok) {
                    console.warn(`In parseGenericDate, Pattern ${pattern} failed to match ${date}.`);   
                }
        }
    }
    if (cursor !== date.length) {
        console.warn(`In parseGenericDate, Pattern ${pattern} missing end of ${date}.`);   
    }
    return new Date(
        parseInt(got.year),
        parseInt(got.month) - 1, // Months start at zero for some reason
        parseInt(got.day),
        0, // Nothing special for hours
        (new Date()).getTimezoneOffset() - sourceTimezoneOffset, // TZ offsets in minutes
    );
}

function parseDateFromDb(date: string, panelName: string): Date {
    return parseGenericDate(
        date, DATE_PATTERNS[panelName] || DATE_PATTERNS["__default__"]);
}

async function asyncForEach(x: { forEach: any }, fn: (_: any) => Promise<any>): Promise<any> {
    let promises: Promise<any>[] = [];
    x.forEach(async y => {
        promises.push(fn(y));
    });
    return Promise.all(promises);
}

async function assemblePanelDataObjects(
    col: CollectionReference<DocumentData, DocumentData>
): Promise<{ [key: string]: PanelData }> {
    let panelDataObjs: { [key: string]: PanelData } = Object.create(null);
    await asyncForEach(await getDocs(col), (async panelDoc => {
        let panelName = panelDoc.get("name");
        let outputCol = collection(panelDoc.ref, "Output");
        let unsortedYears = Object.create(null);
        await asyncForEach(await getDocs(outputCol), (async outputDoc => {
            let year = basename(outputDoc.ref.path); // kinda hacky but oh well
            if (year === undefined) {
                console.warn('basename failed, year undefined');
                return;
            }
            unsortedYears[year] = Object.entries(outputDoc.data()["Output"]);
        }));
        for (let k in unsortedYears) {
            let sub = unsortedYears[k];
            for (let i = 0; i < sub.length; i++) {
                sub[i] = [
                    parseDateFromDb(sub[i][0], panelName),
                    sub[i][1],
                ];
            }
            unsortedYears[k].sort(
                (a: [string, number], b: [string, number]) => (
                    (a[0] as any) - (b[0] as any)
                )
            );
        }
        let theYears = Object.keys(unsortedYears);
        theYears.sort();
        let dates = [];
        let outputs = [];
        for (let i of theYears) {
            dates.push(...unsortedYears[i].map((x: [Date, number]) => x[0]));
            outputs.push(...unsortedYears[i].map((x: [Date, number]) => x[1]));
        }
        panelDataObjs[panelName] = {
            x: dates,
            y: outputs,
        } as const;
    }));
    return panelDataObjs;
}
