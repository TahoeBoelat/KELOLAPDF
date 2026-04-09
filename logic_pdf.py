from pypdf import PdfReader, PdfWriter
from docx2pdf import convert
import os

# Fungsi untuk menggabungkan PDF
def gabung_pdf(daftar_file, nama_output):
    # Menyiapkan penulis PDF
    writer = PdfWriter()

    for path in daftar_file:
        # Membaca file PDF satu per satu
        reader = PdfReader(path)
        for halaman in reader.pages:
            writer.add_page(halaman)
    
    with open(nama_output, "wb") as f:
        writer.write(f)
    
    print(f"Berhasil disimpan sebagai: {nama_output}")

# Fungsi untuk memotong PDF
def potong_pdf(input_pdf, halaman_pilihan, nama_output):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    # Mengambil halaman berdasarkan index
    halaman = reader.pages[halaman_pilihan - 1]
    writer.add_page(halaman)

    with open(nama_output, "wb") as f:
        writer.write(f)
    
    print(f"Halaman {halaman_pilihan} berhasil dipotong ke: {nama_output}")

# Fungsi untuk konversi DOCX ke PDF
def word_ke_pdf(input_path, output_path):
    convert(input_path, output_path)