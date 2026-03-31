// db.js: Simple IndexedDB wrapper for SIRT Pintar
const DB_NAME = "SIRTPintarDB";
const STORE_CONFIG = "config"; // For GAS URL, app title, etc.
const DB_VERSION = 1;

let dbInstance = null;

function openDB() {
    return new Promise((resolve, reject) => {
        if (dbInstance) return resolve(dbInstance);
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains(STORE_CONFIG)) {
                db.createObjectStore(STORE_CONFIG, { keyPath: "key" });
            }
        };
        request.onsuccess = (e) => {
            dbInstance = e.target.result;
            resolve(dbInstance);
        };
        request.onerror = (e) => reject("DB Error: " + e.target.error);
    });
}

async function saveConfig(key, value) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_CONFIG, "readwrite");
        const store = tx.objectStore(STORE_CONFIG);
        store.put({ key, value });
        tx.oncomplete = () => resolve(true);
        tx.onerror = () => reject(tx.error);
    });
}

async function getConfig(key) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_CONFIG, "readonly");
        const store = tx.objectStore(STORE_CONFIG);
        const req = store.get(key);
        req.onsuccess = () => resolve(req.result ? req.result.value : null);
        req.onerror = () => reject(req.error);
    });
}

async function getAllConfig() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_CONFIG, "readonly");
        const store = tx.objectStore(STORE_CONFIG);
        const req = store.getAll();
        req.onsuccess = () => {
            const result = {};
            req.result.forEach(item => result[item.key] = item.value);
            resolve(result);
        };
        req.onerror = () => reject(req.error);
    });
}

async function clearDB() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_CONFIG, "readwrite");
        const store = tx.objectStore(STORE_CONFIG);
        store.clear();
        tx.oncomplete = () => resolve(true);
        tx.onerror = () => reject(tx.error);
    });
}

async function exportData() {
    const data = await getAllConfig();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");

    // Generate filename based on config or default
    const kelurahan = data.kelurahan || "kelurahan";
    const rt = data.rt || "rt";
    const filename = `${rt}_${kelurahan}.sirt`.replace(/\s+/g, '_').toLowerCase();

    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function importData(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const data = JSON.parse(e.target.result);
                // Validate basic structure if needed
                for (const [key, value] of Object.entries(data)) {
                    await saveConfig(key, value);
                }
                resolve(true);
            } catch (err) {
                reject("Invalid file format");
            }
        };
        reader.onerror = () => reject("File read error");
        reader.readAsText(file);
    });
}
