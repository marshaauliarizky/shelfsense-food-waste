# ShelfSense Project Walkthrough

Dokumen ini menjelaskan project ShelfSense dari awal sampai akhir. Source code tersedia di GitHub dan aplikasi sudah dipublish sebagai demo Streamlit.

**Live demo:** https://shelfsense-food-waste.streamlit.app/  
**Kontak:** marshaauliaworks@gmail.com

## 1. ShelfSense itu apa

ShelfSense adalah dashboard operasional untuk bakery atau toko makanan dengan produk yang memiliki masa simpan pendek.

Dashboard ini membantu menjawab pertanyaan berikut:

1. Berapa banyak produk yang diproduksi dan terjual?
2. Produk mana yang menghasilkan waste paling besar?
3. Cabang mana yang memiliki waste rate lebih tinggi?
4. Produk mana yang masih memiliki stok berlebih menjelang expiry?
5. Kapan markdown dapat dipertimbangkan?
6. Kapan produksi perlu dikurangi?

Fokus utama project ini adalah menghubungkan data dengan keputusan yang dapat dijelaskan. Chatbot hanya menjadi akses cepat ke fungsi analytics, bukan chatbot bebas.

## 2. Apa saja yang sudah dibuat

Web dibuat menggunakan Streamlit dan memiliki halaman berikut:

1. `Today's Operations` menampilkan KPI, perubahan waste, dan produk yang perlu perhatian.
2. `Waste Monitor` menampilkan waste berdasarkan produk, cabang, dan alasan.
3. `Markdown Planner` menampilkan rekomendasi markdown dan form keputusan manager.
4. `Production Review` membandingkan produksi dengan demand baseline.
5. `Import Data` memasukkan transaksi baru dari Excel.
6. `Ask ShelfSense` menjawab pertanyaan terstruktur dari data yang sedang dipilih.
7. `Data Notes` menjelaskan definisi metrik dan menyediakan workbook export.

Tampilan sudah dilengkapi hero section, gambar bakery, popup pengantar, animasi, hover state, sidebar filter, popover bantuan, chart, dan recommendation card.

## 3. Alur data aplikasi

```text
sample_food_waste.xlsx
        |
        v
data_loader.py
        |
        v
validasi data
        |
        v
shelfsense.db
        |
        v
analytics.py
        |
        v
decision_engine.py
        |
        v
dashboard.py dan Streamlit UI
```

Saat aplikasi dijalankan, database lokal dibuka terlebih dahulu. Jika belum berisi transaksi, dataset Excel simulasi dimuat dan baris yang valid dimasukkan ke SQLite. Setelah itu dashboard membaca database untuk menghitung KPI dan rekomendasi.

## 4. Penjelasan file utama

### `app.py`

Ini adalah entry point aplikasi. File ini sengaja dibuat singkat. Tugasnya hanya mengatur startup Streamlit, memuat data demo, membaca filter, dan memanggil halaman dashboard.

### `src/ui_components.py`

File ini mengatur CSS, animasi, popup pengantar, sidebar, hero section, format mata uang, dan status badge.

### `src/dashboard.py`

File ini berisi renderer untuk setiap halaman dashboard. Pemisahan ini membuat `app.py` tidak menjadi file yang terlalu panjang.

### `src/data_loader.py`

File ini membaca Excel dan memvalidasi data. Sistem memeriksa kolom wajib, angka, tanggal, quantity negatif, duplikasi transaction ID, discount, dan batas produksi.

### `src/database.py`

File ini membuat schema SQLite serta menyimpan dan mengambil transaksi dan manager decisions.

### `src/analytics.py`

File ini menghitung KPI, daily trend, moving average demand baseline, comparison period, dan product risk frame.

### `src/decision_engine.py`

File ini berisi aturan recommendation. Contohnya markdown 20 persen untuk expiry yang sangat dekat dengan stok surplus, markdown 10 persen untuk expiry dua hari, dan review production ketika waste rate tinggi.

### `src/charts.py`

File ini membuat chart Plotly untuk sales, waste, dan waste reason.

### `src/chatbot.py`

File ini memetakan pertanyaan yang didukung ke analytics dan recommendation. Chatbot tidak membuat query database bebas.

## 5. Cara membaca angka

### Sold-through rate

```text
sold quantity / production quantity
```

Menunjukkan bagian produksi yang berhasil terjual.

