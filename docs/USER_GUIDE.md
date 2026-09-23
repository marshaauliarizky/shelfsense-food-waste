# ShelfSense User Guide

## Demo online dan kontak

Kalau tidak ingin menjalankan project secara lokal, buka versi live di [ShelfSense Streamlit Demo](https://shelfsense-food-waste.streamlit.app/).

Untuk pertanyaan atau kolaborasi, hubungi `marshaauliaworks@gmail.com`.

## 1. Menjalankan aplikasi

Jalankan perintah berikut dari folder project:

```powershell
python -m streamlit run app.py
```

Aplikasi akan terbuka di browser lokal. Saat pertama kali dibuka, ShelfSense menampilkan popup pengantar singkat.

## 2. Memahami sidebar

`Navigate` berpindah antar halaman.

`Branch` memfilter data untuk semua cabang atau satu cabang tertentu.

`As of` menentukan tanggal analisis. Tanggal ini dipakai untuk menghitung sisa hari sebelum expiry.

Label `SIMULATED DEMO DATA` berarti angka berasal dari dataset simulasi, bukan data bisnis sungguhan.

## 3. Halaman utama

### Today’s Operations

Halaman ini menjawab pertanyaan: apa yang perlu diperhatikan sekarang?

KPI yang ditampilkan adalah jumlah produksi, sold through rate, waste rate, dan estimated loss. Bagian `Needs attention` menampilkan produk yang memiliki kombinasi stok surplus dan expiry dekat, waste tinggi, atau performa slow moving.

### Waste Monitor

Halaman ini membantu melihat produk, cabang, dan alasan yang paling berkontribusi terhadap waste.

### Markdown Planner

Halaman ini menampilkan produk yang mungkin membutuhkan markdown. User dapat mencatat keputusan manager, status keputusan, dan catatan operasional.

### Production Review

Halaman ini membandingkan produksi, penjualan, waste, dan demand baseline. Demand baseline menggunakan moving average sederhana untuk kebutuhan demo.

### Import Data

Halaman ini digunakan untuk memasukkan data Excel baru ke database.

### Ask ShelfSense

Gunakan pertanyaan terstruktur seperti:

`Which product has the most waste?`

`Which product should get a markdown?`

`What is the estimated loss?`

`Compare waste between Kemang and Senopati.`

### Data Notes

Halaman ini menjelaskan sumber data, definisi metrik, rule engine, dan menyediakan tombol download workbook.

## 4. Fungsi upload Excel

Upload Excel digunakan ketika user ingin memasukkan transaksi baru, bukan untuk mengganti tampilan saja.

Alurnya:

```text
Excel upload
→ normalisasi nama kolom
→ validasi tipe data dan aturan bisnis
→ tampilkan jumlah baris valid dan ditolak
→ simpan baris valid ke SQLite
→ refresh KPI, chart, recommendation, dan chatbot
```

Kolom minimum yang dibutuhkan:

`transaction_id`, `transaction_date`, `transaction_time`, `branch`, `product_id`, `product_name`, `category`, `production_qty`, `sold_qty`, `waste_qty`, `stock_qty`, `unit_price`, `unit_cost`, `discount_pct`, `expiry_date`, dan `shelf_life_days`.

Sistem menolak quantity negatif, transaction ID duplikat, tanggal invalid, discount di luar rentang 0 sampai 100, serta kondisi sold quantity ditambah waste quantity yang melebihi production quantity.

## 5. Mengapa angka dan rekomendasi bisa muncul

`Sold through rate` dihitung dari sold quantity dibagi production quantity.

`Waste rate` dihitung dari waste quantity dibagi production quantity.

`Estimated loss` dihitung dari waste quantity dikali unit cost.

Markdown 20 persen muncul ketika expiry tersisa maksimal 1 hari dan stok lebih besar daripada demand baseline.

Markdown 10 persen muncul ketika expiry tersisa 2 hari dan stok masih surplus.

Pengurangan produksi disarankan ketika waste rate produk melewati 10 persen selama minimal 3 hari berturut turut.

Semua nilai dampak promo adalah estimated. Hasil aktual harus dimasukkan secara terpisah.

## 6. File yang bisa dilihat manual

`data/sample_food_waste.xlsx` adalah data simulasi mentah.

`data/shelfsense.db` adalah database lokal SQLite.

`exports/ShelfSense_demo_workbook.xlsx` adalah workbook dengan sheet Transactions, KPI Summary, Waste by Product, dan Recommendations.
