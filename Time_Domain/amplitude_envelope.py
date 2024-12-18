# -*- coding: utf-8 -*-
"""amplitude_envelope.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MjdC_XHfky6nSxRGc_sfJhRRdsZzPnL-

Nesse scrip fiz alguns testes para encontrar o envelope de amplitude de um áudio
"""

import librosa
import librosa.display
import IPython.display as ipd
from google.colab import files

teste1 = "/content/teste1.wav" # Faz o upload do arquivo

# Substitua 'nome_do_arquivo' pelo nome do arquivo enviado
ipd.Audio(teste1, rate=44100)

#cria uma array com os valores de amplitude de cada sample
teste, sr = librosa.load(teste1)

teste

#funções adicionais para plotar o gráfico
import numpy as np
import matplotlib.pyplot as plt

# Cria o eixo de tempo
tempo = np.arange(0, len(teste)) / sr

# Plota o sinal de áudio
plt.figure(figsize=(10, 4))
plt.plot(tempo, teste)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Sinal de Áudio')
plt.show()

#duration of a sample
sample_duration = 1 / sr

#number of samples
size = len(teste)

#duration of the audio
duration = sample_duration * size

print(f'Every sample of this audio has a duration of {sample_duration:.6f} seconds and the audio in general has a duration of {duration:.6f} seconds')

FRAME_SIZE = 1024
HOP_LENGTH = 512

def amplitude_envelope(signal, frame_size, hop_length):
  amplitude_envelope = []

  #caminha entre os primeiros valores do frame
  for i in range(0, len(signal), hop_length):
    currant_frame_amplitude_envelope = max(signal[i:i+frame_size]) #pega o maior valor de amplitude de um frame
    amplitude_envelope.append(currant_frame_amplitude_envelope)

  return np.array(amplitude_envelope)

#mesma coisa da função anterior, mas de forma concisa
def fancy_amplitude_envelope(signal, frame_size, hop_length):
  return np.array([max(signal[i:i+frame_size]) for i in range(0, len(signal), hop_length)])

ae_teste = amplitude_envelope(teste, FRAME_SIZE, HOP_LENGTH)
len(ae_teste)

#visualização do envelope de amplitude

frames = range(0, ae_teste.size)
t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)

# Plota o sinal de áudio
plt.figure(figsize=(10, 4))
plt.plot(tempo, teste)
plt.plot(t, ae_teste, color='r')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Sinal de Áudio')
plt.show()