import mss
from PIL import Image

def take_screenshot(output_path="jules-scratch/verification/verification.png"):
    """Takes a screenshot of the primary monitor and saves it to the specified path."""
    with mss.mss() as sct:
        # Get information of monitor 1
        monitor_number = 1
        mon = sct.monitors[monitor_number]

        # Grab the data
        sct_img = sct.grab(mon)

        # Create an Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # Save it to the specified path
        img.save(output_path)
        print(f"Screenshot saved to {output_path}")

if __name__ == "__main__":
    take_screenshot()
