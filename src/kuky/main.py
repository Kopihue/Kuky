#!/usr/bin/env python

import sys
from dataclasses import dataclass

from kuky.actions import Actions
from kuky.logs import Log
from kuky.exceptions import (
    CommandsFailedError,
    CreateKukyConfigDirError,
    RestartWindowManagerError,
)

def main() -> int:
    args = parse_args()

    if args.action == "help":
        Actions.print_help()
        return 0

    Log.enabled = args.verbose
    return run(args)

@dataclass
class ParsedArgs:
    action: str | None
    profile: str | None
    verbose: bool

def parse_args() -> ParsedArgs:
    action = None
    profile = None
    verbose = True

    args = sys.argv[1:]
    if not args:
        action = "help"

    args = iter(args)
    while True:
        try:
            arg = next(args)
        except StopIteration:
            break

        match arg:
            case "-s":
                verbose = False

            case "help":
                action = "help"
                break

            case "switch":
                action = "switch"
                try:
                    profile = next(args)
                except StopIteration:
                    pass
                break

            case "list":
                action = "list"
                break

            case "random":
                action = "random"
                break

            case _:
                action = "help"
                break

    return ParsedArgs(
        action=action,
        profile=profile,
        verbose=verbose
    )

def run(args: ParsedArgs) -> int:
    try:
        Log("Verifying program health...").info()
        actions = Actions()
        match args.action:
            case "switch":
                if args.profile is not None:
                    actions.switch_profile(args.profile)
                else:
                    Log("The switch action requires an argument to work with!", force=True).error()
                    return 1

            case "random":
                actions.switch_random_profile()

            case "list":
                profiles = actions.list_profiles()
                for profile in profiles:
                    print(profile)

            case _:
                return 1

    except ValueError as e:
        Log(str(e), force=True).error()
        return 1

    except IndexError as e:
        Log(str(e), force=True).error()
        return 1

    except CreateKukyConfigDirError as e:
        Log(str(e), force=True).error()
        return 1

    except RestartWindowManagerError as e:
        Log(str(e), force=True).error()
        return 1

    except CommandsFailedError as e:
        Log(str(e), force=True).error()
        return 1

    except OSError as e:
        Log(repr(e), force=True).error()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
