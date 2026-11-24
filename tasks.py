import time
from celery import Celery

app = Celery('tugas_kbj')
app.config_from_object('celeryconfig')

# --- TUGAS UJI COBA 3 SKEMA ROUTING ---
@app.task(name='tasks.proses_fanout_1')
def proses_fanout_1(pesan):
    print(f"[FAN-OUT 1] Menerima siaran: {pesan}")
    return f"Fanout 1 selesai: {pesan}"

@app.task(name='tasks.proses_fanout_2')
def proses_fanout_2(pesan):
    print(f"[FAN-OUT 2] Menerima siaran: {pesan}")
    return f"Fanout 2 selesai: {pesan}"

@app.task(name='tasks.proses_topic')
def proses_topic(data):
    print(f"[TOPIC / WILDCARD] Memproses data: {data}")
    time.sleep(1)
    return f"Data diproses: {data}"

# --- LOGIKA PROGRAM  (SHORT & LONG) ---
@app.task(name='tasks.proses_uts')
def proses_uts(pesan_json):
    jenis_app = pesan_json.get("app_id")
    isi_data = pesan_json.get("data")
    print(f"[UTS WORKER] Dapat orderan '{jenis_app}', datanya: {isi_data}")

    if jenis_app == "LONG":
        time.sleep(1)
        hasilnya = f"Sukses hitung rumus rumit untuk data {isi_data}"
    elif jenis_app == "SHORT":
        hasilnya = f"Echo balik: {isi_data}"
    else:
        hasilnya = "App ID salah!"

    respon = {"status": "OK", "result": hasilnya}
    print(f"[UTS WORKER] Selesai -> {respon}")
    return respon
