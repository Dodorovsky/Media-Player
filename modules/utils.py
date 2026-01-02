def format_time(ms):
    if ms < 0:
        ms = 0
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}" 
