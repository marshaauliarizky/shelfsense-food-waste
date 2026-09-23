# ShelfSense — Food Waste Prevention & Dynamic Pricing

**Tanggal:** 2026-09-22  
**Status:** Design spec untuk MVP portfolio  
**Target:** Demo lokal berbasis Streamlit dengan data simulasi yang realistis

## 1. Ringkasan

ShelfSense adalah dashboard operasional untuk membantu bakery atau retail food store mengurangi makanan yang tidak terjual. Aplikasi menggabungkan data produksi, penjualan, stok, expiry, markdown, dan alasan waste untuk menghasilkan tiga jenis bantuan:

1. pemantauan kondisi operasional hari ini;
2. deteksi produk yang berisiko menjadi waste;
3. rekomendasi tindakan yang dapat dijelaskan, seperti markdown atau pengurangan produksi.

MVP ini ditujukan untuk portfolio. Semua data yang disediakan adalah data simulasi dan harus diberi label sebagai simulated/demo data. Sistem tidak boleh menyajikan estimasi sebagai hasil aktual.

## 2. Masalah dan tujuan

### Masalah

Bisnis makanan dengan shelf life pendek harus menyeimbangkan produksi, ketersediaan produk, penjualan, harga markdown, dan risiko expiry. Dashboard biasa hanya menunjukkan angka historis, tetapi belum menjawab produk mana yang perlu ditangani dan mengapa.

### Tujuan MVP

- Membuat data operasional mudah diimpor dan divalidasi.
- Menghasilkan KPI waste dan penjualan yang dapat ditelusuri ke data sumber.
- Menandai produk yang membutuhkan perhatian hari ini.
- Memberi rekomendasi markdown atau perubahan produksi berbasis rule.
- Menunjukkan estimasi dampak tanpa menyamarkan simulasi sebagai fakta.
- Membuat demo portfolio yang mudah dijalankan dan mudah dipahami reviewer.

### Bukan tujuan MVP

- Forecasting machine learning production-grade.
- Optimasi harga real-time untuk pelanggan individual.
- Integrasi POS, payment gateway, atau supplier.
- LLM bebas yang dapat mengakses seluruh database tanpa batasan.
- Klaim pengurangan waste pada bisnis nyata.

## 3. Dasar domain dan sumber referensi

Desain metrik mengikuti prinsip bahwa pengukuran waste harus memiliki baseline, definisi yang konsisten, dan perbandingan antarperiode. UNEP merekomendasikan pengukuran yang dapat digunakan untuk memantau perubahan dari waktu ke waktu dan membedakan konteks retail serta food service.

Referensi utama:

