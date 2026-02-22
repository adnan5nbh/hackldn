from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import csv
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

# --- CONFIGURATION ---
EXCEL_FILE = 'campus_data_log.xlsx'
CSV_FILE = 'campus_data_log.csv'

room_data = {
    "temperature": "--",
    "humidity": "--",
    "light": "--",
    "occupancy": 0,
    "status_text": "Scanning...",
    "status_color": "#38bdf8"
}

def excel_logger():
    """Background task to write to BOTH CSV and Excel every 10 seconds"""
    print("🚀 Double Logging Started (CSV + Excel)...")
    while True:
        time.sleep(10) 
        
        if room_data["temperature"] != "--":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. HANDLE CSV (The 'Real-Time' Viewable File)
            try:
                file_exists = os.path.isfile(CSV_FILE)
                with open(CSV_FILE, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Timestamp", "Temp", "Humidity", "Light", "Fullness", "Status"])
                    writer.writerow([
                        timestamp, 
                        room_data["temperature"], 
                        room_data["humidity"], 
                        room_data["light"], 
                        f"{room_data['occupancy']}%", 
                        room_data["status_text"]
                    ])
                print(f"📄 CSV Logged: {timestamp}")
            except Exception as e:
                print(f"❌ CSV Error: {e}")

            # 2. HANDLE EXCEL (The 'Presentation' File)
            new_entry = {
                "Timestamp": [timestamp],
                "Temp (°C)": [room_data["temperature"]],
                "Humidity (%)": [room_data["humidity"]],
                "Light (Lux)": [room_data["light"]],
                "Fullness (%)": [f"{room_data['occupancy']}%"],
                "Status Class": [room_data["status_text"]]
            }
            df_new = pd.DataFrame(new_entry)

            try:
                if not os.path.isfile(EXCEL_FILE):
                    df_new.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
                else:
                    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                        try:
                            start_row = writer.book['Sheet1'].max_row
                        except:
                            start_row = 0
                        df_new.to_excel(writer, index=False, header=False, startrow=start_row, sheet_name='Sheet1')
                print(f"✅ Excel Updated: {timestamp}")
            except PermissionError:
                print("⚠️ EXCEL LOCKED: Close the .xlsx file to save new rows!")
            except Exception as e:
                print(f"❌ Excel Error: {e}")

threading.Thread(target=excel_logger, daemon=True).start()

# --- WEB UI (Same High-End Dark Mode) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Uni-Sense Hub</title>
    <meta http-equiv="refresh" content="1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .header { margin-bottom: 30px; text-align: center; }
        .header h1 { font-size: 2.5rem; margin-bottom: 5px; color: #38bdf8; }
        .grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; max-width: 900px; width: 100%; }
        .card { background: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #334155; min-width: 200px; }
        .label { font-size: 0.8rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.1em; margin-bottom: 10px; }
        .value { font-size: 2.5rem; font-weight: 700; }
        .occupancy-card { width: 100%; max-width: 460px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); text-align: center;}
        .status-display { font-size: 4rem; font-weight: 900; margin: 10px 0; }
        .bar-bg { background: #334155; height: 12px; width: 100%; border-radius: 10px; margin-top: 15px; }
        .bar-fill { height: 100%; transition: all 0.8s ease; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Uni-Sense Hub</h1>
        <p style="color: #94a3b8;">Dual Logging Active (CSV + XLSX)</p>
    </div>
    <div class="grid">
        <div class="card"><div class="label">Temp</div><div class="value">{{ data.temperature }}°C</div></div>
        <div class="card"><div class="label">Humidity</div><div class="value">{{ data.humidity }}%</div></div>
        <div class="card"><div class="label">Light</div><div class="value">{{ data.light }}</div></div>
        <div class="card occupancy-card">
            <div class="label">Status</div>
            <div class="status-display" style="color: {{ data.status_color }};">{{ data.status_text }}</div>
            <div class="bar-bg">
                <div class="bar-fill" style="width: {{ data.occupancy }}%; background-color: {{ data.status_color }};"></div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE, data=room_data)

@app.route('/update', methods=['POST'])
def update():
    room_data.update(request.json)
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)