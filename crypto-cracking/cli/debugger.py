from curses import COLOR_CYAN


class Color:
    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    PURPLE  = "\033[95m"
    END     = "\033[0m"

class Debugger:
    _debug: bool
    def __init__(self, set_active: bool, name: str="") -> None:
        """Constructor

        Parameters
        ----------
        set_active : bool
            Whether debug statements should be printed
        """
        self._debug = set_active
        self._name = name

        if set_active:
            self.debug("DEBUGGING ENABLED")


    def _print(self, color: Color, string: str):
        print(f"{f'[{self._name}] ' if self._name else ''}{color}{string}{Color.END}", flush=True)

    def ok(self, string: str):
        self._print(Color.GREEN, string)

    def debug(self, string: str):
        if self._debug:
            self._print(Color.PURPLE, string)

    def info(self, string: str):
        self._print(Color.CYAN, string)

    def warn(self, string: str):
        self._print(Color.YELLOW, string)

    def err(self, string: str):
        self._print(Color.RED, string)

    def printf(self, string: str):
        self._print(Color.END, string)

if __name__ == "__main__":
    d = Debugger(True, "main")
    d.printf("printf")
    d.debug("debug")
    d.info("info")
    d.warn("warn")
    d.err("err")
