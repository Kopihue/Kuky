class Log:
    enabled = True

    def __init__(self, message: str = "Message left empty..."):
        self.message = message

    def error(self, force: bool = False):
        if Log.enabled or force:
            print(f"[ERROR] {self.message}")

    def unknown_error(self, force: bool = False):
        if Log.enabled or force:
            print(f"[UNKNOWN ERROR] {self.message}")

    def warning(self, force: bool = False):
        if Log.enabled or force:
            print(f"[WARNING] {self.message}")

    def success(self, force: bool = False):
        if Log.enabled or force:
            print(f"[SUCCESS] {self.message}")

    def info(self, force: bool = False):
        if Log.enabled or force:
            print(f"[INFO] {self.message}")
