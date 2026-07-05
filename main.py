#!/usr/bin/env python

import sys
from actions import Actions

def main():
    args = sys.argv[1:]
    args.reverse()

    help_panel = False
    switch, profile = False, None
    random = False

    # switch, hola
    while args:
        arg = args.pop()

        match arg:
            case "help":
                help_panel = True
                break

            case "switch":
                switch = True
                try:
                    profile = args.pop()
                except IndexError:
                    print("Switch action requires a profile to work with!")
                    return
                break

            case "random":
                random = True
                break

            case _:
                print("Invalid action, try: \"help\" for help!")
                return

    if help_panel:
        print("Help panel deployed")

    elif switch and profile:
        action = Actions()
        try:
            action.switch_profile(profile)
        except Exception as e:
            print(e)

    elif random:
        action = Actions()

if __name__ == "__main__":
    main()
