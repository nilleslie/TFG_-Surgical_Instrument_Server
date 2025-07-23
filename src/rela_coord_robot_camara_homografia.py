import cv2
import numpy as np

# === CONFIGURATION ===
N_POINTS = 12  

# === PART 1: Capture image clicks ===
image_points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f" Clicked point: ({x}, {y})")
        image_points.append([x, y])

# === PART 2: Image capture and point selection ===
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
print(f"🔧 Click {N_POINTS} reference points")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    for pt in image_points:
        cv2.circle(frame, tuple(pt), 5, (0, 255, 0), -1)

    cv2.imshow("Camera - Click reference points", frame)
    cv2.setMouseCallback("Camera - Click reference points", click_event)

    if len(image_points) >= N_POINTS:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
image_points = np.array(image_points, dtype=np.float32)

# === PART 3: Enter real-world coordinates in the robot's system ===
print(f"\nEnter the real-world (robot) coordinates in cm for the {N_POINTS} points:")
real_world_points = []
for i in range(N_POINTS):
    x = float(input(f"Point {i+1} - X (cm): "))
    y = float(input(f"Point {i+1} - Y (cm): "))
    real_world_points.append([x, y])
real_world_points = np.array(real_world_points, dtype=np.float32)

# === PART 4: Compute homography ===
H, status = cv2.findHomography(image_points, real_world_points)
np.save("MAT_H_LAB2.npy", H)
np.save("image_points.npy", image_points)
np.save("real_world_points.npy", real_world_points)

print("\n Homography computed and saved as 'MAT_H_LAB2.npy'")

# === PART 5: Basic visual verification ===
projected = cv2.perspectiveTransform(image_points.reshape(-1, 1, 2), H)
print("\nComparison of projected vs real points:")
for i, (proj, real) in enumerate(zip(projected.reshape(-1, 2), real_world_points)):
    print(f"Point {i+1}: Projected = ({proj[0]:.2f}, {proj[1]:.2f})  |  Real = ({real[0]:.2f}, {real[1]:.2f})")
