import pathlib
import sys
import shutil

class Actions:
    def __init__(self):
        home_dir = pathlib.Path.home()
        kuky_dir = home_dir / ".config" / "kuky"

        if not kuky_dir.exists():
            try:
                kuky_dir.mkdir(parents = True)
            except Exception as e:
                print("There was an exception creating the \"kuky\" config dir under \".config\"")
                print(e)
                sys.exit(1)

        self.profiles = [profile for profile in kuky_dir.iterdir() if profile.is_dir()]
        self.home_config_dir = home_dir / ".config"

    def switch_profile(self, profile: str):
        found_profile = None
        for option in self.profiles:
            if profile == option.name:
                found_profile = option

        if not found_profile:
            raise ValueError("Profile not found...")

        profile_configs = [config for config in found_profile.iterdir() if config.is_dir()]
        for config in profile_configs:
            config_dir = self.home_config_dir / config.name
            if not config_dir.exists():
                pass
            elif config_dir.is_symlink():
                config_dir.unlink()
            else:
                shutil.rmtree(config_dir) if config_dir.is_dir() else config_dir.unlink()
            config_dir.symlink_to(config)