- [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024)
- [UNEP SDG Indicator 12.3.1(b)](https://www.unep.org/indicator-1231b)
- [U.S. Food Waste Pact 2025 Data Report](https://foodwastepact.refed.org/resources/2025-data-report/)
- [Effects of dynamic pricing of perishable products on revenue and waste](https://doi.org/10.1016/S0305-750X(16)30396-6)
- [Dynamic Pricing and Organic Waste Bans](https://pubsonline.informs.org/doi/10.1287/mksc.2020.0214)

Referensi tersebut digunakan untuk membentuk konsep KPI dan faktor rekomendasi, bukan untuk mengklaim bahwa rule MVP ini merupakan model optimal atau hasil penelitian yang direplikasi.

## 4. Pengguna dan skenario utama

### Persona

- **Store manager:** ingin tahu produk yang harus ditangani sebelum toko tutup.
- **Supervisor produksi:** ingin membandingkan rencana produksi dengan permintaan aktual.
- **Inventory staff:** ingin melihat stok mendekati expiry dan mencatat waste.
- **Portfolio reviewer:** ingin melihat hubungan antara masalah bisnis, data, analitik, dan keputusan.

### Skenario utama

1. User membuka aplikasi dan langsung melihat kondisi operasional hari ini.
2. User memilih tanggal dan cabang.
3. User melihat produk berisiko waste beserta angka pendukung dan tindakan yang disarankan.
4. User mengimpor file Excel dan menerima ringkasan validasi.
5. User memasukkan transaksi atau waste secara manual.
6. User menanyakan pertanyaan terstruktur melalui Ask ShelfSense.
7. User membandingkan hasil aktual setelah markdown dengan estimasi awal.

## 5. Arah visual dan UX

### Konsep

Nama aplikasi: **ShelfSense**  
Tagline: **A clearer view of what should sell, what may spoil, and what to do next.**

Tampilan harus terasa seperti internal operations console untuk bakery modern, bukan template dashboard AI.

### Prinsip visual

- Palet charcoal, cream, muted green, dan amber.
- Tipografi sederhana dan hierarki kuat.
- Sidebar kecil untuk navigasi dan filter.
- Ruang kosong yang cukup; tidak memenuhi layar dengan chart.
- Tidak menggunakan neon gradient, robot icon, atau klaim “AI-powered”.
- Status menggunakan label `High priority`, `Watch`, dan `No action`.
- Copywriting memakai bahasa operasional: `Markdown window`, `Production note`, `Likely driver`, dan `Manager action`.

### Halaman

#### A. Today’s Operations

Komponen:

- filter tanggal dan cabang;
- KPI total produksi, sold-through rate, waste rate, estimated loss;
- daftar `Needs attention`;
- panel `What changed?` dibandingkan periode pembanding;
- grafik 7 hari penjualan dan waste;
- catatan bahwa data bersifat simulasi.

#### B. Waste Monitor

Komponen:

- tren waste harian;
- waste berdasarkan `waste_reason`;
- produk penyumbang waste terbesar;
- perbandingan waste rate antar-cabang;
- tabel detail produk dan transaksi terkait.

#### C. Markdown Planner

Komponen:

- daftar rekomendasi berdasarkan prioritas;
- stok tersisa, forecast sampai tutup, expiry days, dan markdown yang disarankan;
- alasan rekomendasi;
- estimated units saved dan estimated revenue;
- form untuk mencatat keputusan manager;
- form untuk memasukkan hasil aktual setelah promo.

#### D. Production Review

Komponen:

- actual versus planned production;
- produk yang terlalu banyak diproduksi;
- produk yang sering stockout;
- moving average sebagai baseline demand;
- catatan pola weekday/weekend.

#### E. Ask ShelfSense

Chatbot menggunakan pertanyaan terstruktur dan fungsi query terbatas. Pertanyaan contoh:

- `What needs attention before closing?`
- `Why is sourdough flagged today?`
- `Compare waste between Kemang and Senopati.`
- `Which product should get an early markdown?`

Jawaban wajib menyebut periode, cabang bila relevan, angka utama, dan alasan. Jika data tidak tersedia, jawab dengan keterbatasan yang jelas.

#### F. Data Notes

Halaman dokumentasi kecil yang menjelaskan definisi KPI, sumber dataset, arti estimated versus actual, dan keterbatasan rule engine.

## 6. Arsitektur teknis

MVP menggunakan aplikasi Streamlit terstruktur dalam satu repository:

```text
app.py
src/
  config.py
  database.py
  data_loader.py
  analytics.py
  decision_engine.py
  chatbot.py
  charts.py
  ui.py
data/
  sample_food_waste.xlsx
tests/
  test_data_loader.py
  test_analytics.py
  test_decision_engine.py
  test_chatbot.py
requirements.txt
README.md
```

Tanggung jawab modul:

- `config.py`: path database, nama kolom, dan konfigurasi demo.
- `database.py`: inisialisasi SQLite, insert/upsert, query transaksi, dan penyimpanan keputusan.
- `data_loader.py`: baca Excel, normalisasi nama kolom, validasi, dan menghasilkan error report.
- `analytics.py`: KPI, demand baseline, risk metrics, dan agregasi.
- `decision_engine.py`: rule-based recommendation dengan output terstruktur.
- `chatbot.py`: intent matching dan pemanggilan fungsi analitik yang diizinkan.
- `charts.py`: fungsi chart Plotly yang menerima DataFrame bersih.
- `ui.py`: komponen tampilan bersama, cards, status badge, dan format angka.
- `app.py`: routing halaman dan state Streamlit.

## 7. Model data

Tabel utama `transactions` memiliki kolom:

```text
transaction_id       TEXT PRIMARY KEY
transaction_date     DATE NOT NULL
transaction_time     TIME NOT NULL
branch               TEXT NOT NULL
product_id           TEXT NOT NULL
product_name         TEXT NOT NULL
category             TEXT NOT NULL
production_qty       INTEGER NOT NULL
sold_qty             INTEGER NOT NULL
waste_qty            INTEGER NOT NULL
stock_qty            INTEGER NOT NULL
unit_price           REAL NOT NULL
unit_cost            REAL NOT NULL
discount_pct         REAL NOT NULL DEFAULT 0
expiry_date          DATE NOT NULL
shelf_life_days      INTEGER NOT NULL
forecast_qty         REAL
weather              TEXT
event_flag           INTEGER NOT NULL DEFAULT 0
waste_reason         TEXT
actual_markdown_revenue REAL
created_at           DATETIME NOT NULL
```

Tabel `manager_decisions` memiliki kolom:

```text
decision_id          INTEGER PRIMARY KEY AUTOINCREMENT
transaction_id       TEXT NOT NULL
decision_type        TEXT NOT NULL
decision_status      TEXT NOT NULL
recommended_discount REAL
actual_discount      REAL
manager_note         TEXT
actual_sold_qty      INTEGER
actual_waste_qty     INTEGER
created_at           DATETIME NOT NULL
```

Constraint penting:

- quantity tidak boleh negatif;
- `sold_qty + waste_qty` tidak boleh melebihi `production_qty` untuk record harian yang sama;
- `discount_pct` berada pada rentang 0–100;
- `unit_price` dan `unit_cost` lebih besar dari 0;
- `expiry_date` tidak boleh kosong;
- `transaction_id` tidak boleh duplikat;
- `branch`, `product_id`, dan `product_name` wajib terisi.

## 8. Definisi metrik

```text
sold_through_rate = sold_qty / production_qty
waste_rate = waste_qty / production_qty
estimated_loss = waste_qty * unit_cost
gross_revenue = sold_qty * unit_price * (1 - discount_pct / 100)
markdown_revenue = sold_qty * unit_price * (1 - actual_discount / 100)
stock_gap = stock_qty - forecast_qty
```

Semua pembagian harus aman ketika denominator bernilai nol. Dalam kasus tersebut, nilai ditampilkan sebagai `—`, bukan infinity atau error.

Perbandingan periode default menggunakan 7 hari terakhir dibandingkan 7 hari sebelumnya. Label harus menyebutkan periode yang dipakai.

## 9. Decision engine

Decision engine versi MVP bersifat deterministic dan explainable. Output setiap rekomendasi:

```python
{
    "product_id": str,
    "priority": "high" | "watch" | "no_action",
    "issue": str,
    "evidence": list[str],
    "action": str,
    "suggested_discount_pct": float | None,
    "estimated_units_saved": float,
    "estimated_revenue": float,
}
```

Aturan awal:

1. Jika `expiry_days <= 1` dan `stock_qty > forecast_qty`, rekomendasikan markdown prioritas tinggi.
2. Jika `waste_rate > 0.10` selama minimal 3 hari berturut-turut, rekomendasikan pengurangan produksi.
3. Jika rata-rata `sold_qty` melebihi `forecast_qty` secara konsisten, rekomendasikan penambahan produksi.
4. Jika `discount_pct >= 20` dan sold-through tetap di bawah 50%, tandai sebagai slow-moving.
5. Jika `stock_qty <= forecast_qty` dan tidak mendekati expiry, jangan sarankan markdown.

Besaran markdown default:

- expiry 0–1 hari: 20%;
- expiry 2 hari dengan surplus: 10%;
- tidak ada risiko expiry: tidak ada markdown.

Rule tidak boleh menyatakan bahwa waste pasti akan berkurang. Gunakan kata `estimated`, dan simpan hasil aktual terpisah dari rekomendasi.

## 10. Chatbot terbatas

Chatbot MVP melakukan intent matching sederhana, bukan generative AI. Intent minimum:

- `top_waste_product`;
- `highest_waste_branch`;
- `today_markdown_recommendations`;
- `estimated_loss_period`;
- `product_reason`;
- `weekday_weekend_comparison`.

Setiap intent memanggil fungsi di `analytics.py` atau `decision_engine.py`. Chatbot tidak boleh membuat SQL bebas dari input user dan tidak boleh menjawab angka yang tidak berasal dari query.

Jika pertanyaan tidak cocok dengan intent yang tersedia, chatbot menampilkan daftar pertanyaan yang didukung.

## 11. Dataset simulasi

Dataset mencakup setidaknya:

- 3 cabang: Kemang, Senopati, dan BSD;
- periode minimal 8 minggu;
- 10–15 produk bakery;
- kategori pastry, bread, cake, dan savory;
- variasi weekday/weekend;
- variasi cuaca dan event;
- produk dengan shelf life pendek;
- beberapa pola overproduction, stockout, dan slow-moving;
- transaksi sebelum dan sesudah markdown.

Dataset tidak boleh terlihat sempurna. Namun, pola dan angka harus tetap konsisten dengan constraint data. README harus menyebutkan bahwa data dibuat untuk demonstrasi dan bukan data bisnis nyata.

## 12. Error handling

Import Excel harus menampilkan:

- jumlah baris berhasil;
- jumlah baris ditolak;
- daftar kolom wajib yang hilang;
- alasan penolakan per baris;
- jumlah duplikasi;
- preview baris bermasalah.

Input manual harus menampilkan error inline dan tidak menyimpan record sampai seluruh validasi lolos.

Database harus menggunakan transaksi saat import batch. Jika validasi batch gagal pada konfigurasi strict, tidak boleh ada sebagian data yang tersimpan.

## 13. Testing dan acceptance criteria

Unit test minimum:

- validasi menolak kolom wajib yang hilang;
- validasi menolak quantity negatif;
- validasi menolak duplicate `transaction_id`;
- validasi menolak `sold_qty + waste_qty > production_qty`;
- KPI menghitung waste rate dan estimated loss dengan benar;
- KPI tidak error ketika production bernilai nol;
- rule expiry menghasilkan priority high pada kondisi yang sesuai;
- rule slow-moving tidak menghasilkan markdown jika tidak ada surplus;
- chatbot menjawab intent yang didukung dari data aktual;
- chatbot menolak pertanyaan di luar scope dengan fallback yang jelas.

Acceptance criteria aplikasi:

- `streamlit run app.py` membuka aplikasi tanpa error;
- sample dataset dapat dimuat dari keadaan awal;
- upload data valid memperbarui KPI dan chart;
- upload data invalid tidak merusak database;
- rekomendasi menampilkan evidence dan action;
- estimated impact dibedakan secara visual dari actual result;
- semua halaman memiliki label simulated/demo data;
- README menjelaskan instalasi, penggunaan, arsitektur, KPI, dan keterbatasan.

## 14. Risiko dan batasan

- Data simulasi tidak dapat membuktikan dampak bisnis nyata.
- Rule-based recommendation tidak menggantikan forecasting atau pricing optimization.
- `forecast_qty` MVP memakai moving average, bukan model ML.
- Perhitungan estimated revenue bersifat ilustratif dan tidak memasukkan seluruh biaya operasional.
- Chatbot hanya menjawab intent yang telah didefinisikan.
- SQLite cocok untuk demo lokal, bukan deployment multi-user.

## 15. Definisi selesai

MVP dianggap selesai jika user dapat menjalankan aplikasi lokal, melihat dashboard dari sample dataset, mengimpor data baru, mencatat keputusan markdown, menerima rekomendasi yang dapat dijelaskan, dan menggunakan chatbot untuk pertanyaan yang didukung. Seluruh fungsi utama harus memiliki test otomatis dan README harus menjelaskan bahwa hasil berasal dari simulated data.
