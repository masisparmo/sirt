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

## Rencana Jangka Panjang (Opsional)
Jika jumlah RT sudah sangat banyak, mengedit `index.html` setiap kali ada pendaftaran mungkin merepotkan. Solusinya:
1.  Buat satu Google Sheet khusus milik Anda (Admin Pusat) yang berisi 2 kolom: `ID_RT` dan `URL_GAS`.
2.  Buat script JSON API sederhana untuk Sheet tersebut.
3.  Ubah kode di `index.html` (fungsi `fetchMasterDirectory`) untuk mengambil data dari JSON API Anda, bukan dari variabel `MOCK_MASTER_DIR`.
