import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set camera resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Check if the webcam opened correctly
if not cap.isOpened():
    print("Could not open the webcam.")
    exit()

print("Camera started. Press 'q' to quit.")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Display the video feed
    cv2.imshow("Webcam View", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Closing camera...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
