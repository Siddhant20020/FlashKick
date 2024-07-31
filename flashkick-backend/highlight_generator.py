from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import numpy as np
import librosa
import os

def calculate_ema(data, window):
    """Calculate the Exponential Moving Average (EMA) of a data series."""
    ema = [data[0]]
    for x in data[1:]:
        ema.append((1 - 1/window) * ema[-1] + (1/window) * x)
    return np.array(ema)

def analyze_audio(video):
    """Extract audio from the video and analyze it to detect peaks."""
    try:
        audio = video.audio
        audio_path = "temp_audio.wav"
        audio.write_audiofile(audio_path)
        
        y, sr = librosa.load(audio_path)
        amplitude = np.abs(librosa.stft(y))
        energy = np.sum(amplitude, axis=0)
        smoothed_energy = calculate_ema(energy, window=30)
        
        peak_indices = np.where((smoothed_energy[1:-1] > smoothed_energy[:-2]) &
                                (smoothed_energy[1:-1] > smoothed_energy[2:]))[0] + 1
        peak_times = librosa.frames_to_time(peak_indices, sr=sr)
        
        os.remove(audio_path)
        
        return peak_times
    except Exception as e:
        print(f"An error occurred during audio analysis: {e}")
        return []

def detect_scenes(video):
    """Detect scene changes based on frame differencing."""
    try:
        frame_diffs = []
        last_frame = None
        
        for frame in video.iter_frames():
            if last_frame is not None:
                diff = np.sum((frame - last_frame) ** 2)
                frame_diffs.append(diff)
            last_frame = frame
        
        frame_diffs = np.array(frame_diffs)
        frame_diffs = frame_diffs / np.max(frame_diffs)
        smoothed_diffs = calculate_ema(frame_diffs, window=10)
        
        threshold = 0.5
        scene_indices = np.where(smoothed_diffs > threshold)[0]
        scene_times = video.fps * scene_indices
        
        return scene_times
    except Exception as e:
        print(f"An error occurred during scene detection: {e}")
        return []

def generate_highlights(source):
    """Generate a single highlight video with a maximum duration limit."""
    try:
        video = VideoFileClip(source)
        
        peak_times = analyze_audio(video)
        print(f"Detected audio peaks at: {peak_times}")
        
        scene_times = detect_scenes(video)
        print(f"Detected scene changes at: {scene_times}")
        
        key_times = sorted(set(peak_times) | set(scene_times))
        
        max_duration = 12 * 60  # 12 minutes
        total_duration = 0
        highlight_clips = []
        
        for i, time in enumerate(key_times):
            if total_duration >= max_duration:
                break
            start = max(0, time - 3)  # Start 3 seconds before the event
            end = min(video.duration, time + 3)  # End 3 seconds after
            clip_duration = end - start
            if total_duration + clip_duration > max_duration:
                end = start + (max_duration - total_duration)
                clip_duration = end - start
            highlight_clips.append(video.subclip(start, end))
            total_duration += clip_duration
            print(f"Added segment from {start} to {end} ({clip_duration} seconds)")
        
        if highlight_clips:
            final_clip = concatenate_videoclips(highlight_clips)
            output_path = "highlights/highlight_video.mp4"
            final_clip.write_videofile(output_path, codec="libx264")
            print(f"Saved single highlight video to {output_path}")
        else:
            print("No highlights were detected.")
        
        print("Highlight generation completed.")
        return True

    except Exception as e:
        print(f"An error occurred during highlight generation: {e}")
        return False
