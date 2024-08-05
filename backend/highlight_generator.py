import os
import io
import numpy as np
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from multiprocessing import Pool
import logging
import json

# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensuring necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Key events to search for in the transcript
KEY_EVENTS = ['goal', 'foul', 'half', 'substitution', 'penalty', 'free kick', 'corner', 'yellow card', 'red card']

def transcribe_video_with_whisper(video_path, audio_path, transcript_output_path):
    """Transcribe the video audio using Whisper."""
    try:
        logging.info("Transcribing video with Whisper...")
        model = whisper.load_model("base")
        
        # Extracting audio from video
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} was not created.")
        
        # Transcribing audio
        result = model.transcribe(audio_path)
        transcript = result.get("segments", [])
        formatted_transcript = [{
            "start": seg["start"],
            "end": seg["end"],
            "lines": [seg["text"]]
        } for seg in transcript]

        # Saving formatted transcript to a JSON file
        with open(transcript_output_path, 'w') as f:
            json.dump(formatted_transcript, f, indent=4)

        return formatted_transcript
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        raise

def tokenize_and_extract_events(transcript, tokenized_output_path):
    """Tokenize transcript and extract events."""
    try:
        logging.info("Tokenizing and extracting events...")
        stop_words = set(stopwords.words('english'))
        punctuation = set(string.punctuation)
        
        highlights = []
        tokenized_output = []

        for item in transcript:
            start = item.get('start', '')
            end = item.get('end', '')
            description = item.get('lines', '')

            line_tokens = word_tokenize(' '.join(description))
            cleaned_tokens = [token.lower() for token in line_tokens if token.lower() not in stop_words and token not in punctuation]

            tokenized_output.append({
                'start': start,
                'end': end,
                'tokens': cleaned_tokens
            })

            for event in KEY_EVENTS:
                if event in cleaned_tokens:
                    highlights.append({
                        'start': start,
                        'end': end,
                        'event_type': event,
                        'description': ' '.join(cleaned_tokens)
                    })
        
        # Saving tokenized output to a JSON file
        with open(tokenized_output_path, 'w') as f:
            json.dump(tokenized_output, f, indent=4)
        
        return highlights
    except Exception as e:
        logging.error(f"Error during tokenization and event extraction: {e}")
        raise

def generate_highlights_from_events(video, events):
    """Generate video highlights based on extracted events."""
    try:
        logging.info("Generating highlights from events...")
        highlights = []
        for event in events:
            start = max(0, float(event['start']) - 10)  # 10 seconds before the event
            end = min(video.duration, float(event['end']) + 10)  # 10 seconds after the event
            highlight_clip = video.subclip(start, end)
            highlights.append(highlight_clip)
        
        if highlights:
            final_highlight = concatenate_videoclips(highlights)
            output_file = "final_highlight.mp4"
            final_highlight.write_videofile(output_file, codec="libx264", audio_codec="aac")
            logging.info(f"Highlights saved to {output_file}")
            return highlights
        else:
            logging.info("No highlights generated.")
            return []
    except Exception as e:
        logging.error(f"Error generating highlights: {e}")
        return []

def process_video_chunk(args):
    """Process a chunk of the video."""
    video_path, start_time, end_time, audio_path, transcript_output_path, tokenized_output_path = args
    try:
        video = VideoFileClip(video_path)
        
        if end_time > video.duration:
            end_time = video.duration

        if start_time >= end_time:
            return []

        chunk_clip = video.subclip(start_time, end_time)
        transcript = transcribe_video_with_whisper(video_path, audio_path, transcript_output_path)
        events = tokenize_and_extract_events(transcript, tokenized_output_path)
        highlights = generate_highlights_from_events(chunk_clip, events)
        
        return highlights if highlights else []
    except Exception as e:
        logging.error(f"Error processing video chunk: {e}")
        return []

def generate_highlights(video_path, is_stream=False, chunk_duration_minutes=10):
    """Generate highlights from the video."""
    try:
        logging.info("Generating highlights...")
        if is_stream:
            video = VideoFileClip(io.BytesIO(video_path))
        else:
            video = VideoFileClip(video_path)
        
        highlights_dir = "highlights"
        os.makedirs(highlights_dir, exist_ok=True)
        
        chunk_duration = chunk_duration_minutes * 60
        video_duration = video.duration
        
        num_chunks = int(np.ceil(video_duration / chunk_duration))
        
        logging.info(f"Total duration: {video_duration} seconds")
        logging.info(f"Chunk duration: {chunk_duration} seconds")
        logging.info(f"Number of chunks: {num_chunks}")

        transcript_output_dir = os.path.join(highlights_dir, "transcripts")
        tokenized_output_dir = os.path.join(highlights_dir, "tokenized_outputs")
        os.makedirs(transcript_output_dir, exist_ok=True)
        os.makedirs(tokenized_output_dir, exist_ok=True)

        with Pool() as pool:
            chunk_args = [
                (
                    video_path, 
                    i * chunk_duration, 
                    min((i + 1) * chunk_duration, video_duration),
                    f"temp_audio_chunk_{i}.wav",
                    os.path.join(transcript_output_dir, f"transcript_chunk_{i}.json"),
                    os.path.join(tokenized_output_dir, f"tokenized_output_chunk_{i}.json")
                )
                for i in range(num_chunks)
            ]
            results = pool.map(process_video_chunk, chunk_args)
        
        highlight_clips = [clip for sublist in results for clip in sublist if isinstance(sublist, list)]
        
        if highlight_clips:
            final_highlight = concatenate_videoclips(highlight_clips)
            output_file = os.path.join(highlights_dir, "final_highlight.mp4")
            final_highlight.write_videofile(output_file, codec="libx264", audio_codec="aac")
            logging.info(f"Highlights saved to {output_file}")
            return True
        else:
            logging.info("No highlights generated.")
            return False
    except Exception as e:
        logging.error(f"Error generating highlights: {e}")
        raise   
