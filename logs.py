class Log:
    enabled = True

    def __init__(
            self,
            message: str = "Message left empty...",
            force: bool = False,
            tabs: int = 0,
            new_lines: int = 0,
            ):

        self.message = message
        self.force = force

        self.tabs = ""
        for tab in range(tabs):
            self.tabs += "\t"

        self.new_lines = ""
        for new in range(new_lines):
            self.new_lines += "\n"

    def error(self):
        if Log.enabled or self.force:
            print(f"{self.new_lines}{self.tabs}[ERROR] {self.message}")

    def unknown_error(self):
        if Log.enabled or self.force:
            print(f"{self.new_lines}{self.tabs}[UNKNOWN ERROR] {self.message}")

    def warning(self):
        if Log.enabled or self.force:
            print(f"{self.new_lines}{self.tabs}[WARNING] {self.message}")

    def success(self):
        if Log.enabled or self.force:
            print(f"{self.new_lines}{self.tabs}[SUCCESS] {self.message}")

    def info(self):
        if Log.enabled or self.force:
            print(f"{self.new_lines}{self.tabs}[INFO] {self.message}")
