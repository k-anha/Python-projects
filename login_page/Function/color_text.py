# Function to print colored texts
def color_text(text: str, color_code: str) -> None:
    print(f"\033[{color_code}m{text}\033[0m")
