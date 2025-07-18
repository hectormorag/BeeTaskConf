import cv2

# Input and output paths
video_path = r"C:\Users\ZOHMORAL\Downloads\beedio.mp4"
output_image_path = r"C:\Users\ZOHMORAL\Downloads\first_frame.jpg"

# Open the video
cap = cv2.VideoCapture(video_path)

# Check if the video is opened
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    # Read the first frame
    ret, frame = cap.read()
    if ret:
        # Save frame exactly as is (no resizing)
        cv2.imwrite(output_image_path, frame)
        print(f"First frame saved to: {output_image_path}")
    else:
        print("Error: Could not read the first frame.")

# Release resources
cap.release()
