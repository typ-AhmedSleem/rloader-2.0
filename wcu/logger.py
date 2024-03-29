class TextColor:
    RED = '\033[1;31;40m'
    GREEN = '\033[1;32;40m'
    YELLOW = '\033[1;33;40m'
    BLUE = '\033[1;34;40m'
    WHITE = '\033[1;37;40m'


class BackgroundColor:
    pass


class Logger:

    def __init__(self, tag) -> None:
        self.tag = tag

    def log(self, msg, text_color=TextColor.WHITE):
        print(f"{text_color}[{self.tag}]: {msg}{TextColor.WHITE}")

    def success(self, msg):
        print(f"{TextColor.GREEN}[{self.tag}]: {msg}{TextColor.WHITE}")

    def error(self, msg):
        print(f"{TextColor.RED}[{self.tag}]: {msg}{TextColor.WHITE}")

    def info(self, msg):
        print(f"{TextColor.YELLOW}[{self.tag}]: {msg}{TextColor.WHITE}")

    def warning(self, msg):
        print(f"{TextColor.BLUE}[{self.tag}]: {msg}{TextColor.WHITE}")
