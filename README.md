# Tugas 2 Komputasi Berbasis Jaringan - Job Queue dengan Celery & RabbitMQ

Proyek ini mengimplementasikan arsitektur *Message Brokering* dan *Job Queue* menggunakan **Celery** dan **RabbitMQ**, mencakup uji coba tiga skema *routing* pesan (*Fan-Out*, *Topic*, dan *Wildcard*) serta migrasi sistem *Client–Broker–Worker* dari proyek UTS ke ekosistem Celery.

---

## 1. Perbandingan Pola Routing Pesan (AMQP Exchange)

| Skema Routing | Tipe Exchange | Mekanisme Kerja | Contoh Konfigurasi & Hasil Uji Coba |
| :--- | :--- | :--- | :--- |
| **Fan-Out** | `fanout` | Mengirimkan salinan pesan secara massal (*broadcast*) ke seluruh antrean (*queue*) yang terikat pada *exchange* tanpa memfilter *routing key*. | Pesan `"Peringatan Sistem!"` dikirim ke `ex_fanout`, sehingga otomatis diterima oleh `q_fanout_1` dan `q_fanout_2` secara bersamaan. |
| **Topic (Exact Match)** | `topic` | Mengarahkan pesan secara spesifik hanya ke antrean yang memiliki *routing key* sama persis dengan pola kata berpemisah titik (`.`). | Antrean `q_topic_spesifik` dengan kunci `sensor.suhu.ruang1` hanya menerima pesan dengan kunci persis `sensor.suhu.ruang1`. |
| **Wildcard (`*` dan `#`)** | `topic` | Penyortiran pola fleksibel menggunakan karakter pengganti:<br>• `*` menggantikan tepat **satu kata**.<br>• `#` menggantikan **nol atau lebih kata**. | • `sensor.suhu.*` menangkap `sensor.suhu.ruang1` dan `sensor.suhu.ruang2`.<br>• `sensor.#` menangkap seluruh pesan berawalan `sensor.` termasuk `sensor.kelembapan.gudang`. |

---

## 2. Arsitektur Aplikasi UTS pada Celery
* **Producer (`producer.py`):** Bertindak sebagai *input generator* otomatis yang membangkitkan 10 permintaan JSON acak dengan tipe tugas `SHORT` (pemrosesan cepat) dan `LONG` (simulasi komputasi berat), lalu mengirimkannya secara asinkron ke *broker* menggunakan `.delay()`.
* **Message Broker (RabbitMQ):** Menampung antrean tugas (`celery`, `q_fanout_1`, `q_fanout_2`, `q_topic_spesifik`, `q_wildcard_bintang`, `q_wildcard_pagar`).
* **Worker (`tasks.py`):** Mengeksekusi fungsi pemrosesan tugas di latar belakang berdasarkan `app_id` yang diterima dan mengembalikan respons berstatus `OK`.

---

## 3. Cara Menjalankan Proyek (Windows)

1. **Jalankan RabbitMQ melalui Docker:**
   ```cmd
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```
2. **Aktifkan Virtual Environment & Instal Dependensi:**
   ```cmd
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Jalankan Celery Worker (Terminal 1):**
   ```cmd
   celery -A tasks worker --loglevel=INFO --pool=solo -Q celery,q_fanout_1,q_fanout_2,q_topic_spesifik,q_wildcard_bintang,q_wildcard_pagar
   ```
4. **Jalankan Producer / Input Generator (Terminal 2):**
   ```cmd
   python producer.py
   ```
