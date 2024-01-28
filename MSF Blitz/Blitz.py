import cv2
import pyautogui
import time
from mss import mss
import numpy as np
import pygetwindow as gw


def capture_window(window_name):
    
    """
    Captures a specific window given its name.

    :param window_name: The title of the window to capture.
    :return: The captured image in OpenCV format, or None if the window is not found.
    """
    try:
        # Find the window by name
        window = gw.getWindowsWithTitle(window_name)[0]
        if not window:
            print(f"Window '{window_name}' not found.")
            return None

        # Check if the window is minimized
        if window.isMinimized:
            print(f"Window '{window_name}' is minimized.")
            return None

        # Define the region to capture
        window_region = {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height
        }

        # Capture the specified region
        with mss() as sct:
            sct_img = sct.grab(window_region)

        # Convert to OpenCV format
        return cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR), (window.left, window.top)

    except IndexError:
        print(f"Window '{window_name}' not found.")
        return None
    

def focus_on_window(title):
    title = "BlueStacks App Player"
    try:
        window = gw.getWindowsWithTitle(title)[0]
        if window is not None:
            window.activate()
            return True
    except Exception as e:
        print(f"Error focusing on window: {e}")
    return False


def detect_button(screen, template_path):
    # Read the template image
    template = cv2.imread(template_path, 0)
    h, w = template.shape[:2]  # height and width of the template

    # Convert screen to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

    # Set a threshold for detection
    threshold = 0.9
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Loop through detected points
        # Calculate center of the button
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        return (center_x, center_y)  # Return the center point

    return None

def click_button(x, y):
    print(f"Moving to ({x}, {y}) and clicking.")  # Debug print
    pyautogui.moveTo(x, y, duration=0.25)  # Slower movement to the target
    time.sleep(0.5)  # Wait for the mouse to move
    pyautogui.click(button='left')  # Explicitly specify the mouse button

def main():
    window_title = "BlueStacks App Player"
    operations = [
        {"template": "Find Opponent.JPG", "delay": 0.25},
        {"template": "Blitz Battle.JPG", "delay": 0.5, "check_continue": True},
        {"template": "Blitz Next Team.JPG", "delay": 0.25},
    
    ]

    popup_template = "Continue.JPG"
    popup_delay = 9  # Delay in seconds before checking for the popup

    max_cycles = 100  # Number of cycles before pausing
    cycle_count = 0  # Counter for cycles

    try:
        while True:
            if cycle_count >= max_cycles:
                print("Completed 49 cycles. Pausing for an hour.")
                time.sleep(3600)  # Pause for an hour
                cycle_count = 0  # Reset the cycle count after the pause

            if not focus_on_window(window_title):
                print(f"Could not focus on '{window_title}'. Retrying in 10 seconds...")
                time.sleep(10)
                continue

            screen, window_pos = capture_window(window_title)
            if screen is not None:
                for operation in operations:
                    button_position = detect_button(screen, operation['template'])
                    if button_position:
                        adjusted_position = (button_position[0] + window_pos[0], 
                                             button_position[1] + window_pos[1])
                        click_button(*adjusted_position)
                        print(f"Clicked at: {adjusted_position}")
                        time.sleep(operation['delay'])

                        if operation.get("check_continue"):
                            time.sleep(popup_delay)
                            screen, _ = capture_window(window_title)
                            continue_position = detect_button(screen, popup_template)
                            if continue_position:
                                continue_adjusted = (continue_position[0] + window_pos[0], 
                                                     continue_position[1] + window_pos[1])
                                click_button(*continue_adjusted)
                                print(f"Clicked 'Continue' at: {continue_adjusted}")
                                time.sleep(2)  # Adjust delay as needed

            cycle_count += 1  # Increment the cycle count after each cycle

    except KeyboardInterrupt:
        print("Script stopped by user.")

if __name__ == "__main__":
    main()