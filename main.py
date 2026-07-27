#!/usr/bin/env python

import sys 
from actions import Actions
from logs import Log
from exceptions import *

def main() -> int:
    args = sys.argv[1:]
    args.reverse()

    help_panel = False
    switch, profile = False, None
    list_profiles = False
    random = False
    enable_verbose = True

    if not args:
        help_panel = True

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
                    Log("Switch action requires a profile to work with!").error()
                    return 0
                break

            case "list":
                list_profiles = True
                break

            case "random":
                random = True
                break

            case "-s":
                enable_verbose = False

            case _:
                Log("Invalid action, try: \"help\" for help!").warning()
                return 0

    Log.enabled = enable_verbose
    if help_panel:
        Actions.show_help_panel()
        return 0

    elif switch and profile:
        error_ocurred = False

        Log("Verifying program health...").info()
        try:
            action = Actions()
            action.switch_chosen_profile(profile)
        except CreateKukyConfigDirError as e:
            Log(str(e), force=True).error()
            error_ocurred = True

        except ValueError as e:
            Log(str(e), force=True).error()
            error_ocurred = True
            
        except RestartWindowManagerError as e:
            Log(str(e), force=True).warning()
            error_ocurred = True

        except CommandsFailedError as e:
            Log(str(e), force=True).error()
            error_ocurred = True
            
        if error_ocurred:
            return 1

    elif random:
        error_ocurred = False
        try:
            action = Actions()
            action.switch_random_profile()
        except CreateKukyConfigDirError as e:
            Log(str(e), force=True).error()
            error_ocurred = True

        except IndexError as e:
            Log(str(e), force=True).error()
            error_ocurred = True

        except ValueError as e:
            Log(str(e), force=True).error()
            error_ocurred = True

        except RestartWindowManagerError as e:
            Log(str(e), force=True).warning()
            error_ocurred = True

        except CommandsFailedError as e:
            Log(str(e), force=True).error()
            error_ocurred = True

        if error_ocurred:
            return 1

    elif list_profiles:
        error_ocurred = False
        try:
            action = Actions()
            profiles = action.get_profiles_list()
        except CreateKukyConfigDirError as e:
            Log(str(e), force=True).error()
            error_ocurred = True
            
        if error_ocurred:
            return 1

        if not profiles:
            Log("No profiles to show, create yourself one bro", force=True).warning()
        else:
            for profile in profiles:
                print(f"[+] {profile.name}")

    return 0

if __name__ == "__main__":
    status_code = main()
    sys.exit(status_code)
