
def display_time(millis: int) -> str:
    if millis < 0:
        millis = 0
    seconds = millis // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"