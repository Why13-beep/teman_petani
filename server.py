from flask import Flask, request, jsonify
from tanaman_logic import load_jadwal, hitung_jadwal_pemupukan

app = Flask(__name__)
data_jadwal = load_jadwal()

@app.route("/")
def index():
    return "Teman Petani API is running!"

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
    
if __name__ == "__main__":
    app.run()