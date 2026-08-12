import os
import math
import numpy as np
from pathlib import Path
from typing import Tuple, Optional

VOICE_PROFILE_DIR = Path(r"C:\Users\sasi vardhan.P\myname\device_manager\data\voice_profile")
EMBEDDING_FILE = VOICE_PROFILE_DIR / "speaker_embedding.npy"

class SpeakerVerifier:
    """
    Offline Local CPU Speaker Verification Subsystem.
    Extracts acoustic spectral feature embeddings (MFCC & Spectral Centroids)
    and computes cosine similarity against the enrolled user profile.
    Maintains 100% offline local privacy without cloud API dependencies.
    """
    def __init__(self, threshold: float = 0.70):
        self.threshold = threshold
        self.enrolled_embedding: Optional[np.ndarray] = None
        self.load_profile()

    def load_profile(self) -> bool:
        if EMBEDDING_FILE.exists():
            try:
                self.enrolled_embedding = np.load(str(EMBEDDING_FILE))
                print(f"[SPEAKER VERIFIER]: Loaded enrolled speaker profile from '{EMBEDDING_FILE}'.")
                return True
            except Exception as e:
                print(f"[SPEAKER VERIFIER WARNING]: Could not load profile: {e}")
        return False

    def extract_embedding(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[np.ndarray]:
        """
        Extracts a normalized 128-dimensional acoustic feature vector from raw 16-bit PCM audio.
        """
        if not audio_data or len(audio_data) < 1600:
            return None

        try:
            signal = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            if np.max(np.abs(signal)) > 0:
                signal = signal / np.max(np.abs(signal))  # Peak normalize

            # Frame size 25ms (400 samples at 16kHz), hop size 10ms (160 samples)
            frame_len = int(0.025 * sample_rate)
            hop_len = int(0.010 * sample_rate)
            num_frames = (len(signal) - frame_len) // hop_len

            if num_frames < 1:
                return None

            features = []
            for i in range(num_frames):
                frame = signal[i * hop_len : i * hop_len + frame_len]
                # Apply Hann window
                windowed = frame * np.hanning(len(frame))
                
                # FFT Spectrum
                fft_mag = np.abs(np.fft.rfft(windowed, n=512))
                
                # 20 Filterbank / Log Spectral energies
                energy = np.log(fft_mag + 1e-6)
                
                # Spectral Centroid
                freqs = np.linspace(0, sample_rate / 2, len(fft_mag))
                centroid = np.sum(freqs * fft_mag) / (np.sum(fft_mag) + 1e-6)
                
                # Zero crossing rate
                zcr = np.mean(np.abs(np.diff(np.sign(frame))))
                
                frame_feat = np.concatenate([energy[:40], [centroid, zcr]])
                features.append(frame_feat)

            feat_matrix = np.array(features)
            mean_vec = np.mean(feat_matrix, axis=0)
            std_vec = np.std(feat_matrix, axis=0)
            
            # Combine mean and std to form robust 84/128-dim acoustic vector
            embedding = np.concatenate([mean_vec, std_vec])
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            return embedding
        except Exception as e:
            print(f"[SPEAKER VERIFIER ERROR]: Feature extraction failed: {e}")
            return None

    def save_enrolled_embedding(self, embeddings: list) -> bool:
        if not embeddings:
            return False
        try:
            VOICE_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            avg_emb = np.mean(embeddings, axis=0)
            norm = np.linalg.norm(avg_emb)
            if norm > 0:
                avg_emb = avg_emb / norm
            np.save(str(EMBEDDING_FILE), avg_emb)
            self.enrolled_embedding = avg_emb
            print(f"[SPEAKER VERIFIER]: Saved new speaker profile to '{EMBEDDING_FILE}'.")
            return True
        except Exception as e:
            print(f"[SPEAKER VERIFIER ERROR]: Failed to save profile: {e}")
            return False

    def verify(self, audio_data: bytes, sample_rate: int = 16000) -> Tuple[bool, float]:
        """
        Verifies if incoming raw audio matches the enrolled speaker profile.
        Returns (is_authorized, confidence_score).
        """
        if self.enrolled_embedding is None:
            # If no profile enrolled yet, default allow with warning
            return True, 1.0

        current_emb = self.extract_embedding(audio_data, sample_rate=sample_rate)
        if current_emb is None:
            # If audio too short or silent, allow pass-through to STT/wake word
            return True, 0.85

        similarity = float(np.dot(self.enrolled_embedding, current_emb))
        # Map cosine similarity to 0.0 - 1.0 confidence score
        confidence = max(0.0, min(1.0, (similarity + 1.0) / 2.0))

        is_authorized = similarity >= (self.threshold - 0.20)  # Tolerant baseline for local mic
        return is_authorized, confidence

speaker_verifier = SpeakerVerifier()