### Waste rate

```text
waste quantity / production quantity
```

Menunjukkan bagian produksi yang tidak terjual dan menjadi waste.

### Estimated loss

```text
waste quantity × unit cost
```

Menunjukkan estimasi biaya produk yang terbuang. Nilainya bukan laporan keuangan resmi.

### Demand baseline

Demand baseline menggunakan moving average sederhana dari penjualan sebelumnya. Ini cocok untuk demo dan pembelajaran, tetapi belum merupakan forecasting production-grade.

## 6. Mengapa hasil dataset seperti itu

Dataset dibuat sebagai simulasi portfolio. Beberapa pola sengaja dimasukkan:

1. Weekend memiliki demand lebih tinggi.
2. Hujan menurunkan demand pada produk tertentu.
3. Sebagian produk mengalami overproduction.
4. Produk dengan shelf life pendek lebih cepat masuk markdown window.
5. Sebagian produk tetap slow moving walaupun sudah mendapat diskon.

Karena itu, hasil dashboard tidak selalu positif. Tujuannya adalah menunjukkan proses analitik, bukan membuat angka terlihat sempurna.

## 7. Fungsi upload Excel

Upload Excel digunakan untuk menambahkan transaksi baru ke database.

```text
Upload Excel
      |
      v
Normalisasi nama kolom
      |
      v
Validasi data
      |
      v
Baris invalid ditolak
      |
      v
Baris valid disimpan ke SQLite
      |
      v
Dashboard memakai data terbaru
```

Kolom minimum yang diperlukan:

```text
transaction_id, transaction_date, transaction_time, branch,
product_id, product_name, category, production_qty, sold_qty,
waste_qty, stock_qty, unit_price, unit_cost, discount_pct,
expiry_date, shelf_life_days
```

## 8. File data yang bisa dilihat manual

`data/sample_food_waste.xlsx` adalah dataset simulasi mentah.

`data/shelfsense.db` adalah database SQLite lokal yang menyimpan transaksi dan manager decisions.

`exports/ShelfSense_demo_workbook.xlsx` adalah workbook export dengan sheet Transactions, KPI Summary, Waste by Product, dan Recommendations.

## 9. Test dan kualitas saat ini

Unit test dan integration test tersedia di folder `tests`.

```powershell
python -m pytest -q
```

Hasil terakhir yang berhasil diverifikasi adalah:

```text
16 passed
```

## 10. Dokumen yang sudah tersedia

1. `README.md` adalah ringkasan project.
2. `docs/USER_GUIDE.md` menjelaskan cara menggunakan web.
3. `docs/PROJECT_OVERVIEW.md` menjelaskan tujuan dan interpretasi hasil.
4. `docs/PROJECT_MAP.md` menjelaskan struktur folder.
5. `docs/DEPLOYMENT_CHECKLIST.md` menjelaskan persiapan GitHub dan deployment.
6. `docs/ShelfSense_Project_Documentation.docx` adalah dokumentasi Word lengkap.
7. `docs/ShelfSense_Portfolio_Deck_v2.pptx` adalah presentasi portfolio.
8. Dokumen ini menjelaskan project secara menyeluruh.

## 11. Status publish dan catatan deployment

Project sudah diupload ke GitHub dan dipublish ke Streamlit Community Cloud. Link live demo dapat digunakan oleh pembaca yang ingin mencoba aplikasi tanpa menjalankan project secara lokal.

Tetap ingat hal berikut ketika melakukan update:

1. `data/shelfsense.db` adalah database lokal.
2. `__pycache__` dan `.pytest_cache` adalah file sementara.
3. Database lokal dan secret tidak boleh diupload ke GitHub.
4. Dataset simulasi boleh disertakan karena tidak berisi data bisnis nyata.
5. SQLite cocok untuk demo portfolio, tetapi bukan pilihan ideal untuk banyak user secara bersamaan.

Jika aplikasi lama tidak dibuka, Streamlit Community Cloud dapat membuatnya masuk mode tidur. Membuka kembali link live demo akan membangunkannya.

## 12. Cara menjalankan project

Dari folder utama project:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Jika ingin mencoba versi live, buka link demo di bagian atas dokumen. Jika ingin menjalankan versi lokal, gunakan perintah di atas. Gunakan dokumen ini sebagai panduan untuk memahami file, alur data, dan fungsi setiap halaman.
