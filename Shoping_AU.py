import cv2
from PIL import Image
import cv2.aruco as aruco

# Define product information (replace with actual product data)
products = {
    "marker1.jpg": {"name": "T-Shirt", "price": 19.99, "image": "tshirt.png"},
    "marker2.jpg": {"name": "Sneakers", "price": 79.99, "image": "sneakers.png"},
}

# Load camera
cap = cv2.VideoCapture(0)

# Load product images
product_images = {name: cv2.imread(products[name]["image"]) for name in products}

# Define Aruco dictionary and parameters
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
aruco_params = aruco.DetectorParameters_create()

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Convert frame to grayscale for easier processing
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect AR markers
  corners, marker_ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

  if marker_ids is not None:
    for corner, marker_id in zip(corners, marker_ids):
      # Get product information based on marker ID (assuming marker image filename matches ID)
      product_info = products.get(f"marker{marker_id[0]}.jpg")

      if product_info:
        # Load product image
        product_image = product_images[f"marker{marker_id[0]}.jpg"]

        # Resize product image to fit on screen (adjust as needed)
        product_image_resized = cv2.resize(product_image, (200, 200))

        # Define overlay position (adjust as needed)
        x, y = 100, 100

        # Overlay product image on the frame
        frame[y:y+product_image_resized.shape[0], x:x+product_image_resized.shape[1]] = product_image_resized

        # Add product information text
        cv2.putText(frame, f"{product_info['name']}: ${product_info['price']}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Draw marker (optional)
        aruco.drawDetectedMarkers(frame, corners, marker_ids)

  # Display the resulting frame
  cv2.imshow('AR Shopping', frame)

  # Exit on 'q' key press
  if cv2.waitKey(1) == ord('q'):
    break

# Release capture and close all windows
cap.release()
cv2.destroyAllWindows()
