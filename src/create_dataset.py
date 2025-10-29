import cv2
import os

# Create the main data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Create subdirectories for each sign
signs = ['hello', 'thanks', 'iloveyou']
for sign in signs:
    if not os.path.exists(os.path.join('data', sign)):
        os.makedirs(os.path.join('data', sign))

# Start the camera
cap = cv2.VideoCapture(0)

# Set the current sign and image count
current_sign = 'hello'
count = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, quit
    if key == ord('q'):
        break

    # If the 'c' key is pressed, capture and save the image
    elif key == ord('c'):
        # Save the image to the appropriate directory
        cv2.imwrite(os.path.join('data', current_sign, f'{current_sign}_{count}.jpg'), frame)
        print(f'Saved image {count} for sign {current_sign}')
        count += 1

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
