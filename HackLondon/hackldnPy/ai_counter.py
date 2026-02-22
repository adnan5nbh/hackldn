import cv2
from ultralytics import YOLO
import requests

model = YOLO('yolov8n.pt') 
cap = cv2.VideoCapture(0) # '0' is your laptop webcam
TOTAL_SEATS = 30 

# Smoothing history to stop the percentage from jumping
history = []

print("AI Node Online. Categorizing occupancy...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame, classes=[0], conf=0.4, verbose=False)
    current_count = len(results[0].boxes)

    # Add current count to history and keep only the last 15 frames
    history.append(current_count)
    if len(history) > 15:
        history.pop(0)
    
    # Calculate smooth average
    avg_count = sum(history) / len(history)
    occupancy_pct = (avg_count / TOTAL_SEATS) * 100

    # --- CATEGORY CLASSES ---
    if occupancy_pct <= 33:
        status = "Plenty of Space"
        color_code = "#22c55e" # Green
    elif occupancy_pct <= 66:
        status = "Moderately Busy"
        color_code = "#eab308" # Yellow
    else:
        status = "Limited Spaces"
        color_code = "#ef4444" # Red

    # Send data to dashboard
    try:
        requests.post("http://127.0.0.1:5000/update", json={
            "occupancy": round(occupancy_pct, 1),
            "status_text": status,
            "status_color": color_code
        })
    except:
        pass

    # Show the preview window (press 'q' to quit)
    cv2.imshow("Campus AI Monitor", results[0].plot())
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()