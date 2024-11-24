import cv2
import imagehash
from PIL import Image
import numpy as np
import librosa
from moviepy.editor import VideoFileClip
import os

def extract_frames(video_path, frame_dir, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_list = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % frame_rate == 0:
            frame_path = os.path.join(frame_dir, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_list.append(frame_path)
            count += 1
    
    cap.release()
    return frame_list

def compare_frames(frame_list_1, frame_list_2):
    hashes_1 = [imagehash.phash(Image.open(frame)) for frame in frame_list_1]
    hashes_2 = [imagehash.phash(Image.open(frame)) for frame in frame_list_2]

    differences = []
    for h1, h2 in zip(hashes_1, hashes_2):
        differences.append(h1 - h2)
    
    avg_diff = sum(differences) / len(differences)
    return avg_diff

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mean_amplitude = np.mean(np.abs(y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    return mean_amplitude, spectral_centroid

def compare_audio_features(features_1, features_2):
    diff = np.abs(np.array(features_1) - np.array(features_2))
    return np.mean(diff)

def compare_videos(video_path_1, video_path_2):
    frame_dir_1 = "frames_video_1"
    frame_dir_2 = "frames_video_2"
    audio_path_1 = "audio_1.wav"
    audio_path_2 = "audio_2.wav"
    
    os.makedirs(frame_dir_1, exist_ok=True)
    os.makedirs(frame_dir_2, exist_ok=True)

    frames_1 = extract_frames(video_path_1, frame_dir_1)
    frames_2 = extract_frames(video_path_2, frame_dir_2)

    frame_difference = compare_frames(frames_1, frames_2)
    print(f"Frame difference (pHash): {frame_difference}")

    extract_audio(video_path_1, audio_path_1)
    extract_audio(video_path_2, audio_path_2)

    audio_features_1 = extract_audio_features(audio_path_1)
    audio_features_2 = extract_audio_features(audio_path_2)

    audio_difference = compare_audio_features(audio_features_1, audio_features_2)
    print(f"Audio difference: {audio_difference}")

    for file in os.listdir(frame_dir_1):
        os.remove(os.path.join(frame_dir_1, file))
    os.rmdir(frame_dir_1)

    for file in os.listdir(frame_dir_2):
        os.remove(os.path.join(frame_dir_2, file))
    os.rmdir(frame_dir_2)

    os.remove(audio_path_1)
    os.remove(audio_path_2)

    if frame_difference < 10 and audio_difference < 0.1:  # Adjust thresholds as needed
        return "The videos are identical."
    else:
        return "The videos are different or one is edited."
