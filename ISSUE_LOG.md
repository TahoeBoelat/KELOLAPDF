## [Known Issues / To-Do]
### Issue #002: Metadata Exposure
- **Deskriptsi:** Dokumen hasil olahan masih menyimpan metadata asli (author, created date, dll).
- **Rencana:** Melakukan implementasi Sanitization untuk menghapus semua metadata untuk privasi pengguna.


## [Resolved Issues]
### Issue #001: Ineffective Compression on Image-Heavy PDF
- **Deskripsi:** Fungsi `compress_content_streams()` saat ini hanya mengompres instruksi teks/objek. Pada PDF hasil scan (image-based), ukuran file tidak berkurang secara signifikan, bahkan bisa sedikit membengkak karena overhead struktur PDF baru.
- **Rencana Perbaikan:** Implementasi "Image Downsampling" menggunakan library `Pillow` untuk meresample gambar di dalam PDF ke DPI yang lebih rendah.
- **Status:** Closed (2026-04-24)