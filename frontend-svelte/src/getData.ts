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
            unsortedYears[k].sort(
                (a: [string, number], b: [string, number]) => Math.sign(
                    (new Date(a[0]) as any) - (new Date(a[1]) as any)
                )
            );
            for (let i of unsortedYears[k]) {
                console.log(i);
            }
        }
    });
    return panelDataObjs;
}
