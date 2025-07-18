import cv2
import numpy as np

# Global list to store points
points = []

# Mouse callback function to collect 3 points
def click_event(event, x, y, flags, param):
    global points, img_copy

    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 3:
        points.append((x, y))
        cv2.circle(img_copy, (x, y), 4, (0, 0, 255), -1)  # Red point
        cv2.imshow("Image", img_copy)

        if len(points) == 3:
            # Fit a circle
            circle = cv2.minEnclosingCircle(np.array(points))
            center, radius = circle
            center_int = tuple(map(int, center))
            radius_int = int(radius)

            # Draw circle and center
            cv2.circle(img_copy, center_int, radius_int, (0, 255, 0), 2)  # Green circle
            cv2.circle(img_copy, center_int, 5, (255, 0, 0), -1)  # Blue center
            cv2.imshow("Image", img_copy)

            # Save a 200x200 px crop around the circle center
            crop_size = 200
            x_start = max(center_int[0] - crop_size // 2, 0)
            y_start = max(center_int[1] - crop_size // 2, 0)
            x_end = x_start + crop_size
            y_end = y_start + crop_size

            # Create annotated version for saving
            annotated_img = img.copy()
            for p in points:
                cv2.circle(annotated_img, p, 4, (0, 0, 255), -1)
            cv2.circle(annotated_img, center_int, radius_int, (0, 255, 0), 2)
            cv2.circle(annotated_img, center_int, 5, (255, 0, 0), -1)

            # Handle crop that might go outside image bounds
            annotated_crop = annotated_img[y_start:y_end, x_start:x_end]
            h, w = annotated_crop.shape[:2]

            # Pad if crop is smaller than 200x200
            if h < crop_size or w < crop_size:
                padded = np.zeros((crop_size, crop_size, 3), dtype=np.uint8)
                padded[:h, :w] = annotated_crop
                annotated_crop = padded

            # Save
            save_path = r"C:\Users\ZOHMORAL\Downloads\circle_crop.jpg"
            cv2.imwrite(save_path, annotated_crop)
            print(f"Cropped image saved at {save_path}")

# Load image
img_path = r"C:\Users\ZOHMORAL\Downloads\first_frame.jpg"
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Image not found at {img_path}")

img_copy = img.copy()

# Create window and set callback
cv2.imshow("Image", img_copy)
cv2.setMouseCallback("Image", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
