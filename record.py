import time
import pyautogui
from pynput import mouse, keyboard
import threading
from datetime import datetime
import json

# Global list to store recorded events
recorded_events = []
recording = False

def on_move(x, y):
    if recording:
        timestamp = datetime.now().timestamp()
        recorded_events.append({"timestamp": timestamp, "type": "mouse_move", "position": (x, y)})

def on_click(x, y, button, pressed):
    if recording:
        timestamp = datetime.now().timestamp()
        event_type = "mouse_down" if pressed else "mouse_up"
        recorded_events.append({"timestamp": timestamp, "type": event_type, "position": (x, y), "button": str(button)})

def on_press(key):
    global recording
    if key == keyboard.Key.f11:
        recording = not recording
        print(f"\n{'--- Recording STARTED ---' if recording else '--- Recording STOPPED ---'}")
        if not recording:
            save_recording_json()
    elif recording:
        try:
            char = key.char
            recorded_events.append({"timestamp": datetime.now().timestamp(), "type": "key_down", "key": char})
        except AttributeError:
            recorded_events.append({"timestamp": datetime.now().timestamp(), "type": "key_down", "key": str(key)})

def on_release(key):
    if recording:
        try:
            char = key.char
            recorded_events.append({"timestamp": datetime.now().timestamp(), "type": "key_up", "key": char})
        except AttributeError:
            recorded_events.append({"timestamp": datetime.now().timestamp(), "type": "key_up", "key": str(key)})
        except Exception as e:
            print(f"Error recording key release: {e}")

def save_recording_json(filename="game_recording.json"):
    if recorded_events:
        with open(filename, "w") as f:
            json.dump(recorded_events, f, indent=4)
        print(f"Recording saved to {filename} in JSON format.")
    else:
        print("No events recorded.")

def start_listeners():
    with mouse.Listener(on_move=on_move, on_click=on_click) as mouse_listener, \
            keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

if __name__ == "__main__":
    print("Press F11 to start and stop recording for the game bot.")
    print("Mouse movements, clicks, and key presses will be recorded in JSON format.")

    listener_thread = threading.Thread(target=start_listeners)
    listener_thread.daemon = True
    listener_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nRecording interrupted. Saving to JSON...")
        save_recording_json()