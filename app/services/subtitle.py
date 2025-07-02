
from app.utils.text_to_srt import text_to_srt

class SubtitleService:
    def __init__(self, config):
        self.config = config

    def generate_srt(self, word_boundaries, max_line_length=10):
        srt_content = ""
        subtitle_id = 1
        current_line = ""
        line_start_time = 0

        for i, word_info in enumerate(word_boundaries):
            word = word_info["text"]
            start_time = word_info["offset"] / 10000000  # Convert to seconds
            end_time = start_time + (word_info["duration"] / 10000000)

            if not current_line:
                line_start_time = start_time

            if len(current_line) + len(word) + 1 > max_line_length and current_line:
                srt_content += text_to_srt(subtitle_id, current_line, line_start_time, last_end_time)
                subtitle_id += 1
                current_line = word
                line_start_time = start_time
            else:
                if current_line:
                    current_line += " "
                current_line += word
            
            last_end_time = end_time

            # Add the last line if it's the end of the boundaries
            if i == len(word_boundaries) - 1 and current_line:
                srt_content += text_to_srt(subtitle_id, current_line, line_start_time, end_time)

        return srt_content
