<div align="center">

# 🍽️ Tkinter POS System — Pawone Simbah Restaurant

### *Sistem Kasir Restoran yang Cepat, Rapi, dan Mudah Digunakan*

Aplikasi **Point of Sale (POS)** desktop untuk restoran, dibangun dengan Python, Tkinter, dan ttkbootstrap. Dirancang khusus untuk mempercepat alur pemesanan menu, perhitungan pembayaran, hingga pencetakan struk — semua dalam satu antarmuka bertema gelap yang modern.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20%2B%20ttkbootstrap-FFD43B?style=flat-square&logo=python&logoColor=blue)
![Pillow](https://img.shields.io/badge/Image-Pillow%20(PIL)-9C27B0?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Desktop-informational?style=flat-square)
![License](https://img.shields.io/badge/License-Open%20Source-green?style=flat-square)

</div>

---

## 💡 Tentang Proyek

> *"Kasir yang cepat adalah pelayanan pertama yang dirasakan pelanggan."*

**Pawone Simbah Restaurant POS** adalah sistem kasir yang dirancang agar staf dapat memproses pesanan hanya dengan beberapa kali klik, mulai dari memilih menu bergambar, menentukan varian rasa, menghitung kembalian secara otomatis, hingga mencetak struk dan menyimpan riwayat transaksi harian.

| 🎯 Tujuan | 📈 Manfaat |
|---|---|
| Mempercepat proses input pesanan | Antrean pelanggan lebih singkat |
| Mendukung varian menu (rasa, ukuran, dll.) | Fleksibel untuk berbagai preferensi pelanggan |
| Menghitung pembayaran & kembalian otomatis | Minim kesalahan hitung manual |
| Menyimpan riwayat transaksi ke CSV | Rekap penjualan harian lebih mudah |

## ✨ Fitur Utama

- 🔐 **Login Kasir** — autentikasi nama kasir & password sebelum mengakses sistem
- 🖼️ **Tampilan Menu Bergambar** — menu ditampilkan dalam bentuk kartu (card) dengan foto produk
- 🗂️ **Kategori Menu** — filter cepat berdasarkan kategori *Makanan*, *Minuman*, dan *Cemilan*
- 🔍 **Pencarian Menu Real-time** — cari item hanya dengan mengetik nama menu
- 🎛️ **Pilihan Varian Menu** — dialog interaktif untuk memilih varian (misal: Pedas/Original) & jumlah
- 🛒 **Keranjang Pesanan Dinamis** — tambah, ubah kuantitas, dan hapus item langsung dari tabel pesanan
- 💰 **Kalkulasi Otomatis** — total belanja, jumlah bayar, dan kembalian dihitung *real-time*
- 🧾 **Cetak Struk Digital** — struk transaksi ditampilkan rapi lengkap dengan rincian item & kembalian
- 💾 **Riwayat Transaksi Otomatis** — setiap transaksi tersimpan ke file CSV harian (`data/transaksi_YYYYMMDD.csv`)
- 🎨 **Tema Antarmuka Gelap (Darkly)** — tampilan modern menggunakan `ttkbootstrap`

## 🛠️ Tech Stack

<div align="center">

| Layer | Teknologi |
|:---:|:---:|
| **Bahasa** | Python 3 |
| **GUI Framework** | Tkinter + ttkbootstrap (tema `darkly`) |
| **Pengolahan Gambar** | Pillow (PIL) |
| **Penyimpanan Data** | CSV (built-in `csv` module) |
| **Struktur Kode** | Object-Oriented (class `RestaurantPOS`) |

</div>

## 📦 Instalasi & Menjalankan

```bash
# 1. Clone repository
git clone https://github.com/alnafs23/Tkinter-POS-System.git
cd Tkinter-POS-System

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install ttkbootstrap pillow

# 4. Jalankan aplikasi
python main.py
```

> ⚠️ Pastikan seluruh file gambar menu (misalnya `Nasi Goreng.jpg`, `Ayam.jpg`, `bc1.jpg`, dll.) berada di direktori yang sama dengan skrip utama agar gambar tampil dengan benar.

## 🖥️ Cara Penggunaan

1. Jalankan aplikasi, lalu masukkan **nama kasir** dan **password** pada halaman login
2. Setelah berhasil login, pilih kategori menu (*Semua*, *Makanan*, *Minuman*, *Cemilan*) atau gunakan kolom pencarian
3. Klik gambar menu yang diinginkan — jika menu memiliki varian, akan muncul dialog pilihan varian & jumlah
4. Item yang dipilih otomatis masuk ke **keranjang pesanan** di sisi kanan layar
5. Masukkan **nominal pembayaran** — total dan kembalian akan terhitung otomatis
6. Klik **"Cetak Struk & Simpan"** untuk menampilkan struk dan menyimpan transaksi ke riwayat harian

## 🔑 Akses Login

Aplikasi menggunakan daftar password kasir yang telah ditentukan di dalam kode (`valid_passwords`). Sesuaikan atau tambahkan password sesuai kebutuhan staf restoran Anda.

## 📁 Struktur Proyek

```
Tkinter-POS-System/
├── main.py                       # Entry point aplikasi (class RestaurantPOS)
├── data/                          # Riwayat transaksi harian (dibuat otomatis)
│   └── transaksi_YYYYMMDD.csv
├── *.jpg / *.jpeg                # Aset gambar menu & latar belakang
└── README.md                      # Dokumentasi proyek
```

## 🗺️ Rencana Pengembangan

- [ ] Manajemen menu dinamis (tambah/edit/hapus menu tanpa mengubah kode)
- [ ] Integrasi cetak struk ke printer thermal fisik
- [ ] Laporan rekap penjualan harian/bulanan dalam bentuk dashboard
- [ ] Sistem hak akses multi-level (kasir vs admin)
- [ ] Migrasi penyimpanan data ke database (SQLite)

## 🤝 Kontribusi

Kontribusi sangat terbuka bagi siapa saja yang ingin membantu mengembangkan proyek ini:

1. *Fork* repository ini
2. Buat branch fitur baru (`git checkout -b fitur-baru`)
3. *Commit* perubahan (`git commit -m 'Menambahkan fitur baru'`)
4. *Push* ke branch (`git push origin fitur-baru`)
5. Buka *Pull Request*

## 📄 Lisensi

Proyek ini bersifat **open source** dan bebas digunakan untuk keperluan pembelajaran maupun pengembangan lebih lanjut.

---

<div align="center">

**Dibuat dengan 💙 oleh [alnafs23](https://github.com/alnafs23)**

</div>
