# Panduan Admin Pusat / Pemilik Aplikasi

Dokumen ini ditujukan untuk pemilik aplikasi (`https://sirt.isparmo.com`) dalam mengelola pendaftaran RT baru.

## Konsep Multi-Tenant (Banyak RT)
Aplikasi ini dirancang agar satu halaman web (`index.html`) bisa digunakan oleh banyak RT berbeda. Setiap RT memiliki:
1.  **Database Sendiri** (Google Spreadsheet + Apps Script milik mereka sendiri).
2.  **ID Unik** (misal: `rt08-royal2`).

Warga mengakses aplikasi spesifik RT mereka menggunakan parameter URL:
`https://sirt.isparmo.com/?id=rt08-royal2`

---

## Cara Mendaftarkan RT Baru (Onboarding)

Jika ada Ketua RT (misal: Pak Budi dari RT 08 Taman Royal 2) yang menghubungi Anda via WhatsApp untuk menggunakan aplikasi ini:

### 1. Minta Data dari RT
Pastikan Ketua RT sudah mengikuti panduan di halaman "Panduan & Code" aplikasi, yaitu:
*   Membuat Google Sheet.
*   Memasang script backend (Copy-Paste kode).
*   Melakukan Deploy Web App dan menyalin URL-nya.

**Data yang Anda butuhkan dari mereka:**
*   Nama RT/Perumahan (misal: RT 08 Taman Royal 2).
*   URL Web App Google Script mereka (harus berawalan `https://script.google.com/macros/s/...`).

### 2. Tentukan ID Unik
Buatlah ID singkat dan unik untuk RT tersebut. Gunakan huruf kecil, angka, dan tanda hubung saja (tanpa spasi).
*   Contoh: `rt08-royal2`

### 3. Update Master Directory
Saat ini, "Master Directory" masih bersifat **MOCK (Simulasi)** di dalam kode `index.html`.

**Untuk menambahkan RT baru:**
1.  Buka file `index.html` di repository GitHub Anda.
2.  Cari bagian `const MOCK_MASTER_DIR`.
3.  Tambahkan baris baru dengan format `"ID-RT": "URL-GAS",`. Pastikan ID ditulis dalam **HURUF KAPITAL** (karena kode akan menormalisasinya).

**Contoh Kode:**
```javascript
const MOCK_MASTER_DIR = {
    "RT01-DEMO": "https://script.google.com/macros/s/AKfycbw13I-yATL4RDK0KEdsitex54dAQ9Q9HTnDEQWs4HB_d6fO2_bp_LHilb5kIwz4TITP/exec",
    // Tambahkan RT baru di sini:
    "RT08-ROYAL2": "https://script.google.com/macros/s/AKfycb...URL_PUNYA_RT_08.../exec"
};
```
4.  Commit dan Push perubahan tersebut ke GitHub.
5.  Tunggu beberapa menit hingga GitHub Pages terupdate.

### 4. Berikan Link ke Ketua RT
Setelah update live, berikan link akses kepada Ketua RT:
`https://sirt.isparmo.com/?id=rt08-royal2`

Saat mereka atau warga membuka link tersebut:
1.  Aplikasi akan otomatis mendeteksi ID `rt08-royal2`.
2.  Aplikasi mencari URL Database yang sesuai di `MOCK_MASTER_DIR`.
3.  Aplikasi menyimpan konfigurasi tersebut di browser warga.
4.  Warga langsung melihat data RT 08 Taman Royal 2.

---

## Tutorial: Membuat Master Directory Otomatis (JSON API)

Jika Anda sudah memiliki banyak klien RT, mengedit file HTML setiap kali ada pendaftaran baru akan sangat merepotkan. Solusinya adalah membuat **Database Pusat** di Google Sheet milik Anda sendiri.

**Konsep:**
1.  Anda punya Google Sheet berisi daftar ID RT dan URL Database mereka.
2.  Anda membuat script sederhana (API) untuk membaca data tersebut.
3.  Web App (`index.html`) akan "bertanya" ke API Anda: *"Saya punya ID rt08-royal2, mana URL Database-nya?"*

### Langkah 1: Buat Master Sheet
1.  Buat Google Sheet baru di akun Google Anda (beri nama "Master SIRT").
2.  Isi baris pertama (Header):
    *   Kolom A1: `ID_RT`
    *   Kolom B1: `URL_GAS`
    *   Kolom C1: `Nama_RT` (Opsional, untuk catatan Anda)
3.  Isi data RT di baris berikutnya:
    *   A2: `RT08-ROYAL2`
    *   B2: `https://script.google.com/macros/s/...` (URL Backend RT tersebut)
    *   C2: `RT 08 Taman Royal 2`

### Langkah 2: Buat Script API Master
1.  Di Google Sheet tersebut, klik **Ekstensi > Apps Script**.
2.  Hapus kode yang ada, tempelkan kode berikut:

```javascript
function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  // Hapus header
  data.shift();

  var result = {};
  data.forEach(function(row) {
    var id = row[0].toString().toUpperCase().trim();
    var url = row[1];
    if(id && url) {
      result[id] = url;
    }
  });

  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3.  Klik **Simpan**.
4.  Klik **Terapkan (Deploy) > Deployment Baru**.
    *   Jenis: **Aplikasi Web**.
    *   Keterangan: "API Master v1".
    *   Yang memiliki akses: **Siapa saja (Anyone)**.
5.  Salin **URL Web App** yang Anda dapatkan (misal: `https://script.google.com/macros/s/XYZ.../exec`). Ini adalah **MASTER_API_URL** Anda.

### Langkah 3: Update `index.html`
Sekarang, ubah kode di `index.html` agar tidak lagi menggunakan `MOCK_MASTER_DIR`, tapi mengambil data dari Master Sheet Anda.

Cari fungsi `fetchMasterDirectory(id)` dan ubah menjadi seperti ini:

```javascript
// Ganti URL ini dengan URL Web App Master Anda dari Langkah 2
const MASTER_API_URL = "https://script.google.com/macros/s/XYZ.../exec";

async function fetchMasterDirectory(id) {
    try {
        // Ambil semua data ID dari Master Sheet
        const response = await fetch(MASTER_API_URL);
        const directory = await response.json();

        // Cari ID yang cocok
        const normalizedId = id.toUpperCase().trim();
        if (directory[normalizedId]) {
            return directory[normalizedId];
        }
    } catch (e) {
        console.error("Gagal mengambil Master Directory", e);
    }
    return null; // ID tidak ditemukan
}
```

**Selesai!**
Sekarang, setiap kali ada RT baru:
1.  Cukup tambahkan baris baru di Google Sheet "Master SIRT" Anda.
2.  Tidak perlu edit kode HTML atau deploy ulang website.
3.  ID baru akan langsung aktif.
