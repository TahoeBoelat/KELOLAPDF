# KELOLAPDF - OFFLINE TOOL
Aplikasi desktop berbasis Python untuk mengelola file PDF secara cepat dan offline

## FITUR UTAMA
* **GABUNG PDF**
* **POTONG PDF**
* **WORD to PDF**

## RIWAYAT PENGEMBANGAN (CHANGELOG)

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