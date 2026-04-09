import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from logic_pdf import gabung_pdf, potong_pdf, word_ke_pdf

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelola PDF - Offline")
        self.root.geometry("550x550")
        
        # State Data
        self.files_terpilih = []
        self.file_tunggal_path = ""

        # --- SETUP TAB (NOTEBOOK) ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_merge = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text=" Gabung PDF ")
        self.notebook.add(self.tab_split, text=" Potong PDF ")

        self.setup_merge_ui()
        self.setup_split_ui()

        # Status Bar (Global)
        self.status_var = tk.StringVar(value="Siap")
        self.status_label = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # --- TAB 1: UI GABUNG ---
    def setup_merge_ui(self):
        tk.Label(self.tab_merge, text="Daftar File untuk Digabung:", font=("Arial", 10, "bold")).pack(pady=10)
        self.listbox = tk.Listbox(self.tab_merge, width=60, height=10)
        self.listbox.pack(padx=20, pady=5)

        btn_frame = ttk.Frame(self.tab_merge)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Tambah File", command=self.pilih_file_multi).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hapus Semua", command=self.reset_list).grid(row=0, column=1, padx=5)

        ttk.Button(self.tab_merge, text="PROSES GABUNG", command=self.proses_gabung).pack(pady=20)

    # --- TAB 2: UI POTONG ---
    def setup_split_ui(self):
        tk.Label(self.tab_split, text="File Sumber:", font=("Arial", 10, "bold")).pack(pady=10)
        self.lbl_file_split = tk.Label(self.tab_split, text="Belum ada file", fg="blue")
        self.lbl_file_split.pack(pady=5)
        
        ttk.Button(self.tab_split, text="Pilih File PDF", command=self.pilih_file_tunggal).pack(pady=5)

        tk.Label(self.tab_split, text="Masukkan Nomor Halaman:").pack(pady=20)
        self.ent_halaman = ttk.Entry(self.tab_split, width=10)
        self.ent_halaman.pack()

        ttk.Button(self.tab_split, text="POTONG & SIMPAN", command=self.proses_potong).pack(pady=30)
    
    # --- TAB 3: WORD KE PDF ---
    def setup_web_ui(self):
        tk.Label(self.tab_word, text="Konversi Word (.docx) ke PDF", font=("Arial", 10, "bold")).pack(pady=10)
        self.lbl_word_path = tk.Label(self.tab_word, text="Belum ada file yang terpilih", fg="green")
        self.lbl_word_path.pack(pady=10)
        ttk.Button(self.tab_word, text="Pilih File Word", command=self.pilih_file_word).pack(pady=5)
        ttk.Button(self.tab_word, text="Konversi ke PDF", command=self.proses_konversi_word).pack(pady=40)
    
    # --- FUNGSI LOGIKA KONVERSI WORD KE PDF ---
    def pilih_file_word(self):
        f = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if f:
            self.file_word_path = f
            self.lbl_word_path.config(text=f.split("/")[-1])
            self.status_var.set("File word siap dikonversi")
    
    def fungsi_konversi(self):
        if not self.file_word_path:
            messagebox.showwarning("Peringatan", "Pilih file Word dulu!")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if save_path:
            try:
                self.status_var.set("Mengonversi.. Mohon menunggu")
                self.root.update_idletask()
                word_ke_pdf(self.file_word_path, save_path)
                messagebox.showinfo("Sukses", "File selesai dikonversi")
                self.status_var.set("Konversi selesai")
            except Exception as e:
                messagebox.showerror("Error", f"Pastikan MS Word terinstall. Error: {e}")
                self.status_var.set("Gagal konversi")

    # --- LOGIKA FUNGSI ---
    def pilih_file_multi(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            for f in files:
                if f not in self.files_terpilih:
                    self.files_terpilih.append(f)
                    self.listbox.insert(tk.END, f.split("/")[-1])
            self.status_var.set(f"Total: {len(self.files_terpilih)} file")

    def reset_list(self):
        self.files_terpilih = []
        self.listbox.delete(0, tk.END)
        self.status_var.set("Daftar dikosongkan")

    def proses_gabung(self):
        if not self.files_terpilih:
            messagebox.showwarning("Peringatan", "Pilih file dulu!")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf")
        if out:
            gabung_pdf(self.files_terpilih, out)
            messagebox.showinfo("Sukses", "PDF berhasil digabung!")

    def pilih_file_tunggal(self):
        f = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if f:
            self.file_tunggal_path = f
            self.lbl_file_split.config(text=f.split("/")[-1])

    def proses_potong(self):
        if not self.file_tunggal_path or not self.ent_halaman.get():
            messagebox.showwarning("Peringatan", "Lengkapi file dan nomor halaman!")
            return
        try:
            hal = int(self.ent_halaman.get())
            out = filedialog.asksaveasfilename(defaultextension=".pdf")
            if out:
                potong_pdf(self.file_tunggal_path, hal, out)
                messagebox.showinfo("Sukses", f"Halaman {hal} berhasil dipotong!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    
if __name__ == "__main__":
    app_root = tk.Tk()
    app = PDFApp(app_root)
    app_root.mainloop()