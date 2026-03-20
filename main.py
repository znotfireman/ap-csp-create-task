from typing import TypedDict, Optional, Union
from tkinter import *
import tkinter.font as tkFont
import time
import math
from pynput import keyboard
from colorama import Style, Fore

class Key(TypedDict):
    label: str
    codes: list[Union[str, keyboard.Key]]
    x: int
    y: int
    width: Optional[int]
    height: Optional[int]

KEYS: list[Key] = [
    {
        "label": "W",
        "codes": ["W", "w"],
        "x": 1,
        "y": 0,
        "width": None,
        "height": None
    },
    {
        "label": "A",
        "codes": ["A", "a"],
        "x": 0,
        "y": 1,
        "width": None,
        "height": None
    },
    {
        "label": "S",
        "codes": ["S", "s"],
        "x": 1,
        "y": 1,
        "width": None,
        "height": None
    },
    {
        "label": "D",
        "codes": ["D", "d"],
        "x": 2,
        "y": 1,
        "width": None,
        "height": None
    }
]

KEY_WIDTH = 64
KEY_HEIGHT = 64
KEY_TEXT_SIZE = 24
KEY_TIME_TEXT_SIZE = 12
KEY_MARGIN = 2

root = Tk(screenName="AP CSP", baseName="AP CSP", className='Tk', useTk=1)
canvas = Canvas(root, background='black')
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

font = tkFont.Font(family="Arial", size=KEY_TEXT_SIZE)
time_font = tkFont.Font(family="Arial", size=KEY_TIME_TEXT_SIZE)

keys_held_at: dict[str, float] = {}

def render_key(key: Key, bg_fill, fg_fill, held_at=None):
    label = key.get("label")
    
    x0 = key.get("x") * KEY_WIDTH + KEY_MARGIN
    y0 = key.get("y") * KEY_HEIGHT + KEY_MARGIN
    
    width = key.get("width") or 1
    height = key.get("height") or 1
    
    real_width = width * KEY_WIDTH
    real_height = height * KEY_HEIGHT
    
    x1 = x0 + real_width - KEY_MARGIN
    y1 = y0 + real_height - KEY_MARGIN
    
    canvas.create_rectangle(
        x0,
        y0,
        x1,
        y1,
        fill=bg_fill
    )
    
    canvas.create_text(
        x0 + real_width / 2,
        y0 + real_height / 2,
        text=label,
        fill=fg_fill,
        justify="center",
        font=font
    )
    
    if held_at:
        time_pressed = time.time() - held_at

        # HACK: using a newline as to not deal with layouting
        time_label = f"\n{time_pressed:.2f}s"
        
        canvas.create_text(
            x0 + real_width / 2,
            y0 + real_height / 2,
            text=time_label,
            fill=fg_fill,
            justify="center",
            anchor="n",
            font=time_font
        )
    
def on_press(key: Union[keyboard.Key, Event]):
    try:
        if key.char not in keys_held_at:
            keys_held_at[key.char] = time.time()
    except AttributeError:
        # special keys don't have a char field
        if key not in keys_held_at:
            keys_held_at[key] = time.time()


def on_release(key: Union[keyboard.Key, Event]):
    try:
        if key.char in keys_held_at:
            keys_held_at.pop(key.char)
    except AttributeError:
        # special keys don't have a char field
        if key in keys_held_at:
            keys_held_at.pop(key)

def key_loop():
    for key in KEYS:
        is_key_pressed = False
        held_at = math.inf
        
        for code in key.get("codes"):
            if code in keys_held_at:
                is_key_pressed = True
                key_held_at = keys_held_at[code]
                
                if key_held_at < held_at:
                    held_at = key_held_at

        if is_key_pressed:
            render_key(key, "yellow", "black", held_at)
        else:
            render_key(key, "gray", "white")
    
    # ~30fps
    root.after(32, key_loop)
    
def create_formatter(style, reset):
    def style(str, style=style, reset=reset):
        return style + str + reset
    
    return style
    
style_dim = create_formatter(Style.DIM, Style.RESET_ALL)
style_bright = create_formatter(Style.BRIGHT, Style.RESET_ALL)

def quote(str):
    return style_dim("'") + str + style_dim("'")

# Clears the terminal by printing an abitrary amount of empty lines
def clear_terminal():
    print("\n" * 80)

clear_terminal()
print(style_dim("Welcome to ") + style_bright("Keybound") + style_dim(", the keyboard HUD for gameplay recordings."))
print("Two keyboard implementations are available:")
print()
print(style_bright("pynput"))
print(style_dim("*"), "Will respond to inputs while the program is unfocused")
print(style_dim("*"), "Requires adding Python to accessibility permissions on MacOS")
print()
print(style_bright("tkinter"))
print(style_dim("*"), "Will NOT respond to inputs while the program is unfocused")
print(style_dim("*"), "Requires no setup")
print()

while True:
    keyboard_implementation = input(f"Which keyboard implementation should be used? ({quote("pynput")} or {quote("tkinter")}): ")

    if keyboard_implementation == "pynput":
        print(style_dim("Using pynput..."))
        keyboard.Listener(on_press=on_press, on_release=on_release).start()
        break
    elif keyboard_implementation == "tkinter":
        print(style_dim("Using tkinter..."))
        root.bind("<Key>", on_press)
        root.bind("<KeyRelease>", on_release)
        break
    else:
        clear_terminal()
        print(Fore.RED + style_bright(f"Unknown keyboard implementation named '{keyboard_implementation}'") + Fore.RESET)
    
key_loop()

def on_main_loop():
    clear_terminal()
    print(Fore.GREEN + style_bright("Started!") + Fore.RESET)
    print(style_dim("Check the Dock for a Python window."))
    print()
    
root.after(10, on_main_loop)
root.mainloop()
