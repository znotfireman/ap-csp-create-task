# You could use dictionaries here but builders have "type safety" and I'm not
# bothered to learn python typechecking :/

# Keycodes are based on Tkinter:
# https://stackoverflow.com/a/32289245

class Key:
    def __init__(self):
        self.label = "?"
        self.codes = []
        self.x = 0
        self.y = 0
        pass
    
    def set_label(self, label: str):
        self.label = label
        return self
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        return self
    
    def add_keycode(self, code: str):
        self.codes.append(code)
        return self

KEYS = [
    Key()
        .set_label("W")
        .set_position(1, 0)
        .add_keycode("W")
        .add_keycode("w"),
    
    Key()
        .set_label("A")
        .set_position(1, 0)
        .add_keycode("A")
        .add_keycode("a"),
    
    Key()
        .set_label("A")
        .set_position(0, 1)
        .add_keycode("A")
        .add_keycode("a"),
        
    Key()
        .set_label("S")
        .set_position(1, 1)
        .add_keycode("S")
        .add_keycode("s"),
        
    Key()
        .set_label("D")
        .set_position(2, 1)
        .add_keycode("D")
        .add_keycode("d"),
        
    Key()
        .set_label("Space")
        .set_position(2, 0)
        .add_keycode("<Space>")
]

# ------------------------------------------------------------------------------

from keypress import Keys, get_key
from tkinter import *
import tkinter
import tkinter.font as tkFont
import argparse
import os
import tomllib
import subprocess

homedir = os.path.expanduser('~')

KEY_WIDTH = 64
KEY_HEIGHT = 64
KEY_TEXT_SIZE = 24
KEY_TEXT_TOP_PADDING = 24

CONFIGURATION_DIR = f"{homedir}/.bikey"
CONFIGURATION_FILE_PATH = f"{CONFIGURATION_DIR}/configuration.toml"

parser = argparse.ArgumentParser(prog = 'Bikey', description = 'Bill\'s Keyboard HUD')
parser.add_argument('subcommand', default="help")
parser.add_argument('-c', '--configuration', default=CONFIGURATION_FILE_PATH)

def init(configuration_path):
    if os.path.exists(configuration_path):
        print(f"already initialized configuration file at {configuration_path}")
        exit(1)
    
    configuration = open(configuration_path, "w+")
    configuration.writelines("\n".join([
        "[[inputs]]",
        "label = 'W'",
        "codes = ['W', 'w']",
        "position = [1, 0]",
        "",
        "[[inputs]]",
        "label = 'A'",
        "codes = ['A', 'a']",
        "position = [0, 1]",
        "",
        "[[inputs]]",
        "label = 'S'",
        "codes = ['S', 's']",
        "position = [1, 1]",
        "",
        "[[inputs]]",
        "label = 'D'",
        "codes = ['D', 'd']",
        "position = [2, 1]",
    ]))
    
    configuration.close()
    print(f"wrote base configuration at {configuration_path}")

def bind_key(root: Tk, canvas: Canvas, font: tkFont.Font, key):
    key_label = key.get("label")
    key_codes = key.get("codes")
    
    position = key.get("position")
    x = position[0]
    y = position[1]
    
    position_x = x * KEY_WIDTH
    position_y = y * KEY_HEIGHT
    
    canvas.create_rectangle(position_x, position_y, position_x + KEY_WIDTH, position_y + KEY_HEIGHT, fill="white")
    
    text_size = font.measure(key_label)
    canvas.create_text(
        position_x + KEY_WIDTH / 2 - text_size / 2,
        position_y + KEY_TEXT_TOP_PADDING,
        text=key_label,
        fill="black",
        font=font
    )
    
    for keycode in key_codes:
        def on_key_press(event: Event):
            global keycode
            print("keycode pressed", keycode, event)

        root.bind(keycode, on_key_press)

def run(configuration_path):
    if os.path.exists(args.configuration) == False:
        print(f"cannot find configuration file at {args.configuration}")
        exit(1)
    
    configuration_contents = open(args.configuration, "rb")
    configuration = tomllib.load(configuration_contents)
    
    inputs = configuration.get("inputs")
    
    root = Tk(screenName="Bikey", baseName="Bikey", className='Tk', useTk=1)
    canvas = Canvas(root, background='black')
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    
    font = tkFont.Font(family="Arial", size=KEY_TEXT_SIZE)
    
    for key in inputs:
        bind_key(root, canvas, font, key)

    canvas.pack()
    root.mainloop()
        
if __name__ == "__main__":
    args = parser.parse_args()
    os.makedirs(CONFIGURATION_DIR, exist_ok=True)
 
    if args.subcommand == "help":
        parser.print_help()
    elif args.subcommand == "run":
        run(args.configuration)
    elif args.subcommand == "init":
        init(args.configuration)
    elif args.subcommand == "configure":
        if os.path.exists(CONFIGURATION_FILE_PATH):
            subprocess.run(["code", CONFIGURATION_FILE_PATH])
        else:
            print(f"no configuration file at {CONFIGURATION_FILE_PATH}")
            exit(1)
    elif args.subcommand == "deinit":
        if os.path.exists(CONFIGURATION_FILE_PATH):
            os.remove(CONFIGURATION_FILE_PATH)
            print(f"removed configuration file at {CONFIGURATION_FILE_PATH}")
        else:
            print(f"no configuration file at {CONFIGURATION_FILE_PATH}")
            exit(1)
    else:
        print(f"invalid subcommand: {args.subcommand}")
        exit(1)
    
    exit(0)
