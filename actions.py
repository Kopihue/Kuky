from pathlib import Path
import pathlib
import time
import shutil
import random
import subprocess
import tomllib
from exceptions import *

class Actions:
    def __init__(self):
        self.config_dir = pathlib.Path.home() / ".config"
        self.kuky_dir = self.config_dir / "kuky"

        if not self.kuky_dir.exists():
            try:
                self.kuky_dir.mkdir(parents = True)
            except Exception as e:
                raise CreateKukyConfigDirError(str(e))

        self.profiles = [profile for profile in self.kuky_dir.iterdir()]
    
    def switch_chosen_profile(self, chosen_profile: str):
        profile = self.kuky_dir / chosen_profile
        if not profile.exists():
            raise ValueError("Choosen profile does not exist!")

        profile_programs = [program for program in profile.iterdir() if program.is_dir()]

        self._create_symlinks(profile_programs)
        data = self._get_toml_config_file_data(profile)

        commands_failed = self._reload_programs_from_toml(data)
        if commands_failed is not None:
            raise CommandsFailedError(commands_failed)

    def switch_random_profile(self):
        if not self.profiles:
            raise IndexError("You have no profiles to choose...")

        choice = random.randint(0, len(self.profiles) - 1)
        try:
            self.switch_chosen_profile(self.profiles[choice].name)
        except Exception as e: 
            raise e

    def get_profiles_list(self) -> list[Path]:
        return self.profiles.copy()

    # *************************************************************** #

    def _create_symlinks(self, profile_programs: list[Path]):
        for profile_program_dir in profile_programs:
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
        toml_path = chosen_profile / "config.toml"
        if not toml_path.exists():
            raise RestartWindowManagerError("TOML config file not found")

        with open(toml_path, "rb") as f:
            data = tomllib.load(f)

        return data

    def _reload_programs_from_toml(self, data: dict) -> dict[str, str] | None:
        execute_field = data.get("execute")
        if not execute_field:
            raise RestartWindowManagerError("[execute] field not found in config.toml")

        reload = execute_field.get("reload")
        commands = execute_field.get("commands")

        if reload:
            for program in reload:
                subprocess.run(["pkill", program], capture_output = True, text = True)

            time.sleep(0.25)

            for program in reload:
                subprocess.Popen(program,
                                 stdout=subprocess.DEVNULL,
                                 stdin=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 )

        commands_failed = {}
        if commands:
            for command in commands:
                try:
                    subprocess.run(command, capture_output = True, text = True)
                except OSError as e:
                    commands_failed[str(command)] = str(e)

        return commands_failed if commands_failed else None
