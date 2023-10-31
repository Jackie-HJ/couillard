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

const DATE_PATTERNS = {
    "__default__": "MM-DD-YYYY",
};

interface PanelData {
    readonly name: string;
    readonly dates: readonly Date[];
    readonly outputs: readonly number[];
}

export default async function getData() {
    const app = initializeApp(firebaseConfig);
    let db = getFirestore(app);
    let col = collection(db, "Solar Arrays");
    let panelDataObjs = await assemblePanelDataObjects(col);
    console.log(panelDataObjs);
    return [1, 2, 2, 4];
};

function basename(path: string): string {
    for (let i = path.length - 1; i >= 0; i--) {
        if (path[i] === "/") {
            return path.slice(i + 1);
        }
    }
    return undefined as any;
}

function parseGenericDate(date: string, pattern: string): Date {
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
    );
}

function parseDateFromDb(date: string, panelName: string): Date {
    return parseGenericDate(date, DATE_PATTERNS[panelName] || DATE_PATTERNS["__default__"]);
}

async function assemblePanelDataObjects(
    col: CollectionReference<DocumentData, DocumentData>
): Promise<readonly PanelData[]> {
    let panelDataObjs: PanelData[] = [];
    (await getDocs(col)).forEach(async panelDoc => {
        let panelName = panelDoc.get("name");
        let outputCol = collection(panelDoc.ref, "Output");
        let unsortedYears = Object.create(null);
        (await getDocs(outputCol)).forEach(async outputDoc => {
            let year = basename(outputDoc.ref.path); // kinda hacky but oh well
            unsortedYears[year] = Object.entries(outputDoc.data()["Output"]);
        });
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
        let everything = [];
        for (let i of theYears) {
            everything.push(...unsortedYears[i]);
        }
        console.log(everything);
    });
    return panelDataObjs;
}