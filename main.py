import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from logic_pdf import gabung_pdf, potong_pdf, batch_word_ke_pdf

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelola PDF")
        self.root.geometry("600x650")
        
        # State Data
        self.files_merge = []
        self.files_word = []
        self.file_split_path = ""
        self.files_image = []

        # Setup Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_merge = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)
        self.tab_word = ttk.Frame(self.notebook)
        self.tab_image = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text=" Gabung PDF ")
        self.notebook.add(self.tab_split, text=" Potong PDF ")
        self.notebook.add(self.tab_word, text=" Word ke PDF ")
        self.notebook.add(self.tab_image, text=" Foto ke PDF ")

        self.setup_merge_ui()
        self.setup_split_ui()
        self.setup_word_ui()
        self.setup_image_ui()

        # Status Bar
        self.status_var = tk.StringVar(value="Siap")
        self.status_label = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # --- TAB 1: GABUNG ---
    def setup_merge_ui(self):
        tk.Label(self.tab_merge, text="Antrean Gabung PDF", font=("Arial", 10, "bold")).pack(pady=10)
        # Frame untuk Listbox dan Scrollbar
        list_frame = ttk.Frame(self.tab_merge)
        list_frame.pack(padx=20, pady=5)
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_merge = tk.Listbox(
            list_frame,
            width=65,
            height=10,
            exportselection=False,
            yscrollcommand=scrollbar.set
        )
        self.list_merge.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.list_merge.yview)

        # Variabel untuk Button
        btn_frame = ttk.Frame(self.tab_merge)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Tambah File", command=self.pilih_merge_multi).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hapus Terpilih", command=self.hapus_merge_satu).grid(row=0, column=1, padx=5)
        
        ttk.Button(self.tab_merge, text="PROSES GABUNG", command=self.proses_gabung).pack(pady=20)

    # --- TAB 2: POTONG ---
    def setup_split_ui(self):
        tk.Label(self.tab_split, text="Potong Per Halaman", font=("Arial", 10, "bold")).pack(pady=10)
        self.lbl_file_split = tk.Label(self.tab_split, text="Belum ada file terpilih", fg="blue")
        self.lbl_file_split.pack(pady=10)
        ttk.Button(self.tab_split, text="Pilih PDF Sumber", command=self.pilih_split_tunggal).pack()
        
        tk.Label(self.tab_split, text="Nomor Halaman:").pack(pady=(20, 5))
        self.ent_halaman = ttk.Entry(self.tab_split, width=10)
        self.ent_halaman.pack()
        
        ttk.Button(self.tab_split, text="PROSES POTONG", command=self.proses_potong).pack(pady=30)

    # --- TAB 3: WORD KE PDF (BATCH) ---
    def setup_word_ui(self):
        tk.Label(self.tab_word, text="Antrean Konversi Word ke PDF", font=("Arial", 10, "bold")).pack(pady=10)
        # Frame untuk Lisbox dan Scrollbar
        list_frame = ttk.Frame(self.tab_word)
        list_frame.pack(padx=20, pady=5)
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_word = tk.Listbox(
            list_frame,
            width=65,
            height=10,
            exportselection=False,
            yscrollcommand=scrollbar.set
        )
        self.list_word.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.list_word.yview)

        # Variabel untuk Button
        btn_frame = ttk.Frame(self.tab_word)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Tambah Word", command=self.pilih_word_multi).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hapus Terpilih", command=self.hapus_word_satu).grid(row=0, column=1, padx=5)
        
        ttk.Button(self.tab_word, text="KONVERSI SEMUA KE PDF", command=self.proses_batch_word).pack(pady=20)

    # --- FUNGSI LOGIKA (MERGE) ---
    def pilih_merge_multi(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for f in files:
            if f not in self.files_merge:
                self.files_merge.append(f)
                self.list_merge.insert(tk.END, os.path.basename(f))

    def hapus_merge_satu(self):
        try:
            idx = self.list_merge.curselection()[0]
            del self.files_merge[idx]
            self.list_merge.delete(idx)
        except: messagebox.showwarning("Peringatan", "Pilih file di daftar dulu!")

    def proses_gabung(self):
        if not self.files_merge: return
        out = filedialog.asksaveasfilename(defaultextension=".pdf")
        if out:
            gabung_pdf(self.files_merge, out)
            messagebox.showinfo("Sukses", "PDF Berhasil digabungkan!")

    # --- FUNGSI LOGIKA (SPLIT) ---
    def pilih_split_tunggal(self):
        f = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if f:
            self.file_split_path = f
            self.lbl_file_split.config(text=os.path.basename(f))

    def proses_potong(self):
        if not self.file_split_path or not self.ent_halaman.get(): return
        out = filedialog.asksaveasfilename(defaultextension=".pdf")
        if out:
            try:
                potong_pdf(self.file_split_path, int(self.ent_halaman.get()), out)
                messagebox.showinfo("Sukses", "Halaman berhasil dipotong!")
            except Exception as e: messagebox.showerror("Error", str(e))

    # --- FUNGSI LOGIKA (WORD BATCH) ---
    def pilih_word_multi(self):
        files = filedialog.askopenfilenames(filetypes=[("Word Files", "*.docx *.doc")])
        for f in files:
            if f not in self.files_word:
                self.files_word.append(f)
                self.list_word.insert(tk.END, os.path.basename(f))

    def hapus_word_satu(self):
        try:
            idx = self.list_word.curselection()[0]
            del self.files_word[idx]
            self.list_word.delete(idx)
        except: messagebox.showwarning("Peringatan", "Pilih file di daftar dulu!")

    def proses_batch_word(self):
        if not self.files_word: return
        folder = filedialog.askdirectory(title="Pilih Folder Hasil PDF")
        if folder:
            self.status_var.set("Sedang mengonversi massal... Mohon tunggu.")
            self.root.update_idletasks() # PERBAIKAN: Pakai huruf 's' di akhir
            try:
                batch_word_ke_pdf(self.files_word, folder)
                messagebox.showinfo("Sukses", f"Konversi selesai! Cek folder: {folder}")
            except Exception as e:
                messagebox.showerror("Error", f"Pastikan MS Word terinstall. Detail: {e}")
            self.status_var.set("Siap")
    
    # --- TAB KONVERSI FOTO KE PDF ---
    def setup_image_ui(self):
        tk.Label(self.tab_image, text="Daftar Foto (JPG/PNG) untuk jadi PDF", font=("Arial", 10, "bold")).pack(pady=10)
        # Frame untuk menampung ListBox dan Scrollbar
        list_frame = ttk.Frame(self.tab_image)
        list_frame.pack(padx=20, pady=5)
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_image = tk.Listbox(
            list_frame,
            width=65,
            height=10,
            exportselection=False,
            yscrollcommand=scrollbar.set
        )
        self.list_image.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.list_image.yview)

        # Bagian Button
        btn_frame = ttk.Frame(self.tab_image)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Tambah Foto", command=self.pilih_image_multi).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hapus Terpilih", command=self.hapus_image_satu).grid(row=0, column=1, padx=5)

        ttk.Button(self.tab_image, text="UBAH FOTO KE PDF", command=self.proses_image_pdf).pack(pady=20)
    
    # Fungsi memilih multiple file gambar
    def pilih_image_multi(self):
        files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *jpeg *.png")])
        for f in files:
            if f not in self.files_image:
                self.files_image.append(f)
                self.list_image.insert(tk.END, os.path.basename(f))
    
    # Fungsi menghapus satu file gambar
    def hapus_image_satu(self):
        seleksi = self.list_image.curselection()

        if seleksi:
            idx = seleksi[0]
            del self.files_image[idx]
            self.list_image.delete(idx)
            self.status_var.set(f"Foto dihapus. Sisa: {len(self.files_image)}")
        else:
            messagebox.showwarning("Peringatan", "Pilih foto di daftar terlebih dahulu!")
    
    # Fungsi untuk mengkonversi gambar ke PDF
    def proses_image_pdf(self):
        if not self.files_image:
            messagebox.showwarning("Peringatan", "Belum ada foto yang terpilih")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        
        if out:
            self.status_var.set("Mengonversi foto ke PDF")
            self.root.update_idletasks()
            try:
                from logic_pdf import image_ke_pdf
                image_ke_pdf(self.files_image, out)
                messagebox.showinfo("Sukses", f"Berhasil membuat PDF dari {len(self.files_image)} foto!")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memproses gambar: {e}")
            self.status_var.set("Siap")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = PDFApp(app_root)
    app_root.mainloop()