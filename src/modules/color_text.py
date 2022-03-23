class ColorText:

    COLORS = dict(
        YELLOW="\033[93m",
        GREEN="\033[92m",
        RED="\033[91m",
    )
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def to_color(message, color):
        CT = ColorText
        _color = CT.COLORS.get(color, CT.COLORS["GREEN"])
        return _color + CT.BOLD + message + CT.RESET
