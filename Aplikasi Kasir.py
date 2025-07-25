import tkinter as tk
from tkinter import messagebox, TclError
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
import csv
from datetime import datetime

#Setiap menu kini dapat langsung ditambahkan ke keranjang hanya dengan menekan gambar menu.
#Jumlah pesanan dapat disesuaikan dengan menekan angka kuantitas setelah memilih menu.
#Tombol untuk menghapus menu kini ditempatkan secara lebih efisien di samping nama menu.
#Struk akan langsung tercetak secara otomatis setelah nominal pembayaran dimasukkan.
#Tampilan antarmuka aplikasi telah diperbarui agar terlihat lebih rapi dan terstruktur.
#Password (pilih salah satu) "yuna001", "adit008", "alin004", "pawone123"

class RestaurantPOS:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.geometry('1200x800')
        self.root.title("Pawone Simbah Restaurant")
        self.user_data = {"nama": "", "Kasir": ""}
        self.menu_items = []
        self.filtered_items = []
        self.order_items = []
        self.data_dir = "data"
        self.valid_passwords = ["yuna001", "adit008", "alin004", "pawone123"]
        self.create_data_directory()
        self._bg_image_tk_welcome = None
        self._original_bg_image = None
        self.image_cache = {}

    def create_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _resize_welcome_page(self, event=None):
        if not hasattr(self, 'welcome_canvas') or not self.welcome_canvas.winfo_exists(): return
        width, height = self.welcome_canvas.winfo_width(), self.welcome_canvas.winfo_height()
        if width <= 1 or height <= 1: return
        try:
            
            if self._original_bg_image is None: self._original_bg_image = Image.open("bc1.jpg")
            img_resized = self._original_bg_image.resize((width, height), Image.LANCZOS)
            self._bg_image_tk_welcome = ImageTk.PhotoImage(img_resized)
            self.welcome_canvas.create_image(0, 0, anchor="nw", image=self._bg_image_tk_welcome, tags="bg_image")
        except Exception as e:
            print(f"Error resizing background: {e}")
            self.welcome_canvas.configure(bg="#2c3e50")

        
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            if not self.error_label.cget("text"):
                self.error_label.config(bg=self.welcome_canvas['bg'])
            self.error_label.lift()

        for tag in ["text_title", "text_nama_kasir", "text_password"]: self.welcome_canvas.delete(tag)
        font_size_title = max(12, min(24, int(height / 25)))
        font_size_label = max(9, min(16, int(height / 35)))
        self.welcome_canvas.create_text(width / 2, height * 0.22, text="KASIR\nPAWONE SIMBAH RESTAURANT", font=("Perpetua", font_size_title, "bold"), fill="white", justify="center", tags="text_title")
        self.welcome_canvas.create_text(width / 2, height * 0.36, text="Nama Penjaga Kasir", font=("Perpetua", font_size_label, "bold"), fill="white", justify="center", tags="text_nama_kasir")
        self.welcome_canvas.create_text(width / 2, height * 0.47, text="Password", font=("Perpetua", font_size_label, "bold"), fill="white", justify="center", tags="text_password")
        for widget_name in ['Entry_nama', 'Entry_nomor', 'button_next_welcome']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                if widget.winfo_exists(): widget.lift()

    def welcome_page(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.resizable(True, True)
        self.welcome_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.welcome_canvas.pack(fill=tk.BOTH, expand=True)
        self.Entry_nama = tk.Entry(self.root, width=30, font=("Arial", 11))
        self.Entry_nama.place(relx=0.5, rely=0.42, anchor="center")
        self.Entry_nomor = tk.Entry(self.root, width=30, font=("Arial", 11), show="*")
        self.Entry_nomor.place(relx=0.5, rely=0.52, anchor="center")
        
        self.error_label = tk.Label(self.root, text="", font=("Arial", 10), fg="red")
        self.error_label.place(relx=0.5, rely=0.58, anchor="center")
        self.button_next_welcome = ttk.Button(self.root, text="Lanjut", bootstyle="warning", command=self.validate_login)
        self.button_next_welcome.place(relx=0.5, rely=0.65, anchor="center")
        self.welcome_canvas.bind("<Configure>", self._resize_welcome_page)
        self.root.update_idletasks()
        self._resize_welcome_page()
        self.root.bind('<Return>', lambda event: self.validate_login())
        self.Entry_nama.focus()

    def validate_login(self):
        nama, password = self.Entry_nama.get().strip(), self.Entry_nomor.get().strip()
        if hasattr(self, 'error_label') and self.error_label.winfo_exists(): self.error_label.config(text="", bg=self.welcome_canvas['bg']) # Bersihkan teks dan atur latar belakang agar cocok dengan kanvas
        if not nama: self.show_error("Nama kasir harus diisi!"); self.Entry_nama.focus(); return
        if not password: self.show_error("Password harus diisi!"); self.Entry_nomor.focus(); return
        if password not in self.valid_passwords:
            self.show_error("Password salah! Silakan coba lagi.")
            self.Entry_nomor.delete(0, tk.END); self.Entry_nomor.focus(); return
        self.user_data["Kasir"], self.user_data["Password"] = nama, password
        self.root.unbind('<Return>')
        if hasattr(self, 'welcome_canvas'): self.welcome_canvas.unbind("<Configure>")
        self.show_main_interface()

    def show_error(self, message):
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            
            self.error_label.config(text=message, bg="#3F3F3F") # Warna latar belakang gelap agar teks merah terlihat
            self.root.after(3000, lambda: self.error_label.config(text="", bg=self.welcome_canvas['bg']) if hasattr(self, 'error_label') and self.error_label.winfo_exists() else None)

    def open_menu_page(self):
        
        self.menu_items = [
            {"name": "Nasi Goreng Spesial", "price": 15000, "category": "Makanan", "options": ["Pedas", "Manis", "Original", "Extra Telur"], "image": r"Nasi Goreng.jpg"},
            {"name": "Ayam Pilihan", "price": 15000, "category": "Makanan", "options": ["Goreng", "Penyet", "Bakar", "Kremes", "Rica-Rica", "Geprek"], "image": r"Ayam.jpg"},
            {"name": "Burger Klasik", "price": 20000, "category": "Makanan", "options": ["Beef", "Chicken", "HAM", "Vege"], "image": r"Burger.jpg"},
            {"name": "Soto Semarang", "price": 15000, "category": "Makanan", "options": ["Ayam", "Sapi", "Campur"], "image": r"soto.jpg"},
            {"name": "Mie Ayam Komplit", "price": 10000, "category": "Makanan", "options": ["Mi-Bakso", "Mi-Pangsit", "Mi-Yago", "Original"], "image": r"Mie Ayam.jpg"},
            {"name": "Ikan Segar Pilihan", "price": 15000, "category": "Makanan", "options": ["Bakar","Goreng","Gulai"], "image": r"Ikan.jpg"},
            {"name": "Mie Yamin", "price": 15000, "category": "Makanan", "options": ["Original", "Pangsit", "Bakso", "Mix Topping"], "image": r"mie yamin.jpg"},
            {"name": "Ayam Bumbu Bali", "price": 15000, "category": "Makanan", "options": ["Pedas", "Normal"], "image": r"Nasi Ayam Bali.jpeg"},
            {"name": "Telur Barendo", "price": 15000, "category": "Makanan", "options": ["Pedas","Asin"], "image": r"barendo.jpg"},
            {"name": "Ayam Katsu Spesial", "price": 15000, "category": "Makanan", "options": ["BBQ", "Teriyaki","Hot Sauce", "Blackpepper", "Original"], "image": r"Katsu.jpg"},
            {"name": "Bakso Urat", "price": 15000, "category": "Makanan", "options": ["Kosongan", "Balungan", "Komplit"], "image": r"bakso.jpg"},
            {"name": "Sate Madura", "price": 15000, "category": "Makanan", "options": ["Ayam", "Sapi", "Kambing"], "image": r"Sate.jpg"},
            {"name": "Mix Platter", "price": 32000, "category": "Cemilan", "options": ["Large", "Medium", "Small"], "image": r"Mix Platter.jpg"},
            {"name": "Aneka Pisang", "price": 30000, "category": "Cemilan", "options": ["Goreng", "Bakar Coklat", "Bakar Keju", "Bakar Mix"], "image": r"Pisang.jpg"},
            {"name": "Roti Bakar", "price": 15000, "category": "Cemilan", "options": ["Coklat", "Keju", "Mix 2 Topping", "Strawberry", "Nanas", "Original"], "image": r"Robak.jpg"},
            {"name": "Dimsum Lezat", "price": 15000, "category": "Cemilan", "options": ["Original", "Mentai", "BBQ", "Mayo Pedas", "Chili Oil"], "image": r"Dimsum.jpg"},
            {"name": "Teh Klasik", "price": 7000, "category": "Minuman", "options": ["Ice", "Hot", "Normal"], "image": r"es teh.jpg"},
            {"name": " Leci Tea", "price": 10000, "category": "Minuman", "options": ["Ice", "Hot", "Normal", "Less Sugar"], "image": r"leci.jpg"},
            {"name": "Pure Matcha", "price": 20000, "category": "Minuman", "options": ["Ice", "Hot", "Normal"], "image": r"pure matcha.jpg"},
            {"name": "Thai Tea", "price": 7000, "category": "Minuman", "options": ["Ice", "Hot", "Normal", "Less Sugar"], "image": r"Thaitea.jpg"},
            {"name": "Lemon Tea", "price": 7000, "category": "Minuman", "options": ["Ice", "Hot", "Normal"], "image": r"Lemon.jpg"},
            {"name": "Kopi Susu Gula Aren", "price": 7000, "category": "Minuman", "options": ["Ice", "Hot", "Normal", "Less Sugar"], "image": r"kopsu.jpg"},
        ]
        self.filtered_items = self.menu_items.copy()

    def show_main_interface(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.resizable(True, True); self.root.state('zoomed')
        self.open_menu_page()
        
        # Header
        header = tk.Frame(self.root, bg="#222222", height=60); header.pack(fill=tk.X, side=tk.TOP, pady=(0,5)); header.pack_propagate(False)
        tk.Label(header, text=f"Kasir: {self.user_data['Kasir']}", font=("Arial", 14, "bold"), fg="white", bg="#222222").pack(side=tk.LEFT, padx=10, pady=10)
        search_frame = tk.Frame(header, bg="#222222"); search_frame.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(search_frame, text="Cari Menu:", bg="#222222", fg="white").pack(side=tk.LEFT)
        self.search_var = tk.StringVar(); 
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.search_menu)
        ttk.Button(header, text="Log out", command=self.confirm_logout, bootstyle="danger").pack(side=tk.RIGHT, padx=10, pady=10)
        table_frame = tk.Frame(header, bg="#222222"); table_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        tk.Label(table_frame, text="Nama Pelanggan:", bg="#222222", fg="white").pack(side=tk.LEFT)
        self.table_var = tk.StringVar(); ttk.Entry(table_frame, textvariable=self.table_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # Body
        body = tk.Frame(self.root); body.pack(fill=tk.BOTH, expand=True)
        sidebar = tk.Frame(body, bg="#2B2B2B", height=60); sidebar.pack(fill=tk.X, padx=5); sidebar.pack_propagate(False)
        tk.Label(sidebar, text="Kategori:", font=("Arial", 12, "bold"), bg="#2B2B2B", fg="white").pack(side=tk.LEFT, padx=10, pady=15)
        for category in ["Semua", "Makanan", "Minuman", "Cemilan"]:
            ttk.Button(sidebar, text=category, width=12, bootstyle="primary-outline", command=lambda c=category: self.filter_menu(c)).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Content (Menu dan Order)
        content_frame = tk.Frame(body); content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        content_frame.grid_columnconfigure(0, weight=1) 
        content_frame.grid_columnconfigure(1, weight=0, minsize=480) # Disesuaikan agar keranjang lebih lebar
        content_frame.grid_rowconfigure(0, weight=1)

        # Order frame (cart)
        self.order_frame = tk.Frame(content_frame, bd=2, relief=tk.RIDGE)
        self.order_frame.grid(row=0, column=1, sticky="ns", padx=(10,5))
        
        tk.Label(self.order_frame, text="Pesanan", font=("Arial", 16, "bold")).pack(pady=(10,5))
        
        tree_frame = tk.Frame(self.order_frame); tree_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        columns = ("Item", "Qty", "Harga", "Hapus")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 13, "bold")) 
        style.configure("Treeview", font=("Arial", 12)) 

        self.tree.heading("Item", text="Item"); self.tree.heading("Qty", text="Qty"); self.tree.heading("Harga", text="Harga"); self.tree.heading("Hapus", text="")
        self.tree.column("Item", width=220, anchor='w'); self.tree.column("Qty", width=50, anchor='center'); self.tree.column("Harga", width=100, anchor='e'); self.tree.column("Hapus", width=40, anchor='center')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.handle_tree_click)
        
        total_frame = tk.Frame(self.order_frame); total_frame.pack(fill=tk.X, padx=10, pady=(10,5), side=tk.BOTTOM)
        self.total_label = tk.Label(total_frame, text="Total: Rp 0", font=("Arial", 13, "bold"), fg="#4CAF50"); self.total_label.pack(anchor="w")
        payment_frame = tk.LabelFrame(self.order_frame, text="Pembayaran", font=("Arial", 11, "bold")); payment_frame.pack(fill=tk.X, padx=10, pady=5, side=tk.BOTTOM)
        tk.Label(payment_frame, text="Jumlah Bayar (Rp):").pack(anchor="w", padx=5, pady=(5,2))
        self.payment_var = tk.StringVar(); self.payment_entry = ttk.Entry(payment_frame, textvariable=self.payment_var, font=("Arial", 12)); self.payment_entry.pack(fill=tk.X, padx=5, pady=2)
        self.payment_entry.bind('<KeyRelease>', self.calculate_change)
        self.change_label = tk.Label(payment_frame, text="Kembalian: Rp 0", font=("Arial", 12, "bold"), fg="#2196F3"); self.change_label.pack(anchor="w", padx=5, pady=(2,5))
        
        ttk.Button(self.order_frame, text="Cetak Struk & Simpan", command=self.print_receipt, bootstyle="success").pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM, ipady=4)
        
        
        menu_container = tk.Frame(content_frame)
        menu_container.grid(row=0, column=0, sticky="nsew", padx=(5,0))
        self.menu_canvas = tk.Canvas(menu_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_container, orient="vertical", command=self.menu_canvas.yview)
        self.menu_items_frame = tk.Frame(self.menu_canvas)
        
        canvas_window = self.menu_canvas.create_window((0, 0), window=self.menu_items_frame, anchor="nw")

        def configure_canvas(event):
            self.menu_canvas.itemconfig(canvas_window, width=event.width)
        
        def configure_frame(event):
            self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))

        self.menu_canvas.bind("<Configure>", configure_canvas)
        self.menu_items_frame.bind("<Configure>", configure_frame)
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_menu_display(); self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def confirm_logout(self):
        if messagebox.askyesno("Konfirmasi Log Out", "Apakah Anda yakin ingin log out?", parent=self.root): self.welcome_page()
        
    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?", parent=self.root): self.root.destroy()

    def calculate_change(self, event=None):
        try:
            payment = float(self.payment_var.get().replace(",", "")) if self.payment_var.get() else 0.0
            total = sum(item['qty'] * item['price'] for item in self.order_items)
            grand_total = total  
            change = payment - grand_total
        
            if payment == 0 and total == 0:
                self.change_label.config(text="Kembalian: Rp 0", fg="#2196F3")
            elif payment == 0 and total > 0:
                self.change_label.config(text=f"Kurang: Rp {abs(grand_total):,.0f}", fg="red")
            elif change >= 0:
                self.change_label.config(text=f"Kembalian: Rp {change:,.0f}", fg="#2196F3")
            else:
                self.change_label.config(text=f"Kurang: Rp {abs(change):,.0f}", fg="red")
            
        except ValueError:
            current_total = sum(item['qty'] * item['price'] for item in self.order_items)
            self.change_label.config(text=f"Kurang: Rp {current_total:,.0f}", fg="red")

    def filter_menu(self, category):
        self.filtered_items = self.menu_items if category == "Semua" else [item for item in self.menu_items if item["category"] == category]
        self.update_menu_display()

    def search_menu(self, *args):
        query = self.search_var.get().lower()
        self.filtered_items = [item for item in self.menu_items if query in item["name"].lower()]
        self.update_menu_display()

    def handle_item_click(self, item):
        if item["options"]:
            self.show_options_dialog(item)
        else:
            self.add_to_order(item, option=None, quantity=1)

    def show_options_dialog(self, item):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Pilih Opsi - {item['name']}")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        style = ttk.Style()
        style.configure('Dialog.TFrame', background='#333333')
        dialog_frame = ttk.Frame(dialog, padding=20, style='Dialog.TFrame')
        dialog_frame.pack(expand=True, fill="both")

        opt_var = tk.StringVar(value=item["options"][0] if item["options"] else "")
        qty_var = tk.IntVar(value=1)

        ttk.Label(dialog_frame, text="Pilih Varian:", font=("Arial", 12, "bold")).pack(pady=(10,5), padx=20)
        options_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame'); options_frame.pack(pady=5, padx=20, fill="x")
        for option in item["options"]:
            ttk.Radiobutton(options_frame, text=option, variable=opt_var, value=option).pack(anchor="w", pady=2)

        ttk.Label(dialog_frame, text="Jumlah:", font=("Arial", 12, "bold")).pack(pady=(10,5), padx=20)
        stepper_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame'); stepper_frame.pack(pady=5, padx=20)
        ttk.Button(stepper_frame, text="-", width=3, bootstyle="secondary", command=lambda: qty_var.set(max(1, qty_var.get() - 1))).pack(side=tk.LEFT)
        tk.Entry(stepper_frame, textvariable=qty_var, width=5, font=("Arial", 10, "bold"), justify='center').pack(side=tk.LEFT, padx=5)
        ttk.Button(stepper_frame, text="+", width=3, bootstyle="secondary", command=lambda: qty_var.set(qty_var.get() + 1)).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(dialog_frame, style='Dialog.TFrame'); btn_frame.pack(pady=20, padx=20, fill="x")
        
        def on_add():
            self.add_to_order(item, opt_var.get(), qty_var.get())
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Batal", command=dialog.destroy, bootstyle="secondary").pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Tambah", command=on_add, bootstyle="success").pack(side=tk.RIGHT, padx=(0,5))

        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        dialog.wait_window()

    def update_menu_display(self):
        for widget in self.menu_items_frame.winfo_children(): widget.destroy()
        
        num_columns = 5
        for i in range(num_columns): self.menu_items_frame.grid_columnconfigure(i, weight=1)

        for idx, item in enumerate(self.filtered_items):
            row = idx // num_columns
            col = idx % num_columns
            
            card = tk.Frame(self.menu_items_frame, bd=1, relief=tk.SOLID, bg="#333333")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            img_label = tk.Label(card, bg="#333333")
            img_label.pack(pady=(10,5), fill="x")
            
            name_label = tk.Label(card, text=item["name"], font=("Segoe UI", 12, "bold"), bg="#333333", fg="white", wraplength=150)
            name_label.pack(pady=(5,2), fill="x", expand=True)
            
            price_label = tk.Label(card, text=f"Rp {item['price']:,}", bg="#333333", fg="#4CAF50", font=("Segoe UI", 10, "bold"))
            price_label.pack(pady=(0,10))
            
            try:
                if item["image"] not in self.image_cache:
                    img = Image.open(item["image"]).resize((140, 110), Image.LANCZOS)
                    self.image_cache[item["image"]] = ImageTk.PhotoImage(img)
                img_label.config(image=self.image_cache[item["image"]])
            except Exception as e:
                img_label.config(text="[Gambar\nTidak\nTersedia]", fg="white", bg="#555555", width=18, height=6, font=("Arial", 9))
            
            for widget in [card, img_label, name_label, price_label]:
                widget.bind("<Button-1>", lambda e, i=item: self.handle_item_click(i))
    
    def add_to_order(self, item, option, quantity):
        try:
            qty = int(quantity)
            if qty <= 0:
                messagebox.showwarning("Jumlah Tidak Valid", "Jumlah item harus lebih dari 0.", parent=self.root)
                return
        except (ValueError, TclError):
            messagebox.showwarning("Jumlah Tidak Valid", "Masukkan jumlah yang benar.", parent=self.root)
            return

        option_to_use = option if option else "Default"
        for order in self.order_items:
            if order['name'] == item['name'] and order['option'] == option_to_use:
                order['qty'] += qty; self.update_order(); return
        self.order_items.append({"name": item['name'], "option": option_to_use, "price": item['price'], "qty": qty})
        self.update_order()

    def update_order(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        total = 0
        for item in self.order_items:
            subtotal = item['qty'] * item['price']
            display_name = f"{item['name']} ({item['option']})" if item['option'] and item['option'] != "Default" else item['name']
            self.tree.insert('', 'end', values=(display_name, item['qty'], f"{subtotal:,}", '🗑'))
            total += subtotal
            
        grand_total = total  
        self.total_label.config(text=f"Total: Rp {total:,}")
        self.calculate_change()

    def handle_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column_id = self.tree.identify_column(event.x)
            if column_id == "#4":
                item_id = self.tree.identify_row(event.y)
                item_index = self.tree.index(item_id)
                self.remove_item(item_index)

    def remove_item(self, index):
        try:
            item_to_remove = self.order_items[index]
            item_name_display = f"{item_to_remove['name']} ({item_to_remove['option']})" if item_to_remove['option'] and item_to_remove['option'] != "Default" else item_to_remove['name']
            if messagebox.askyesno("Konfirmasi Penghapusan", f"Yakin ingin menghapus '{item_name_display}' dari pesanan?", icon="question", parent=self.root):
                del self.order_items[index]
                self.update_order()
        except IndexError:
            print("Error: Item index out of range. Mungkin sudah dihapus.")
            self.update_order()

    def print_receipt(self):
        if not self.order_items:
            messagebox.showwarning("Kosong", "Tidak ada pesanan untuk dicetak.", parent=self.root)
            return
        try:
            payment_str = self.payment_var.get().replace(",", "")
            payment = float(payment_str) if payment_str else 0.0
        except (ValueError, TclError):
            messagebox.showerror("Error", "Masukkan jumlah pembayaran yang valid!", parent=self.root)
            return

        now = datetime.now()
        total_pesanan = sum(item['qty'] * item['price'] for item in self.order_items)
        grand_total_final = total_pesanan
        
        if payment < grand_total_final:
            messagebox.showerror("Error Pembayaran", f"Pembayaran kurang! Masih kurang Rp {(grand_total_final - payment):,.0f}", parent=self.root)
            return

        change = payment - grand_total_final
        receipt_data = {
            "tanggal": now.strftime("%Y-%m-%d"),
            "waktu": now.strftime("%H:%M:%S"),
            "nama_kasir": self.user_data['Kasir'],
            "table_number": self.table_var.get() if self.table_var.get() else " None",
            "items": self.order_items,
            "total_pesanan": total_pesanan,
            "grand_total": grand_total_final,
            "payment": payment,
            "change": change
        }
        
        
        receipt_string = "---------- PAWONE SIMBAH RESTAURANT ----------\n"
        receipt_string += "----------------------------------------------\n"
        receipt_string += f"Tanggal: {receipt_data['tanggal']}\n"
        receipt_string += f"Waktu:   {receipt_data['waktu']}\n"
        receipt_string += f"Kasir:   {receipt_data['nama_kasir']}\n"
        receipt_string += f"Meja/Pelanggan: {receipt_data['table_number']}\n"
        receipt_string += "----------------------------------------------\n"
        receipt_string += "{:<25} {:>5} {:>10}\n".format("Item", "Qty", "Subtotal")
        receipt_string += "----------------------------------------------\n"
        
        for item in receipt_data['items']:
            display_name = f"{item['name']}"
            if item['option'] and item['option'] != "Default":
                display_name += f" ({item['option']})"
            subtotal_item = item['qty'] * item['price']
            receipt_string += "{:<25} {:>5} {:>10,}\n".format(display_name, item['qty'], subtotal_item)
        
        receipt_string += "----------------------------------------------\n"
        receipt_string += f"{'Total Pesanan:':<30} Rp {receipt_data['total_pesanan']:,}\n"
        receipt_string += f"{'Jumlah Bayar:':<30} Rp {receipt_data['payment']:,}\n"
        receipt_string += f"{'Kembalian:':<30} Rp {receipt_data['change']:,}\n"
        receipt_string += "----------------------------------------------\n"
        receipt_string += "      ❤ Terima Kasih atas Kunjungan Anda ❤      \n"
        receipt_string += "----------------------------------------------\n"

        
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Struk Pembayaran")
        receipt_window.transient(self.root)
        receipt_window.grab_set()
        receipt_window.resizable(False, False)

       
        receipt_text_widget = tk.Text(receipt_window, wrap="word", font=("Consolas", 12), width=46, height=20, background="#2c3e50", foreground="white", bd=0, highlightthickness=0)
        receipt_text_widget.pack(padx=10, pady=10)
        receipt_text_widget.insert(tk.END, receipt_string)
        receipt_text_widget.config(state=tk.DISABLED) # Make text read-only

        receipt_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (receipt_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (receipt_window.winfo_height() // 2)
        receipt_window.geometry(f"+{x}+{y}")
        
        self.save_to_csv(receipt_data)
        messagebox.showinfo("Cetak Struk", "Struk berhasil dicetak dan data disimpan!", parent=self.root)
        
        self.order_items = []
        self.update_order()
        self.payment_var.set("") 
        self.calculate_change() 

    def save_to_csv(self, data):
        filename = os.path.join(self.data_dir, f"transaksi_{datetime.now().strftime('%Y%m%d')}.csv")
        file_exists = os.path.isfile(filename)
        is_empty = not file_exists or os.path.getsize(filename) == 0 

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if is_empty:
                writer.writerow(["Tanggal", "Waktu", "Nama Kasir", "Pelanggan", "Nama Item", "Varian", "Jumlah", "Harga Satuan", "Subtotal Item", "Total Pesanan", "Grand Total", "Jumlah Bayar", "Kembalian"])
            if data['items']:
                for i, item_detail in enumerate(data['items']):
                    varian_display = item_detail['option'] if item_detail['option'] and item_detail['option'] != "Default" else "-"
                    if i == 0:
                        row = [data['tanggal'], data['waktu'], data['nama_kasir'], data.get('table_number', 'None'), item_detail['name'], varian_display, item_detail['qty'], item_detail['price'], item_detail['qty'] * item_detail['price'], data['total_pesanan'], data['grand_total'], data['payment'], data['change']]
                    else:
                        row = ["", "", "", "", item_detail['name'], varian_display, item_detail['qty'], item_detail['price'], item_detail['qty'] * item_detail['price'], "", "", "", ""]
                    writer.writerow(row)

    def run(self):
        self.welcome_page()
        self.root.mainloop()

if __name__ == '__main__':
    app = RestaurantPOS()
    app.run()