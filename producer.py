import time
import random
from tasks import proses_fanout_1, proses_fanout_2, proses_topic, proses_uts

def uji_fanout():
    print("\n--- 1. MENGUJI FAN-OUT ---")
    proses_fanout_1.apply_async(args=["Peringatan Sistem!"], exchange='ex_fanout')
    proses_fanout_2.apply_async(args=["Peringatan Sistem!"], exchange='ex_fanout')

def uji_topic_dan_wildcard():
    print("\n--- 2. MENGUJI TOPIC & WILDCARD ---")
    proses_topic.apply_async(args=["Suhu Ruang 1 = 30C"], exchange='ex_topic', routing_key='sensor.suhu.ruang1')
    proses_topic.apply_async(args=["Suhu Ruang 2 = 28C"], exchange='ex_topic', routing_key='sensor.suhu.ruang2')
    proses_topic.apply_async(args=["Kelembapan Gudang = 75%"], exchange='ex_topic', routing_key='sensor.kelembapan.gudang')

def jalankan_input_generator_uts():
    print("\n--- 3. INPUT GENERATOR UTS (SHORT & LONG) ---")
    pilihan_app = ["SHORT", "LONG"]
    
    for i in range(1, 11):
        # Membangkitkan 10 data masukan otomatis sesuai format JSON UTS kamu
        jenis_dipilih = random.choice(pilihan_app)
        if jenis_dipilih == "SHORT":
            isi = f"Tes kirim pesan pendek ke-{i}"
        else:
            isi = f"Hitung data baris {random.randint(10000, 99999)}"
            
        format_kirim = {"app_id": jenis_dipilih, "data": isi}
        
        # Mengirim ke worker Celery secara asinkron
        proses_uts.delay(format_kirim)
        print(f"[PRODUCER] Request ke-{i} dikirim: {format_kirim}")
        time.sleep(0.3)

if __name__ == "__main__":
    uji_fanout()
    time.sleep(1)
    uji_topic_dan_wildcard()
    time.sleep(1)
    jalankan_input_generator_uts()
