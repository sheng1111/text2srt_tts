import re
import string
from app.utils.text_to_srt import text_to_srt


class SubtitleService:
    """
    Service for generating SRT subtitles with intelligent text segmentation.
    Handles punctuation preservation and spacing optimization.
    """

    def __init__(self, config):
        """
        Initialize the subtitle service.

        Args:
            config: Configuration dictionary
        """
        self.config = config

    def generate_srt(self, word_boundaries, max_line_length=40, preserve_punctuation=True):
        """
        Generate SRT content from word boundaries with improved text processing.

        Args:
            word_boundaries: List of word boundary info from TTS service
            max_line_length: Maximum characters per subtitle line
            preserve_punctuation: Whether to preserve punctuation marks

        Returns:
            str: Complete SRT content
        """
        if not word_boundaries:
            return ""

        # Clean and prepare word boundaries
        cleaned_boundaries = self._clean_word_boundaries(
            word_boundaries, preserve_punctuation)

        if not cleaned_boundaries:
            return ""

        srt_content = ""
        subtitle_id = 1

        # Group words into logical subtitle segments
        segments = self._create_segments(cleaned_boundaries, max_line_length)

        for segment in segments:
            if segment['words']:
                # Build subtitle text with proper spacing
                subtitle_text = self._build_subtitle_text(
                    segment['words'], preserve_punctuation)

                # Skip empty segments
                if not subtitle_text.strip():
                    continue

                # Generate SRT block
                srt_content += text_to_srt(
                    subtitle_id,
                    subtitle_text,
                    segment['start_time'],
                    segment['end_time']
                )
                subtitle_id += 1

        return srt_content

    def _clean_word_boundaries(self, word_boundaries, preserve_punctuation):
        """
        Clean and filter word boundaries, handling punctuation and empty words.

        Args:
            word_boundaries: Raw word boundary data
            preserve_punctuation: Whether to preserve punctuation

        Returns:
            List of cleaned word boundaries
        """
        cleaned = []

        for word_info in word_boundaries:
            word = word_info["text"]

            # Skip completely empty words
            if not word or not word.strip():
                continue

            # Clean the word
            cleaned_word = self._clean_word(word, preserve_punctuation)

            # Skip if cleaning resulted in empty word
            if not cleaned_word:
                continue

            # Create cleaned word info
            cleaned_info = {
                "text": cleaned_word,
                "offset": word_info["offset"],
                "duration": word_info["duration"]
            }

            cleaned.append(cleaned_info)

        return cleaned

    def _clean_word(self, word, preserve_punctuation):
        """
        Clean individual word, handling punctuation and whitespace.

        Args:
            word: Original word text
            preserve_punctuation: Whether to preserve punctuation

        Returns:
            str: Cleaned word
        """
        # Remove extra whitespace
        word = word.strip()

        if not preserve_punctuation:
            # Remove punctuation but keep alphanumeric and basic symbols
            word = re.sub(r'[^\w\s\-\']', '', word)

        # Clean up multiple spaces
        word = re.sub(r'\s+', ' ', word)

        return word.strip()

    def _create_segments(self, word_boundaries, max_line_length):
        """
        Create logical segments from word boundaries based on timing and length.

        Args:
            word_boundaries: List of cleaned word boundary info
            max_line_length: Maximum characters per line

        Returns:
            List of segments with start_time, end_time, and words
        """
        segments = []
        current_segment = {
            'words': [],
            'start_time': 0,
            'end_time': 0,
            'char_count': 0
        }

        for i, word_info in enumerate(word_boundaries):
            word = word_info["text"]
            start_time = word_info["offset"] / 10000000  # Convert to seconds
            duration = word_info["duration"] / 10000000
            end_time = start_time + duration

            # Initialize segment if it's the first word
            if not current_segment['words']:
                current_segment['start_time'] = start_time

            # Calculate estimated length with this word
            space_needed = 1 if current_segment['words'] else 0
            estimated_length = current_segment['char_count'] + \
                len(word) + space_needed

            # Determine if we should start a new segment
            should_break = self._should_break_segment(
                current_segment, word, estimated_length, max_line_length, i, word_boundaries
            )

            if should_break:
                # Finalize current segment
                if current_segment['words']:
                    current_segment['end_time'] = current_segment['words'][-1]['end_time']
                    segments.append(current_segment)

                # Start new segment
                current_segment = {
                    'words': [{'text': word, 'start_time': start_time, 'end_time': end_time}],
                    'start_time': start_time,
                    'end_time': end_time,
                    'char_count': len(word)
                }
            else:
                # Add word to current segment
                current_segment['words'].append({
                    'text': word,
                    'start_time': start_time,
                    'end_time': end_time
                })
                current_segment['char_count'] += len(word) + space_needed
                current_segment['end_time'] = end_time

        # Add the last segment
        if current_segment['words']:
            segments.append(current_segment)

        return segments

    def _should_break_segment(self, current_segment, word, estimated_length, max_line_length, index, word_boundaries):
        """
        Determine if we should break the current segment and start a new one.

        Args:
            current_segment: Current segment being built
            word: Current word being processed
            estimated_length: Estimated total length with current word
            max_line_length: Maximum allowed length
            index: Current word index
            word_boundaries: All word boundaries

        Returns:
            bool: True if should break segment
        """
        # Don't break if no words in current segment
        if not current_segment['words']:
            return False

        # Break if exceeding max length
        if estimated_length > max_line_length:
            return True

        # Check for natural break points
        has_natural_break = (
            current_segment['char_count'] >= max_line_length * 0.6 and
            self._is_natural_break_point(
                current_segment['words'][-1]['text'], word)
        )
        if has_natural_break:
            return True

        # Check for long pause if we have timing information
        if len(current_segment['words']) > 0 and index > 0:
            last_word = current_segment['words'][-1]
            current_start = word_boundaries[index]["offset"] / 10000000
            previous_duration = word_boundaries[index-1]["duration"] / 10000000
            last_end = last_word['start_time'] + previous_duration

            # If there's a pause longer than 0.5 seconds, consider breaking
            if current_start - last_end > 0.5:
                return True

        return False

    def _is_natural_break_point(self, previous_word, current_word):
        """
        Determine if this is a natural point to break the subtitle.

        Args:
            previous_word: Previous word text
            current_word: Current word text

        Returns:
            bool: True if this is a natural break point
        """
        # Check if previous word ends with strong punctuation
        strong_punctuation = ['.', '!', '?', '。', '！', '？']
        for mark in strong_punctuation:
            if previous_word.endswith(mark):
                return True

        # Check if previous word ends with medium punctuation
        medium_punctuation = [',', ';', ':', '，', '；', '：']
        for mark in medium_punctuation:
            if previous_word.endswith(mark):
                return True

        # Check for transition words that often start new clauses
        transition_words = [
            'and', 'but', 'or', 'so', 'then', 'however', 'therefore',
            'moreover', 'furthermore', 'meanwhile', 'consequently', 'also',
            'additionally', 'finally', 'firstly', 'secondly', 'lastly',
            '而且', '但是', '然而', '因此', '所以', '然後', '同時', '另外',
            '首先', '其次', '最後', '此外', '再者', '接著', '最終'
        ]

        if current_word.lower() in transition_words:
            return True

        return False

    def _build_subtitle_text(self, words, preserve_punctuation):
        """
        Build subtitle text from word list with proper spacing and formatting.

        Args:
            words: List of word dictionaries
            preserve_punctuation: Whether to preserve punctuation

        Returns:
            str: Formatted subtitle text
        """
        if not words:
            return ""

        # Extract text from words
        text_parts = [word['text'] for word in words]

        # Join with single spaces
        subtitle_text = ' '.join(text_parts)

        # Clean up spacing issues
        subtitle_text = self._fix_spacing(subtitle_text, preserve_punctuation)

        return subtitle_text.strip()

    def _fix_spacing(self, text, preserve_punctuation):
        """
        Fix spacing issues in subtitle text.

        Args:
            text: Input text
            preserve_punctuation: Whether punctuation is preserved

        Returns:
            str: Text with fixed spacing
        """
        if not text:
            return ""

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        if preserve_punctuation:
            # Fix spacing around punctuation
            # Remove space before punctuation
            text = re.sub(r'\s+([,.!?;:，。！？；：])', r'\1', text)
            # Ensure space after punctuation (if not at end)
            text = re.sub(r'([,.!?;:，。！？；：])([^\s])', r'\1 \2', text)

        # Fix spacing around quotes
        text = re.sub(r'\s*"\s*', '"', text)
        text = re.sub(r"\s*'\s*", "'", text)

        # Fix spacing around brackets
        text = re.sub(r'\s*\(\s*', '(', text)
        text = re.sub(r'\s*\)\s*', ')', text)

        # Remove spaces at the beginning and end
        text = text.strip()

        return text
