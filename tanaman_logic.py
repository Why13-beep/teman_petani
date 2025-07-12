import json
import os
from datetime import datetime, timedelta
from plyer import notification

# load json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_jadwal(filename="data_tanaman.json"):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def hitung_jadwal_pemupukan(tanaman: str, tanggal_tanam: str):
    """
    Menghitung tanggal pemupukan berdasarkan tanggal tanam.
    :param tanaman: nama tanaman
    :param tanggal_tanam: string format DD-MM-YYYY
    :return: list tanggal pemupukan
    """
    data_jadwal = load_jadwal()

    if tanaman not in data_jadwal:
        raise ValueError(f"Tanaman {tanaman} tidak ditemukan dalam data.")

    try:
        tanggal_awal = datetime.strptime(tanggal_tanam, "%d-%m-%Y")
        hasil = []

        for fase in data_jadwal[tanaman]:
            hari = fase["hari"]
            if isinstance(hari, int):
                tgl_pupuk = tanggal_awal + timedelta(days=hari)
                hasil.append({
                    "tanggal": tgl_pupuk.strftime("%d-%m-%Y"),
                    "pupuk": fase.get("pupuk", []),
                    "catatan": fase.get("catatan", "")
                })
            elif isinstance(hari, list) and len(hari) == 2 and tanaman in ["cabai", "tomat"]:
                for h in range(hari[0], hari[1] + 1, 14):
                    tgl_pupuk = tanggal_awal + timedelta(days=h)
                    hasil.append({
                        "tanggal": tgl_pupuk.strftime("%d-%m-%Y"),
                        "pupuk": fase.get("pupuk", []),
                        "catatan": fase.get("catatan", "") + f" (Hari ke-{h})"
                    })
            elif isinstance(hari,list) and len(hari) == 2 and tanaman == "padi":
                h = hari[0]
                tgl_pupuk = tanggal_awal + timedelta(days=h)
                hasil.append({
                        "tanggal": tgl_pupuk.strftime("%d-%m-%Y"),
                        "pupuk": fase.get("pupuk", []),
                        "catatan": fase.get("catatan", "") + f" (Hari ke-{h})"
                    })
        return hasil

    except ValueError:
        raise ValueError("Format tanggal_tanam harus DD-MM-YYYY")
    
def cek_alarm_hari_ini(tanaman, tanggal_tanam):
    hari_ini = datetime.today().strftime("%d-%m-%Y")
    jadwal = hitung_jadwal_pemupukan(tanaman, tanggal_tanam)

    for item in jadwal:
        if item["tanggal"] == hari_ini:
            pupuk_list = ', '.join(item["pupuk"])
            catatan = item["catatan"]

            notification.notify(
                            title=f"Pemupukan Hari Ini untuk {tanaman.title()}!",
                            message=f"Waktunya pupuk: {pupuk_list}\nCatatan: {catatan}",
                            timeout=10
                            )
            print(f"🔔 Hari ini jadwal pemupukan untuk {tanaman}!")
            print(f"  Pupuk: {pupuk_list}")
            print(f"  Catatan: {catatan}")
            break
    else:
        print("Hari ini tidak ada jadwal pemupukan.")    
    
def input_pengguna():
    data_jadwal = load_jadwal()
    
    while True:
        print("Tanaman tersedia:", ", ".join(data_jadwal.keys()))
        tanaman = input("Masukkan jenis nama tanaman (atau ketik 'keluar' untuk selesai): ").strip().lower()
        if tanaman == "keluar":
            break

        if tanaman not in data_jadwal:
            print(f"❌ Tanaman '{tanaman}' tidak ditemukan.\n")
            continue

        tanam = input("Masukkan tanggal tanam (format: DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(tanam, "%d-%m-%Y") 
        except ValueError:
            print("❌ Format tanggal tidak valid.\n")  
            continue

        hasil = hitung_jadwal_pemupukan(tanaman, tanam)
        print(f"\n📅 Jadwal pemupukan untuk '{tanaman}' (tanam: {tanam}):\n")
        for i, fase in enumerate(hasil, 1):
            print(f"Pemupukan {i}: {fase['tanggal']}")
            print(f"  Pupuk: {', '.join(fase['pupuk'])}")
            print(f"  Catatan: {fase['catatan']}")
            print()

# uji
if __name__ == "__main__":
    input_pengguna()
 
