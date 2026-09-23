# ShelfSense Project Map

## Root

`app.py` adalah entry point aplikasi Streamlit. `requirements.txt` berisi dependency. `README.md` menjelaskan cara menjalankan project.

## Source code

`src/data_loader.py` membaca dan memvalidasi Excel.

`src/database.py` membuat SQLite, menyimpan transaksi, dan menyimpan keputusan manager.

`src/analytics.py` menghitung KPI, moving average, risiko expiry, dan perbandingan periode.

`src/decision_engine.py` menghasilkan rekomendasi yang deterministic dan dapat dijelaskan.

`src/chatbot.py` menyediakan pertanyaan terstruktur yang mengambil angka dari analytics.

`src/charts.py` berisi chart Plotly.

`src/ui.py` berisi format mata uang dan komponen status.

## Data and visual assets

`data/sample_food_waste.xlsx` adalah dataset simulasi utama.

`data/shelfsense.db` adalah database lokal yang dibuat saat aplikasi berjalan.

`exports/ShelfSense_demo_workbook.xlsx` adalah hasil export yang bisa dibuka manual di Excel atau LibreOffice.

`assets/shelfsense-hero.png` adalah visual hero dashboard.

`assets/bakery-product-board.png` adalah product board untuk halaman Markdown Planner.

`assets/chart-sales-waste.png` dan `assets/chart-waste-reasons.png` adalah snapshot chart untuk dokumentasi portfolio.

## Tools and tests

`scripts/generate_sample_data.py` membuat ulang dataset simulasi.

`scripts/export_database.py` membuat workbook export dari database.

`scripts/export_chart_images.py` membuat snapshot chart PNG dari database.

`tests/` berisi unit test dan integration test.

Folder `pytest-cache-files-*`, `__pycache__`, dan file database test bukan bagian dari product output.
