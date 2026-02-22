import cv2
from ultralytics import YOLO
import requests

# 1. Load the model
model = YOLO('yolov8n.pt') 

# 2. Use '0' for the built-in laptop webcam
cap = cv2.VideoCapture(0)

# Speed optimization
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

TOTAL_SEATS = 30 

print("AI Node Online using Laptop Webcam. Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Run AI on the frame
    results = model(frame, classes=[0], conf=0.4, verbose=False)
    count = len(results[0].boxes)
    pct = round((count / TOTAL_SEATS) * 100, 1)

    # Send data to dashboard
    try:
        requests.post("http://127.0.0.1:5000/update", json={"occupancy": pct})
    except:
        pass

    # Show the preview window so you can see the boxes for your demo
    cv2.imshow("Campus AI Monitor", results[0].plot())
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()