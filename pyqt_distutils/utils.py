try:
    import colorama
except ImportError:
    has_colorama = False
else:
    has_colorama = True


def write_message(text, color=None):
    if has_colorama:
        colors = {
            'red': colorama.Fore.RED,
            'green': colorama.Fore.GREEN,
            'yellow': colorama.Fore.YELLOW,
            'blue': colorama.Fore.BLUE
        }
        try:
            print(colors[color] + text + colorama.Fore.RESET)
        except KeyError:
            print(text)
    else:
        print(text)
