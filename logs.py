class Log:
    enabled = True

    def __init__(self, message: str = "Message left empty..."):
        self.message = message

    def error(self):
        if Log.enabled:
            print(f"[ERROR] {self.message}")

    def unknown_error(self):
        if Log.enabled:
            print(f"[UNKNOWN ERROR] {self.message}")

    def warning(self):
        if Log.enabled:
            print(f"[WARNING] {self.message}")

    def success(self):
        if Log.enabled:
            print(f"[SUCCESS] {self.message}")

    def info(self):
        if Log.enabled:
            print(f"[INFO] {self.message}")
