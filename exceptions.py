class RestartWindowManagerError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"You'll have to restart your window manager due to: {self.message}"

class CreateKukyConfigDirError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"I couldn't create \"$HOME/.config/kuky/\" due to: {self.message}"

class CommandsFailedError(Exception):
    def __init__(self, commands: dict):
        super().__init__(commands)
        self.commands = commands

    def __str__(self) -> str:
        errors = "\n".join(
            f"  --> {command}: {error}"
            for command, error in self.commands.items()
        )

        return f"Some commands failed to execute:\n{errors}"
