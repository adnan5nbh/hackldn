from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Data storage - these will be updated by your AI and Arduino scripts
room_data = {
    "temperature": "--",
    "humidity": "--",
    "light": "--",
    "occupancy": 0
}

# The High-Tech UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Uni-Sense | Smart Campus</title>
    <meta http-equiv="refresh" content="1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .header { margin-bottom: 40px; text-align: center; }
        .header h1 { font-size: 2.5rem; margin-bottom: 5px; color: #38bdf8; }
        .header p { color: #94a3b8; font-size: 1.1rem; }
        .status-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 10px #22c55e; }
        
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 800px; width: 100%; }
        .card { background: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #334155; position: relative; }
        .card::after { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #38bdf8; border-radius: 16px 16px 0 0; }
        .label { font-size: 0.9rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; margin-bottom: 10px; }
        .value { font-size: 3rem; font-weight: 700; }
        .unit { font-size: 1.2rem; color: #64748b; margin-left: 5px; }
        
        .occupancy-card { grid-column: span 2; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); }
        .occupancy-bar-bg { background: #334155; height: 12px; width: 100%; border-radius: 6px; margin-top: 15px; }
        .occupancy-bar-fill { background: #38bdf8; height: 100%; border-radius: 6px; transition: width 0.5s ease-in-out; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Uni-Sense Hub</h1>
        <p><span class="status-dot"></span> Live Monitoring: Classroom 101</p>
    </div>

    <div class="grid">
        <div class="card">
            <div class="label">Temperature</div>
            <div class="value">{{ data.temperature }}<span class="unit">°C</span></div>
        </div>
        <div class="card">
            <div class="label">Humidity</div>
            <div class="value">{{ data.humidity }}<span class="unit">%</span></div>
        </div>
        <div class="card">
            <div class="label">Ambient Light</div>
            <div class="value">{{ data.light }}<span class="unit">Lux</span></div>
        </div>
        <div class="card occupancy-card">
            <div class="label">Real-time Occupancy</div>
            <div class="value">{{ data.occupancy }}<span class="unit">% Full</span></div>
            <div class="occupancy-bar-bg">
                <div class="occupancy-bar-fill" style="width: {{ data.occupancy }}%;"></div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, data=room_data)

@app.route('/update', methods=['POST'])
def update():
    global room_data
    room_data.update(request.json)
    return jsonify(status="success")

if __name__ == '__main__':
    print("Dashboard Server Starting on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)