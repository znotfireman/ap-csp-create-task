from keypress import Keys, get_key
import argparse
import os
import tomllib
import subprocess

homedir = os.path.expanduser('~')

CONFIGURATION_DIR = f"{homedir}/.bikey"
CONFIGURATION_FILE_PATH = f"{CONFIGURATION_DIR}/configuration.toml"

parser = argparse.ArgumentParser(prog = 'Bikey', description = 'Bill\'s Keyboard HUD')
parser.add_argument('subcommand', default="help")
parser.add_argument('-c', '--configuration', default=CONFIGURATION_FILE_PATH)

if __name__ == "__main__":
    args = parser.parse_args()
    os.makedirs(CONFIGURATION_DIR, exist_ok=True)

    if args.subcommand == "help":
        parser.print_help()
    elif args.subcommand == "run":
        if os.path.exists(args.configuration) == False:
            print(f"cannot find configuration file at {args.configuration}")
            exit(1)
        
        configuration = open(args.configuration, "rt")
        inputs = tomllib.load(configuration)
    elif args.subcommand == "init":
        if os.path.exists(CONFIGURATION_FILE_PATH):
            print(f"already initialized configuration file at {CONFIGURATION_FILE_PATH}")
            exit(1)
        
        configuration = open(CONFIGURATION_FILE_PATH, "w+")
        configuration.writelines("\n".join([
            "[[inputs]]",
            "keycode = 'W'",
            "position = [1, 0]",
            "",
            "[[inputs]]",
            "keycode = 'A'",
            "position = [0, 1]",
            "",
            "[[inputs]]",
            "keycode = 'S'",
            "position = [1, 1]",
            "",
            "[[inputs]]",
            "keycode = 'D'",
            "position = [2, 1]",
        ]))
        
        configuration.close()
        print(f"wrote base configuration at {CONFIGURATION_FILE_PATH}")
    elif args.subcommand == "configure":
        if os.path.exists(CONFIGURATION_FILE_PATH):
            subprocess.run(["open", CONFIGURATION_FILE_PATH])
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
