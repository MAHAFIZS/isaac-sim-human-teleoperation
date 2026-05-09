import cv2
import mediapipe as mp
import numpy as np
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5055
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Webcam not found.")
    exit()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

print("Sending shoulder + elbow data to Isaac Sim...")
print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        shoulder = [
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        ]

        elbow = [
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
        ]

        wrist = [
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        ]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        shoulder_x = elbow[0] - shoulder[0]
        shoulder_lift = shoulder[1] - elbow[1]

        message = f"{shoulder_x:.4f},{shoulder_lift:.4f},{elbow_angle:.2f}"
        sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))

        cv2.putText(frame, f"Shoulder X: {shoulder_x:.2f}", (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Shoulder Lift: {shoulder_lift:.2f}", (40, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Elbow: {int(elbow_angle)}", (40, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        print(message)

    cv2.imshow("Webcam Multi-Joint Pose Sender", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
sock.close()
cv2.destroyAllWindows()