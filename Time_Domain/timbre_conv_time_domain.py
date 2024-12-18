# -*- coding: utf-8 -*-
"""Timbre_Conv_Time_Domain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GY6bujXQbNZFQoVSPaHuyNKnsq9WnjDO

Esse script tenta deixar mais natural um áudio sintético utilizando as feature de amplitude envelope. Pela a análise dos resultados, não é a melhor forma de se fazer isso. Para fins de Teste é só alterar os parâmetros da função apply_adsr_to_segment
"""

import librosa
import librosa.display
import IPython.display as ipd
from google.colab import files
import numpy as np
import matplotlib.pyplot as plt

#função que divide o sinal em segmentos
def segment_audio(signal,sr=22100):
  # Detectar onsets (pontos onde novas notas ou ataques ocorrem)
  onset_frames = librosa.onset.onset_detect(y=signal, sr=sr, backtrack=True)
  onset_samples = librosa.frames_to_samples(onset_frames)

  # Dividir o áudio em segmentos
  segments = [signal[onset_samples[i]:onset_samples[i+1]] for i in range(len(onset_samples)-1)]

  return segments

# Função para criar e aplicar o envelope ADSR a um segmento
def apply_adsr_to_segment(segment, sr, attack=0.1, decay=0.2, sustain=0.7, release=0.2):
    """
    Aplica um envelope ADSR (Attack, Decay, Sustain, Release) a um segmento de áudio.

    Parâmetros:
        segment: array-like
            O segmento de áudio original.
        sr: int
            A taxa de amostragem do sinal (samples por segundo).
        attack: float
            Duração do ataque em segundos.
        decay: float
            Duração do decaimento em segundos.
        sustain: float
            Nível de sustentação (valor entre 0 e 1).
        release: float
            Duração da liberação em segundos.

    Retorna:
        segment_modificado: array-like
            O segmento de áudio com o envelope ADSR aplicado.
    """
    n_samples = len(segment)  # Número total de amostras no segmento

    # Calcular as durações de cada estágio do envelope em samples
    attack_samples = min(int(attack * sr), n_samples)
    decay_samples = min(int(decay * sr), n_samples - attack_samples)
    sustain_samples = max(0, n_samples - attack_samples - decay_samples - int(release * sr))
    release_samples = n_samples - attack_samples - decay_samples - sustain_samples

    # Inicializar o envelope
    env = np.zeros(n_samples)

    # 1. Ataque: Cresce de 0 até 1
    env[:attack_samples] = np.linspace(0, 1, attack_samples)

    # 2. Decaimento: Decresce de 1 até o nível de sustentação
    env[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)

    # 3. Sustentação: Mantém o nível constante
    env[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain

    # 4. Liberação: Decresce do nível de sustentação até 0
    if release_samples > 0:
        env[-release_samples:] = np.linspace(sustain, 0, release_samples)

    # Aplicar o envelope ao segmento original
    segment_modificado = segment * env

    return segment_modificado

# Função para processar uma lista de segmentos com ADSR e reconstruir o áudio
def process_audio_segments_with_adsr(segments, sr, attack=0.1, decay=0.2, sustain=0.7, release=0.2):
    """
    Aplica um envelope ADSR a cada segmento de áudio e concatena os segmentos processados.

    Parâmetros:
        segments: list of array-like
            Uma lista com os segmentos de áudio.
        sr: int
            A taxa de amostragem do sinal.
        attack, decay, sustain, release: float
            Parâmetros do envelope ADSR.

    Retorna:
        audio_modificado: array-like
            O áudio reconstruído com ADSR aplicado em cada segmento.
    """
    # Processar cada segmento com a função apply_adsr_to_segment
    segments_modificados = [apply_adsr_to_segment(segment, sr, attack, decay, sustain, release) for segment in segments]

    # Concatenar os segmentos processados
    audio_modificado = np.concatenate(segments_modificados)

    return audio_modificado

guitar_file = '/content/luthier_pick_nonoise_mono_body.flac'

guitar, sr = librosa.load(guitar_file)

ipd.display(ipd.Audio(guitar, rate=sr))

segmented_audio = segment_audio(guitar,sr)

new_audio = process_audio_segments_with_adsr(segmented_audio, sr,attack=0.04, decay=0.3, sustain=0.7, release=0.4)

ipd.display(ipd.Audio(new_audio, rate=sr))

time = np.linspace(0, len(new_audio) / sr, num=len(new_audio))

# Plotar o sinal modificado com amplitude envelope
plt.figure(figsize=(10, 4))
plt.plot(time, new_audio, color='g')
plt.title("Sinal de Áudio WAV no Domínio do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.tight_layout()
plt.show()

time = np.linspace(0, len(guitar) / sr, num=len(guitar))

# Plotar o sinal original
plt.figure(figsize=(10, 4))
plt.plot(time, guitar, color='b')
plt.title("Sinal de Áudio WAV no Domínio do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.tight_layout()
plt.show()