import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from logic_pdf import gabung_pdf, potong_pdf, batch_word_ke_pdf, kompres_pdf, hapus_meta_data_pdf, buat_qr_code, simpan_qr_code

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
        self.tab_compress = ttk.Frame(self.notebook)
        self.tab_metadata = ttk.Frame(self.notebook)
        self.tab_qr = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_merge, text=" Gabung PDF ")
        self.notebook.add(self.tab_split, text=" Potong PDF ")
        self.notebook.add(self.tab_word, text=" Word ke PDF ")
        self.notebook.add(self.tab_image, text=" Foto ke PDF ")
        self.notebook.add(self.tab_compress, text=" Kompres PDF ")
        self.notebook.add(self.tab_metadata, text=" Metadata ")
        self.notebook.add(self.tab_qr, text=" Generate QR Code ")

        self.setup_merge_ui()
        self.setup_split_ui()
        self.setup_word_ui()
        self.setup_image_ui()
        self.setup_compress_ui()
        self.setup_metadata_ui()
        self.setup_qr_ui()

        # Status Bar
        self.status_var = tk.StringVar(value="Siap")
        self.status_label = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Binding keyboard global
        self.root.bind_all('<Control-a>', self.handle_select_all)
        self.root.bind_all('<Control-A>', self.handle_select_all)
        self.root.bind_all('<Control-r>', lambda e: self.handle_reset())
        self.root.bind_all('<Control-R>', lambda e: self.handle_reset())
        self.root.bind_all('<Delete>', lambda e: self.handle_delete())
    
    # Fungsi untuk fitur binding
    # Fungsi untuk mendeteksi current tab
    def get_current_tab_data(self):
        """Mendeteksi tab aktif dan mengembalikan(listbox, list_data)"""
        try:
            current_tab_idx = self.notebook.index(self.notebook.select())

            # Mapping index ke object
            mapping = {
                0: (self.list_merge, self.files_merge),
                2: (self.list_word, self.files_word),
                3: (self.list_image, self.files_image)
            }

            return mapping.get(current_tab_idx, (None, None))
        except:
            return None, None
        
    # Fungsi untuk Menghapus File dan Select All
    def handle_select_all(self, event=None):
        listbox, _ = self.get_current_tab_data()
        if listbox:
            listbox.select_set(0, tk.END)
            listbox.focus_set()
        return "break"
    
    def handle_delete(self, event=None, dari_tombol=False):
        listbox, data_list = self.get_current_tab_data()

        if not listbox or not data_list:
            return
        
        indices = listbox.curselection()
        if not indices:
            if dari_tombol:
                messagebox.showwarning("Peringatan", "Pilih file di daftar dulu!")
            return
        
        for i in sorted(indices, reverse=True):
            if i < len(data_list):
                del data_list[i]
                listbox.delete(i)
        
        self.status_var.set(f"Daftar diperbarui. Sisa file: {len(data_list)}")
    
    def handle_reset(self):
        listbox, data_list = self.get_current_tab_data()

        if listbox is not None and data_list is not None:
            confirm_reset = messagebox.askyesno("Konfirmasi Reset", "Apakah anda yakin untuk menghapus semua file ini?")

            if confirm_reset:
                data_list.clear()
                listbox.delete(0, tk.END)
                self.status_var.set("Berhasil di Reset")
        
    # --- TAB 1: GABUNG ---
    def setup_merge_ui(self):
        tk.Label(self.tab_merge, text="Gabung PDF", font=("Arial", 10, "bold")).pack(pady=10)
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
        ttk.Button(btn_frame, text="Hapus Terpilih", command=lambda:self.handle_delete(dari_tombol=True)).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.handle_reset).grid(row=0, column=2, padx=5)
        
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
        
        ttk.Button(self.tab_split, text="POTONG", command=self.proses_potong).pack(pady=30)

    # --- TAB 3: WORD KE PDF (BATCH) ---
    def setup_word_ui(self):
        tk.Label(self.tab_word, text="Rubah Word ke PDF", font=("Arial", 10, "bold")).pack(pady=10)
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
        ttk.Button(btn_frame, text="Hapus Terpilih", command=lambda:self.handle_delete(dari_tombol=True)).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.handle_reset).grid(row=0, column=2, padx=5)
        
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
        try:
            halaman = int(self.ent_halaman.get())
        except ValueError:
            messagebox.showerror("Error", "Nomor halaman harus berupa angka bulat!")
            return
        if out:
            try:
                potong_pdf(self.file_split_path, int(self.ent_halaman.get()), out)
                messagebox.showinfo("Sukses", "Halaman berhasil dipotong!")
            except Exception as e: messagebox.showerror

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
        tk.Label(self.tab_image, text="Rubah Foto (JPG/PNG) untuk jadi PDF", font=("Arial", 10, "bold")).pack(pady=10)
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
            selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set
        )
        self.list_image.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.list_image.yview)

        # Bagian Button
        btn_frame = ttk.Frame(self.tab_image)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Tambah Foto", command=self.pilih_image_multi).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Hapus Terpilih", command=lambda:self.handle_delete(dari_tombol=True)).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.handle_reset).grid(row=0, column=2, padx=5)

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
    
    # TAB KOMPRES PDF 
    def setup_compress_ui(self):
        tk.Label(self.tab_compress, text="Kompres Ukuran File PDF", font=("Arial", 10, "bold")).pack(pady=10)

        self.file_to_compress = ""
        self.lbl_file_compress = tk.Label(self.tab_compress, text="Belum ada file dipilih", fg="gray")
        self.lbl_file_compress.pack(pady=5)
        # Kualitas Kompress
        self.lbl_q = tk.Label(self.tab_compress, text="Pilih tingkat kualitas")
        self.lbl_q.pack(pady=(10,0))

        self.quality_slider = tk.Scale(
            self.tab_compress,
            from_=10, to=100,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.quality_slider.set(60)
        self.quality_slider.pack(pady=10)

        btn_frame = ttk.Frame(self.tab_compress)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Pilih File PDF", command=self.pilih_file_compress).grid(row=0, column=0, padx=5)
        ttk.Button(self.tab_compress, text="Kompres Sekarang", command=self.proses_kompres).pack(pady=20)

        # Booleanvar untuk checkbox
        self.strip_metadata_var = tk.BooleanVar(value=True)
        self.cb_metadata = tk.Checkbutton(
            self.tab_compress,
            text="Hapus Metadata",
            variable=self.strip_metadata_var
        )
        self.cb_metadata.pack(pady=5)
    
    def pilih_file_compress(self):
        f = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if f:
            self.file_to_compress = f
            self.lbl_file_compress.config(text=os.path.basename(f), fg="black")

    def proses_kompres(self):
        if not self.file_to_compress:
            messagebox.showwarning("Peringatan", "Pilih file PDF dulu!")
            return
        
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if out:
            # Mengambil data dari slider
            nilai_kualitas = self.quality_slider.get()
            status_strip = self.strip_metadata_var.get()

            # Menambahkan informasi status
            print(f"Memproses dengan kualitas: {nilai_kualitas}")

            try:
                sukses = kompres_pdf(self.file_to_compress, out, kualitas=nilai_kualitas, strip_metadata=status_strip)

                if sukses:
                    size_old = os.path.getsize(self.file_to_compress) / 1024
                    size_new = os.path.getsize(out) / 1024
                    messagebox.showinfo("Sukses", 
                        f"Berhasil Kompres ({nilai_kualitas}%)!\n"
                        f"Ukuran Awal: {size_old:.1f} KB\n"
                        f"Ukuran Baru: {size_new:.1f} KB\n"
                        f"Hemat: {size_old - size_new:.1f} KB")
                else:
                    messagebox.showerror("Error", "Gagal kompres")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # Tab hapus metadata
    def setup_metadata_ui(self):
        tk.Label(self.tab_metadata, text="Hapus Metadata PDF", font=("Arial", 10, "bold")).pack(pady=10)

        self.file_metadata = ""
        self.lbl_file_metadata = tk.Label(self.tab_metadata, text="Belum ada file dipilih", fg="gray")
        self.lbl_file_metadata.pack(pady=5)

        tk.Button(self.tab_metadata, text="Pilih File PDF", command=self.pilih_file_metadata).pack(pady=10)
        ttk.Button(self.tab_metadata, text="HAPUS METADATA", command=self.proses_metadata).pack(pady=20)

    # Fungsi pilih metadata
    def pilih_file_metadata(self):
        f = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if f:
            self.file_metadata = f
            self.lbl_file_metadata.config(text=os.path.basename(f), fg="black")

    # Fungsi pengolah metadata
    def proses_metadata(self):
        if not self.file_metadata:
            messagebox.showwarning("Peringatan", "Pilih file PDF dulu")
            return

        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if out:
            # PyMuPDF tidak bisa menyimpan ke file yang sedang dibuka (file sumber),
            # jadi jalur output yang sama dengan input ditolak sejak awal.
            if os.path.abspath(out) == os.path.abspath(self.file_metadata):
                messagebox.showerror("Error", "Simpan hasil dengan nama atau lokasi berbeda dari file asli!")
                return

            self.status_var.set("Menghapus metadata...")
            self.root.update_idletasks()

            # hapus_meta_data_pdf() mengembalikan True/False, bukan melempar error
            if hapus_meta_data_pdf(self.file_metadata, out):
                messagebox.showinfo("Sukses", "Metadata berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Gagal menghapus metadata")
            self.status_var.set("Siap")

    # Tab QR Code Generator
    def setup_qr_ui(self):
        tk.Label(self.tab_qr, text="QR Code Generator", font=("Arial", 10, "bold")).pack(pady=10)

        tk.Label(self.tab_qr, text="Masukan URL: ").pack(pady=(10, 0))
        self.ent_qr_url = ttk.Entry(self.tab_qr, width=50)
        self.ent_qr_url.pack(pady=5)

        tk.Label(self.tab_qr, text="Simpan Sebagai:").pack(pady=(20, 5))
        frame_qr_btn = ttk.Frame(self.tab_qr)
        frame_qr_btn.pack(pady=5)
        ttk.Button(frame_qr_btn, text="JPEG", command=lambda: self.proses_simpan_qr("JPEG")).grid(row=0, column=0, padx=10)
        ttk.Button(frame_qr_btn, text="PNG", command=lambda: self.proses_simpan_qr("PNG")).grid(row=0, column=1, padx=10)
        ttk.Button(frame_qr_btn, text="PDF", command=lambda: self.proses_simpan_qr("PDF")).grid(row=0, column=2, padx=10)

    def proses_simpan_qr(self, format_file):
        data = self.ent_qr_url.get().strip()
        if not data:
            messagebox.showwarning("Peringatan", "Masukan URL atau Teks Terlebih Dahulu")
            return
        ekstensi = "jpg" if format_file == "JPEG" else format_file.lower()
        out = filedialog.asksaveasfilename (
            defaultextension=f".{ekstensi}",
            filetypes=[(format_file, f"*.{ekstensi}")]
        )
        if out:
            try:
                img = buat_qr_code(data)
                simpan_qr_code(img, out, format_file)
                messagebox.showinfo("Sukses", "QR Code berhasil disimpan")
            except Exception as e:
                messagebox.showerror("Error" f"Gagal membuat QR Code: {e}")
                 
if __name__ == "__main__":
    app_root = tk.Tk()
    app = PDFApp(app_root)
    app_root.mainloop()