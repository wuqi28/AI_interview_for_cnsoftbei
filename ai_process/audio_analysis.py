import librosa
import numpy as np


def analyze_wav_audio(audio_path, speaker_text):
    y, sr = librosa.load(audio_path, sr=16000)

    # 音频总时长
    duration = librosa.get_duration(y=y, sr=sr)

    # ------------------- 语调分析（Pitch） -------------------
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    avg_pitch = float(np.mean(pitch_values)) if pitch_values.size > 0 else 0

    # ------------------- 静音分析（停顿） -------------------
    intervals = librosa.effects.split(y, top_db=25)
    speech_time = sum([(end - start) / sr for start, end in intervals])
    pause_time = duration - speech_time
    pause_ratio = round(pause_time / duration, 2)
    pause_count = int(pause_time // 2)

    # ------------------- 语速分析 -------------------
    real_word_count = len(speaker_text)
    words_per_minute = real_word_count / (speech_time / 60)

    return {
        "avg_pitch": round(avg_pitch, 2),  # 平均音高（Hz）
        "speech_time": round(speech_time, 2),  # 有效语音时长（秒）
        "pause_time": round(pause_time, 2),  # 静音总时长（秒）
        "pause_ratio": pause_ratio,  # 静音占比
        "pause_count": pause_count,  # 停顿数量（估算）
        "words_per_minute": words_per_minute / 2  # 语速（词/分钟）
    }
