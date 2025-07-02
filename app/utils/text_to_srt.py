import os
from datetime import timedelta

def format_time(seconds):
    """
    Formats seconds into the SRT time format (HH:MM:SS,ms).
    """
    delta = timedelta(seconds=seconds)
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    milliseconds = delta.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def text_to_srt(subtitle_id, text, start_time, end_time):
    """
    Generates a single SRT block.
    """
    start_str = format_time(start_time)
    end_str = format_time(end_time)
    return f"{subtitle_id}\n{start_str} --> {end_str}\n{text}\n\n"