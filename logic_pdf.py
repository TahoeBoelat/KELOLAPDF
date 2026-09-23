from pypdf import PdfReader, PdfWriter
from docx2pdf import convert
from PIL import Image
import os
import io
import fitz
import qrcode

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
    total = len(reader.pages)
    if halaman_pilihan < 1 or halaman_pilihan > total:
        raise ValueError(f"Nomor halaman harus antara 1 dan {total}")
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
def kompres_pdf(path_input, path_output, kualitas=60, strip_metadata=False):
    doc = None
    pdf_baru = None
    try:
        # Membuka dokumen
        doc = fitz.open(path_input)
        # Membuat wadah dokumen PDF kosong yang baru
        pdf_baru = fitz.open()

        for page_num in range(len(doc)):
            # Memuat halaman
            page = doc.load_page(page_num)
            # Render halaman ke gambar (Pixmap)
            pix = page.get_pixmap(alpha=False)
            # Konversi Pixmap ke objek Pillow Image untuk kompresi JPEG
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Menggunakan BytesIO agar pemrosesan gambar tetap di RAM
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="JPEG", quality=kualitas, optimize=True)
            img_buffer.seek(0)

            # Konversi bytes JPEG menjadi satu halaman PDF utuh
            page_baru = pdf_baru.new_page(width=img.width, height=img.height)

            # Memasukan halaman terkompresi ke PDF baru
            rect = fitz.Rect(0, 0, img.width, img.height)
            page_baru.insert_image(rect, stream=img_buffer.getvalue())
        
        # Metadata Stripping
        if strip_metadata:
            # Metadata standar yang sering menyimpan info sensitif
            sanitized_metadata = {
                "author": "",
                "creator": "Kelola PDF Open Source",
                "producer": "Kelola PDF",
                "title": "",
                "subject": "",
                "keywords": "",
                "creationDate": "",
                "modDate": ""
            }
            pdf_baru.set_metadata(sanitized_metadata)
        pdf_baru.save(path_output, garbage=4, deflate=True)
        return True
    
    except Exception as e:
        print(f"Error pada fungsi kompres_pdf: {e}")
        return False
    finally:
        if doc is not None:
            doc.close()
        if pdf_baru is not None:
            pdf_baru.close()

# Fungsi untuk Metadata exposure
def hapus_meta_data_pdf(path_input, path_output):
    doc = None
    try:
        doc = fitz.open(path_input)
        # Pendifinisian metadata yang kosong menggunakan dictionary
        empty_metadata = {
            "author": "",
            "creator": "Kelola PDF Open Source",
            "producer": "Kelola PDF",
            "title": "",
            "subject": "",
            "keywords": "",
            "creationDate": "",
            "modDate": ""
        }
        # Memasukan metadata baru ke dokumen
        doc.set_metadata(empty_metadata)
        # Menghapus metadata lama
        doc.del_xml_metadata()
        # Simpan dengan membersihkan garbage collection
        doc.save(path_output, garbage=4, deflate=True)
        return True
    except Exception as e:
        print(f"Error saat stripping metadata: {e}")
        return False
    finally:
        if doc is not None:
            doc.close()

# Fungsi untuk QR Code Generator
def buat_qr_code(data):
    # Mengembalikan objek image (pillow) dari teks atau url yang diberikan
    qr = qrcode.QRCode (
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    return img.convert("RGB")

# Fungsi untuk menyimpan objek image qr ke file sesuai format
def simpan_qr_code(img, path_output, format_file):
    if format_file  == "JPEG":
        img.save(path_output, "JPEG", quality=95)
    else:
        img.save(path_output, format_file)