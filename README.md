# KELOLAPDF - OFFLINE TOOL
Aplikasi desktop berbasis Python untuk mengelola file PDF secara cepat dan offline

## FITUR UTAMA
* **GABUNG PDF**
* **POTONG PDF**
* **WORD to PDF**

## RIWAYAT PENGEMBANGAN (CHANGELOG)

### v1.5-beta - 2026-04-21
- **Fitur Baru:** Modul "PDF Compressor" (Tahap Awal) untuk mengecilkan ukuran file PDF.
- **Fitur Baru (UX):** Tombol **"Reset Daftar"** di setiap tab untuk mengosongkan antrean dalam satu klik.
- **Fitur Baru (Shortcut):** Implementasi binding keyboard global:
    - `Ctrl + A`: Pilih semua file di daftar aktif.
    - `Delete`: Hapus massal file terpilih (dengan algoritma *reverse index*).
    - `Ctrl + R`: Shortcut cepat untuk fungsi Reset.
- **Perbaikan UI:** Penambahan **Scrollbar** di semua Listbox untuk navigasi file yang lebih baik.
- **Perbaikan Bug:** Menangani error `TypeError` pada pemilihan file tunggal untuk kompresi.

### [v1.4] - 2026-04-16
- **Fitur Baru:** Implementasi fitur konversi gambar ke PDF
- **Perbaikan Bug:** Memperbaiki masalah seleksi Listbox menggunakan `exportselection=False` sehingga tombol hapus bekerja lebih stabil.
- **Perbaikan Bug:** Sinkronisasi penulisan biner pada library Pillow untuk menghindari error `write() argument must be str`.

### [v1.3] - 2026-04-14
- **Fitur Baru:** Implementasi Batch Processing untuk Word-to-PDF (Konversi massal).
- **Kompatibilitas:** Mendukung format legacy `.doc` selain `.docx`.
- **UX:** Sinkronisasi antarmuka antartab menggunakan sistem Listbox dan Folder Output.
- **Bug Fix:** Memperbaiki error atribut pada fungsi `update_idletasks`.

### [v1.3] - 2026-04-14
- **Fitur Baru:** Penambahan tombol "Hapus file terpilih" pada Tab Merge
- **UX:** Penambahan pesan peringatan (messagebox) jika user menghapus tanpa memilih file

### [v1.2] - 2026-04-09
- **Fitur Baru:** Implementasi konversi Word (.docx) ke PDF menggunakan library `docx2pdf`.
- **UI:** Migrasi ke sistem navigasi **Tab (Notebook)** untuk antarmuka yang lebih bersih.
- **Optimasi:** Penambahan `update_idletasks` untuk menjaga responsivitas UI saat proses berat.

### [v1.1] - 2026-04-08
- **Fitur Baru:** Penambahan fitur **Potong PDF (Split)** per halaman tunggal.
- **UI:** Perbaikan manajemen tata letak menggunakan `Frame` dan `Grid`.
- **Version Control:** Inisialisasi manajemen fitur berbasis branch Git.

### [v1.0] - 2026-04-07
- **Rilis Awal:** Peluncuran fitur utama **Penggabungan PDF (Merge)**.

## PANDUAN INSTALASI
1. **Siapkan Environment:** `python -m venv venv`
2. **Aktifkan:** `.\venv\Scripts\activate`
3. **Instal Library:** `pip install -r requirements.txt`
4. **Jalankan:** `python main.py`

## TEKNOLOGI
* Python 3.11+, Tkinter, PyPDF, Docx2pdf.

## LICENSE
MIT License.