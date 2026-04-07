import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from logic_pdf import gabung_pdf

class PDFApp:
    # Inisialisasi antarmuka
    def __init__(self, root):
        self.root = root
        self.root.title("Kelola PDF - Offline")
        self.root.geometry("500x450")

        # Variabel untuk menyimpan daftar file yang dipilih
        self.files_terpilih = []

        # Variabel untuk button
        self.label = tk.Label(root, text="Daftar File PDF yang akan digabung:")
        self.label.pack(pady=5)
        # Variabel listbox untuk menampilkan nama file
        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(padx=20, pady=5)
        # Variabel untuk antarmuka lainnya
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_pilih = ttk.Button(button_frame, text="Tambah File", command=self.pilih_file)
        self.btn_pilih.grid(row=0, column=0, padx=5)
        
        self.btn_hapus = ttk.Button(button_frame, text="Hapus Semua", command=self.reset_list)
        self.btn_hapus.grid(row=0, column=1, padx=5)

        # Variabel untuk mengeksekusi
        self.btn_proses = ttk.Button(root, text="Gabungkan Semua", command=self.proses_gabung)
        self.btn_proses.pack(pady=20)

        # Variabel untuk status bar
        self.status_bar = tk.StringVar(value="Siap digunakan")
        self.status_label = tk.Label(root, textvariable=self.status_bar, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # Fungsi untuk memilih file
    def pilih_file(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            for f in files:
                if f not in self.files_terpilih:
                    self.files_terpilih.append(f)
                    # Menampilkan nama file
                    nama_file = f.split("/")[-1]
                    self.listbox.insert(tk.END, nama_file)

    # Fungsi untuk mereset file
    def reset_list(self):
        self.files_terpilih = []
        self.listbox.delete(0, tk.END)
    
    # Fungsi untuk menggabungkan file
    def proses_gabung(self):
        if not self.files_terpilih:
            messagebox.showwarning("Peringatan", "Silahkan pilih file terlebih dahulu")
            return
        # Menentukan nama output
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if save_path:
            gabung_pdf(self.files_terpilih, save_path)
            messagebox.showinfo("Selesai", "PDF Sudah digabungkan")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()