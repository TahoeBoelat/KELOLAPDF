from logic_pdf import gabung_pdf, potong_pdf

def menu():
    print("====KELOLA PDF====")
    print("1. Gabung PDF")
    print("2. Potong PDF (Ambil 1 Halaman)")
    pilihan = input("Pilih menu (1/2): ")

    if pilihan == "1":
        files = ["Tes1.pdf", "Tes2.pdf"]
        gabung_pdf(files, "hasil_gabung_baru.pdf")
    elif pilihan == "2":
        halaman = int(input("Mau ambil halaman berapa? "))
        potong_pdf("Tes1.pdf", halaman, "halaman_terpotong.pdf")

if __name__ == "__main__":
    menu()