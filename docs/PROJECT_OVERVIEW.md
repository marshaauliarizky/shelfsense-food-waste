# ShelfSense Project Overview

## Project ini tentang apa

ShelfSense adalah sistem analitik operasional untuk bakery atau retail food store. Tujuannya membantu tim memahami produk apa yang berisiko tidak terjual, kapan markdown masuk akal, dan kapan produksi perlu dikurangi.

Project ini tidak berfokus pada chatbot AI bebas. Fokusnya adalah menghubungkan data dengan keputusan operasional yang dapat dijelaskan.

## Mengapa project ini dibuat

Bisnis bakery menghadapi trade off antara ketersediaan produk dan waste. Produksi terlalu sedikit menyebabkan stockout. Produksi terlalu banyak menghasilkan makanan yang tidak terjual. ShelfSense memperlihatkan trade off tersebut melalui data produksi, penjualan, stok, shelf life, expiry, dan markdown.

## Mengapa hasilnya bisa seperti itu

Dataset dibuat sebagai simulasi portfolio dengan beberapa pola operasional yang realistis.

Weekend memiliki demand lebih tinggi.

Hujan menurunkan demand pada beberapa produk.

Beberapa produk sengaja mengalami overproduction.

Pastry dengan shelf life pendek lebih mudah masuk ke markdown window.

Diskon tidak selalu menyelesaikan masalah. Produk yang tetap lambat terjual setelah diskon ditandai sebagai slow moving.

Karena itu, hasil dashboard tidak selalu positif. Ada hari dengan waste tinggi, cabang dengan performa lebih buruk, dan produk yang memiliki revenue lebih rendah setelah markdown. Pola tersebut sengaja dibuat agar demo menunjukkan proses analitik, bukan sekadar angka yang terlihat sempurna.

## Cara membaca kualitas hasil

Dashboard tidak mengklaim bahwa simulasi ini adalah hasil bisnis nyata. Setiap impact diberi label estimated. Keputusan manager dan hasil aktual disimpan sebagai data terpisah agar rekomendasi dapat dibandingkan dengan kenyataan.

## Arsitektur singkat

Excel masuk melalui data loader. Data yang valid disimpan ke SQLite. Analytics menghitung KPI dan demand baseline. Decision engine mengubah kondisi menjadi recommendation. Streamlit menampilkan hasil tersebut dalam dashboard. Chatbot hanya mengakses fungsi analytics dan recommendation yang telah ditentukan.

## Batasan

MVP menggunakan moving average, bukan machine learning forecasting. SQLite ditujukan untuk demo lokal. Chatbot hanya mendukung pertanyaan terstruktur. Dataset bukan data bisnis nyata.
