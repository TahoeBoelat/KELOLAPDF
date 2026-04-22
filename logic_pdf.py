from pypdf import PdfReader, PdfWriter
from docx2pdf import convert
from PIL import Image
import os
import io
import fitz

# Fungsi untuk mengkonversi multiple docx format ke PDF
def batch_word_ke_pdf(daftar_docx, folder_tujuan):
    for docx_path in daftar_docx:
        # Mengambil nama file asli
        nama_asli = os.path.basename(docx_path)
        # Mengganti ekstensi menjadi pdf
        nama_pdf = os.path.splitext(nama_asli)[0] + ".pdf"
        # Gabung folder tujuan dengan nama file baru
        path_output = os.path.join(folder_tujuan, nama_pdf)
        # Konversi
        convert(docx_path, path_output) 

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

# Fungsi untuk konversi gambar ke PDF
def image_ke_pdf(daftar_gambar, path_output):
    """Menggabungkan daftar path gambar menjadi satu file PDF"""
    list_image = []

    for img_path in daftar_gambar:
        img = Image.open(img_path)
        # Variabel untuk mengkonversi RGBA ke RGB
        img_rgb = img.convert('RGB')
        list_image.append(img_rgb)
    
    if list_image:
        image_pertama = list_image[0]
        sisanya = list_image[1:]

        image_pertama.save(
            path_output,
            "PDF",
            save_all = True,
            append_image=sisanya
        )

# Fungsi untuk mengkompress PDF
def kompres_pdf(path_input, path_output, kualitas=60):
    """Mengecilkan ukuran file PDF dengan mengompres konten internal"""
    try:
        doc = fitz.open(path_input)
        pdf_baru = fitz.open()

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            pix = page.get_pixmap(alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            img_buffer = io.BytesIO()
            img.save(img_buffer, format="JPEG", quality=kualitas, optimize=True)
            img_buffer.seek(0)
            
            rect = page.rect
            new_page = pdf_baru.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_buffer.getvalue())

            pdf_baru.save(path_output, garbage=4, deflate=True)
            pdf_baru.close()
            doc.close()

            return True
    except Exception as e:
        print(f"Detail Error: {e}")
        return False