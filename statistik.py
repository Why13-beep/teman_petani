import mysql.connector
from datetime import datetime, timedelta
from db_config import get_db_connection

def get_statistik_mingguan():
    conn = get_db_connection
    cursor = conn.cursor()

    hari_ini = datetime.today()
    seminggu_lalu = hari_ini - timedelta(days=7)

    awal = seminggu_lalu.strftime("%Y-%m-%d")
    akhir = hari_ini.strftime("%Y-%m-%d")

    query = """
                   SELECT tanggal, nama_tanaman, aktivitas, detail
                   FROM aktivitas
                   WHERE tanggal BETWEEN ? AND ?
                   ORDER BY tanggal ASC"""

    cursor.execute(query, (awal, akhir))
    data = cursor.fetchall()
    conn.close()

    if not data:
        return "Tidak ada aktivitas dalam seminggu terakhir"

    #Hitung jumlah aktivitas per jenis
    statistik = {}
    for tgl, tanaman, akt, det in data:
        statistik[akt] = statistik.get(akt, 0) + 1

    ringkasan = "[STATISTIK MINGGUAN]\n"
    ringkasan += f"Periode: {seminggu_lalu.date()} s.d. {hari_ini.date()}\n\n"
    for jenis, jumlah in statistik.items():
        ringkasan += f"- {jenis.capitalize()}: {jumlah} kali \n"

    ringkasan += "\nDetail aktivitas: \n"
    for tgl, tanaman, akt, det in data:
        ringkasan += f"{tgl} | {tanaman} | {akt} -> {det}\n"

    return ringkasan
