from pathlib import Path
import pathlib
import time
import shutil
import random
import subprocess
import tomllib
from exceptions import *
from logs import Log

class Actions:
    def __init__(self):
        self.config_dir = pathlib.Path.home() / ".config"
        self.kuky_dir = self.config_dir / "kuky"

        Log("Verifying ~/.config/kuky/ existence...").info()
        if not self.kuky_dir.exists():
            Log("It does not exist!").info()
            Log("Creating it...").info()
            try:
                self.kuky_dir.mkdir(parents = True)
            except Exception as e:
                raise CreateKukyConfigDirError(str(e))

        Log("Loading profiles into memory...").info()
        self.profiles = [profile for profile in self.kuky_dir.iterdir()]
    
    def switch_chosen_profile(self, chosen_profile: str):
        Log(f"Verifying chosen profile \"{chosen_profile}\" existence...").info()
        profile = self.kuky_dir / chosen_profile
        if not profile.exists():
            raise ValueError("Choosen profile does not exist!")

        Log("Saving programs from the profile into memory...").info()
        profile_programs = [program for program in profile.iterdir() if program.is_dir()]

        Log("Let's create those symlinks!").info()
        self._create_symlinks(profile_programs)

        Log("Let's get that TOML config file!").info()
        data = self._get_toml_config_file_data(profile)

        Log("Let's execute some commands from the TOML config file!").info()
        commands_failed = self._reload_programs_from_toml(data)
        if commands_failed is not None:
            raise CommandsFailedError(commands_failed)

        Log("Done!").success()

    def switch_random_profile(self):
        Log("Verifying that the user has profiles...").info()
        if not self.profiles:
            raise IndexError("You have no profiles to choose...")

        choice = random.randint(0, len(self.profiles) - 1)
        Log(f"The randomness of life has chosen: {self.profiles[choice].name}!").info()
        try:
            self.switch_chosen_profile(self.profiles[choice].name)
        except Exception as e: 
            raise e

    def get_profiles_list(self) -> list[Path]:
        return self.profiles.copy()

    # *************************************************************** #

    def _create_symlinks(self, profile_programs: list[Path]):
        for profile_program_dir in profile_programs:
            Log(f"Creating symlink for: {profile_program_dir.name}").info()
            config_program_dir = self.config_dir / profile_program_dir.name

            try:
                if config_program_dir.is_dir() and not config_program_dir.is_symlink():
                    shutil.rmtree(config_program_dir)
                else:
                    config_program_dir.unlink()
            except FileNotFoundError:
                pass
            except OSError as e:
                raise e

            config_program_dir.symlink_to(profile_program_dir)


    def _get_toml_config_file_data(self, chosen_profile: Path) -> dict:
        Log("Verifying TOML config file existence...").info()
        toml_path = chosen_profile / "config.toml"
        if not toml_path.exists():
            raise RestartWindowManagerError("TOML config file not found")

        Log("Loading TOML config file in memory...").info()
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)

        return data

    def _reload_programs_from_toml(self, data: dict) -> dict[str, str] | None:
        Log("Getting [execute] TOML field...").info()
        execute_field = data.get("execute")
        if not execute_field:
            raise RestartWindowManagerError("[execute] field not found in config.toml")

        Log("Getting \"reload\" and \"commands\" variables...").info()
        reload = execute_field.get("reload")
        commands = execute_field.get("commands")

        if reload:
            for program in reload:
                Log(f"Running \"pkill\" for: {program}...").info()
                subprocess.run(["pkill", program], capture_output = True, text = True)

            Log("Sleeping the program a bit to wait for pkill to finish...").info()
            time.sleep(0.25)

            for program in reload:
                Log(f"Let's reopen {program}!").info()
                subprocess.Popen(program,
                                 stdout=subprocess.DEVNULL,
                                 stdin=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 )

        Log("Running commands...").info()
        commands_failed = {}
        if commands:
            for command in commands:
                Log(f"Running: {command}").info()
                try:
                    subprocess.run(command, capture_output = True, text = True)
                except OSError as e:
                    Log("It failed! let's save it to inform the user!").info()
                    commands_failed[str(command)] = str(e)

        return commands_failed if commands_failed else None
