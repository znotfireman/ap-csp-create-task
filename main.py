from typing import TypedDict, Optional
from tkinter import *
import tkinter.font as tkFont
import time
import math

class Key(TypedDict):
    label: str
    # Refer to Tkinter keycodes:
    # https://stackoverflow.com/a/32289245
    codes: list[str]
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
    },
    {
        "label": "Jump",
        "codes": [" "],
        "x": 0,
        "y": 2,
        "width": 3,
        "height": 0.5
    },
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
        time_label = f"\n{time_pressed:.1f}s"
        
        canvas.create_text(
            x0 + real_width / 2,
            y0 + real_height / 2,
            text=time_label,
            fill=fg_fill,
            justify="center",
            anchor="n",
            font=time_font
        )
    
keys_held_at: dict[str, float] = {}

def on_pressed(event: Event):
    if event.char not in keys_held_at:
        keys_held_at[event.char] = time.time()

def on_released(event: Event):
    if event.char in keys_held_at:
        keys_held_at.pop(event.char)

root.bind("<Key>", on_pressed)
root.bind("<KeyRelease>", on_released)

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
            
    # ~60fps
    root.after(16, key_loop)
    
key_loop()
root.mainloop()
