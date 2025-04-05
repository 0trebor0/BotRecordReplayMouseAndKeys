import time
import json
import pyautogui
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, Listener

def replay_actions(filename="game_recording.json"):
    try:
        with open(filename, "r") as f:
            recorded_events = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'.")
        return

    mouse = MouseController()
    keyboard = KeyboardController()

    key_map = {
        'Key.alt': Key.alt, 'Key.alt_gr': Key.alt_gr, 'Key.alt_l': Key.alt_l, 'Key.alt_r': Key.alt_r,
        'Key.backspace': Key.backspace, 'Key.caps_lock': Key.caps_lock, 'Key.cmd': Key.cmd,
        'Key.cmd_l': Key.cmd_l, 'Key.cmd_r': Key.cmd_r,
        'Key.ctrl': Key.ctrl, 'Key.ctrl_l': Key.ctrl_l, 'Key.ctrl_r': Key.ctrl_r,
        'Key.delete': Key.delete, 'Key.down': Key.down, 'Key.end': Key.end, 'Key.enter': Key.enter,
        'Key.esc': Key.esc, 'Key.f1': Key.f1, 'Key.f2': Key.f2, 'Key.f3': Key.f3,
        'Key.f4': Key.f4, 'Key.f5': Key.f5, 'Key.f6': Key.f6, 'Key.f7': Key.f7,
        'Key.f8': Key.f8, 'Key.f9': Key.f9, 'Key.f10': Key.f10, 'Key.f11': Key.f11,
        'Key.f12': Key.f12, 'Key.home': Key.home, 'Key.insert': Key.insert, 'Key.left': Key.left,
        'Key.num_lock': Key.num_lock, 'Key.page_down': Key.page_down, 'Key.page_up': Key.page_up,
        'Key.pause': Key.pause, 'Key.print_screen': Key.print_screen, 'Key.right': Key.right,
        'Key.scroll_lock': Key.scroll_lock, 'Key.shift': Key.shift, 'Key.shift_l': Key.shift_l,
        'Key.shift_r': Key.shift_r, 'Key.space': Key.space, 'Key.tab': Key.tab, 'Key.up': Key.up,
        'Key.num0': '0', 'Key.num1': '1', 'Key.num2': '2', 'Key.num3': '3', 'Key.num4': '4',
        'Key.num5': '5', 'Key.num6': '6', 'Key.num7': '7', 'Key.num8': '8', 'Key.num9': '9',
        'Key.decimal': '.', 'Key.kp_divide': '/', 'Key.kp_multiply': '*',
        'Key.kp_subtract': '-', 'Key.kp_add': '+', 'Key.kp_enter': Key.enter,
        'Key.media_play': None, 'Key.media_pause': None, 'Key.media_next': None,
        'Key.media_previous': None, 'Key.media_stop': None, 'Key.media_volume_up': None,
        'Key.media_volume_down': None, 'Key.media_volume_mute': None, 'Key.f13': None,
        'Key.f14': None, 'Key.f15': None, 'Key.f16': None, 'Key.f17': None,
        'Key.f18': None, 'Key.f19': None, 'Key.f20': None, 'Key.menu': None,
        'Key.print': None, 'Key.select': None, 'Key.clear': None, 'Key.sleep': None,
        'Key.sysrq': None, 'Key.cancel': None, 'Key.prior': None, 'Key.next': None,
        'Key.separator': None, 'Key.out': None, 'Key.crsel': None, 'Key.exsel': None,
        'Key.kana': None, 'Key.junja': None, 'Key.final': None, 'Key.hanja': None,
        'Key.kanji': None, 'Key.convert': None, 'Key.nonconvert': None, 'Key.accept': None,
        'Key.modechange': None, 'Key.execute': None, 'Key.help': None,
        'Key.single_quote': "'", 'Key.double_quote': '"', 'Key.comma': ',',
        'Key.minus': '-', 'Key.period': '.', 'Key.slash': '/', 'Key.semicolon': ';',
        'Key.equal': '=', 'Key.left_bracket': '[', 'Key.backslash': '\\',
        'Key.right_bracket': ']', 'Key.grave': '`', 'Key.backtick': '`',
        'Key.mute': None, 'Key.volume_down': None, 'Key.volume_up': None, 'Key.power': None,
        'Key.kp0': '0', 'Key.kp1': '1', 'Key.kp2': '2', 'Key.kp3': '3', 'Key.kp4': '4',
        'Key.kp5': '5', 'Key.kp6': '6', 'Key.kp7': '7', 'Key.kp8': '8', 'Key.kp9': '9',
        'Key.kp_decimal': '.', 'Key.kp_enter': Key.enter, 'Key.kp_divide': '/',
        'Key.kp_multiply': '*', 'Key.kp_subtract': '-', 'Key.kp_add': '+',
        'Key.left_windows': Key.cmd_l, 'Key.right_windows': Key.cmd_r, 'Key.menu': Key.menu,
    }

    if not recorded_events:
        print("No events to replay.")
        return

    print("Waiting for F9 to start replay...")

    start_replay_flag = False

    def on_press(key):
        nonlocal start_replay_flag
        if key == Key.f9:
            start_replay_flag = True
            return False  # Stop the listener

    with Listener(on_press=on_press) as listener:
        listener.join()

    print("\n--- Game Bot Replay STARTED ---")
    time.sleep(1)  # Short delay before starting

    start_time = recorded_events[0]["timestamp"] if recorded_events else 0
    pressed_keys = set()
    mouse_path = []

    for i, event in enumerate(recorded_events):
        timestamp = event["timestamp"]
        event_type = event["type"]
        delay = timestamp - start_time
        if delay > 0:
            time.sleep(delay)
        start_time = timestamp

        try:
            if event_type == "mouse_move":
                mouse.position = event["position"]
            elif event_type == "mouse_down":
                mouse.position = event["position"] # Ensure mouse is at the correct spot
                button_str = event["button"].split('.')[-1]
                button = getattr(Button, button_str, None)
                if button:
                    mouse.press(button)
            elif event_type == "mouse_up":
                mouse.position = event["position"] # Ensure mouse is at the correct spot
                button_str = event["button"].split('.')[-1]
                button = getattr(Button, button_str, None)
                if button:
                    mouse.release(button)
            elif event_type == "key_down":
                key_str = event["key"]
                if key_str != 'Key.f11':
                    key = key_map.get(key_str, key_str)
                    if key not in pressed_keys:
                        keyboard.press(key)
                        pressed_keys.add(key)
            elif event_type == "key_up":
                key_str = event["key"]
                if key_str != 'Key.f11':
                    key = key_map.get(key_str, key_str)
                    if key in pressed_keys:
                        keyboard.release(key)
                        pressed_keys.remove(key)

        except Exception as e:
            print(f"Error replaying event {i+1}: {event}. Error: {e}")

    # Ensure all keys are released at the end
    for key in list(pressed_keys):
        try:
            keyboard.release(key)
        except Exception as e:
            print(f"Error releasing key {key} at the end: {e}")
        pressed_keys.remove(key)

    print("\n--- Game Bot Replay FINISHED ---")

if __name__ == "__main__":
    replay_actions()
