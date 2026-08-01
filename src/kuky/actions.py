import time
import shutil
import random
import subprocess
import tomllib
from pathlib import Path

from kuky.exceptions import (
    CommandsFailedError,
    CreateKukyConfigDirError,
    RestartWindowManagerError,
)
from kuky.logs import Log

class Actions:
    def __init__(self):
        self.config_dir = Path.home() / ".config"
        self.kuky_dir = self.config_dir / "kuky"

        Log("Verifying ~/.config/kuky/ existence...", tabs=1).info()
        if not self.kuky_dir.exists():
            Log("It does not exist!", tabs=1).info()
            Log("Creating it...", tabs=1).info()
            try:
                self.kuky_dir.mkdir(parents = True)
            except OSError as e:
                raise CreateKukyConfigDirError(str(e))

        Log("Loading profiles into memory...", tabs=1).info()
        self.profiles = [profile for profile in self.kuky_dir.iterdir()]

    @staticmethod
    def print_help():
        print("USAGE: kuky [flag] [action] [argument]")

    def switch_profile(self, profile_name: str):
        Log(f"Verifying chosen profile \"{profile_name}\" existence...", new_lines=1).info()
        profile = self.kuky_dir / profile_name
        if not profile.exists():
            raise ValueError("Choosen profile does not exist!")

        Log("Saving programs from the profile into memory...", tabs=1).info()
        profile_programs = [program for program in profile.iterdir() if program.is_dir()]

        Log("Let's create those symlinks!", new_lines=1).info()
        self._create_symlinks(profile_programs)

        Log("Let's get that TOML config file!", new_lines=1).info()
        data = self._load_config(profile)

        Log("Let's execute some commands from the TOML config file!", new_lines=1).info()
        commands_failed = self._execute_config(data)
        if commands_failed is not None:
            raise CommandsFailedError(commands_failed)

        Log("Done!", new_lines=1).success()

    def switch_random_profile(self):
        Log("Verifying that the user has profiles...").info()
        if not self.profiles:
            raise IndexError("You have no profiles to choose...")

        choice = random.randint(0, len(self.profiles) - 1)
        Log(f"The randomness of life has chosen: {self.profiles[choice].name}!").info()
        self.switch_profile(self.profiles[choice].name)

    def list_profiles(self) -> list[Path]:
        return self.profiles.copy()

    def _create_symlinks(self, profile_programs: list[Path]):
        for profile_program_dir in profile_programs:
            Log(f"Creating symlink for: {profile_program_dir.name}", tabs=1).info()
            config_program_dir = self.config_dir / profile_program_dir.name

            try:
                if config_program_dir.is_dir() and not config_program_dir.is_symlink():
                    shutil.rmtree(config_program_dir)
                else:
                    config_program_dir.unlink()
            except FileNotFoundError:
                pass

            config_program_dir.symlink_to(profile_program_dir)

    def _load_config(self, profile_name: Path) -> dict:
        Log("Verifying TOML config file existence...", tabs=1).info()
        toml_path = profile_name / "config.toml"
        if not toml_path.exists():
            raise RestartWindowManagerError("TOML config file not found")

        Log("Loading TOML config file in memory...", tabs=1).info()
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)

        return data

    def _execute_config(self, data: dict) -> dict[str, str] | None:
        Log("Getting [execute] TOML field...", tabs=1).info()
        execute_field = data.get("execute")
        if not execute_field:
            raise RestartWindowManagerError("[execute] field not found in config.toml")

        Log("Getting \"reload\" and \"commands\" variables...", tabs=1).info()
        reload = execute_field.get("reload")
        commands = execute_field.get("commands")

        if reload:
            for program in reload:
                Log(f"Running \"pkill\" for: {program}...", tabs=1).info()
                subprocess.run(["pkill", program], capture_output=True, text=True, check=False)

            Log("Sleeping the program a bit to wait for pkill to finish...", tabs=1).info()
            time.sleep(0.25)

            for program in reload:
                Log(f"Let's reopen {program}!", tabs=1).info()
                subprocess.Popen(program,
                                 stdout=subprocess.DEVNULL,
                                 stdin=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 )

        Log("Running commands...", tabs=1).info()
        commands_failed = {}
        if commands:
            for command in commands:
                Log(f"Running: {command}", tabs=1).info()
                try:
                    subprocess.run(command, capture_output=True, text=True, check=False)
                except OSError as e:
                    Log("It failed! let's save it to inform the user!", tabs=1).info()
                    commands_failed[str(command)] = str(e)

        return commands_failed if commands_failed else None
