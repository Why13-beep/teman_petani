from flask import Flask, request, jsonify
from tanaman_logic import load_jadwal, hitung_jadwal_pemupukan
from statistik import get_statistik_mingguan

app = Flask(__name__)

@app.route("/")
def index():
    return "Teman Petani API is running!"

data_jadwal = load_jadwal()
@app.route("/jadwal", methods= ["POST"])
def get_jadwal():
    data = request.json
    tanaman = data.get("tanaman")
    tanggal = data.get("tanggal_tanam")

    try:
        hasil = hitung_jadwal_pemupukan(tanaman, tanggal, data_jadwal)
        return jsonify({"jadwal": hasil})
    except Exception as e:
        return jsonify({"error": str(e)}),400
        
#get statistics
@app.route("/statistik", methods=["GET"])
def get_statistik():
    try:
        statistik = get_statistik_mingguan()
        return jsonify({"statistik": statistik})

    except:
        return jsonify({"error": "Gagal mengambil statistik"}), 400
    
app.run(host="0.0.0.0", port=81)
