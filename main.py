import numpy as np
import librosa
import matplotlib.pyplot as plt
import pyaudio
import pygame
from mutagen.mp3 import MP3 as mp3

filepath = "./assets/music/Perfume_Polyrhythm.mp3"
def bpm_analyze():
    duration = 30
    x_sr = 200
    bpm_min, bpm_max = 60, 240

    # 楽曲の信号を読み込む
    y, sr = librosa.load(filepath, offset=38, duration=duration, mono=True)

    # ビート検出用信号の生成
    # リサンプリング & パワー信号の抽出
    x = np.abs(librosa.resample(y, sr, x_sr)) ** 2
    x_len = len(x)

    # 各BPMに対応する複素正弦波行列を生成
    M = np.zeros((bpm_max, x_len), dtype=np.complex)
    for bpm in range(bpm_min, bpm_max):
        thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / x_sr)
        M[bpm] = np.exp(-1j * thete)

    # 各BPMとのマッチング度合い計算
    #（複素正弦波行列とビート検出用信号との内積）
    x_bpm = np.abs(np.dot(M, x))

    # BPM　を算出
    bpm = np.argmax(x_bpm)
    return bpm

def make_metronome(bpmNum):
    # サンプリングレートを定義 --- (*1)
    RATE = 44100

    # BPMや音長を定義 --- (*2)
    BPM = bpmNum

    L1 = (60 / BPM * 4)
    L2, L4, L8 = (L1 / 2, L1 / 4, L1 / 8)

    # ドレミ...の周波数を定義 --- (*3)
    C, D, E, F, G, A, B, C2 = (
        261.626, 293.665, 329.628,
        349.228, 391.995, 440.000,
        493.883, 523.251)

    # サイン波を生成
    def tone(freq, length, gain):
        slen = int(length * RATE)
        t = float(freq) * np.pi * 2 / RATE
        return np.sin(np.arange(slen) * t) * gain

    # 再生
    def play_wave(stream, samples):
        stream.write(samples.astype(np.float32).tostring())

    # 出力用のストリームを開く（メトロノーム）
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    frames_per_buffer=1024,
                    output=True)

    # 再生
    print("play")
    pygame.mixer.init()
    click = pygame.mixer.Sound('./assets/click.wav')
    pygame.mixer.init(frequency=mp3(filepath).info.sample_rate)  # 曲のサンプリング周波数を取得しその値で初期化する。
    pygame.mixer.music.load(filepath) # ファイルの読み込み
    mp3_music = pygame.mixer.Sound(filepath)
    mp3_length = mp3(filepath).info.length  # 曲の長さを取得
    #pygame.mixer.music.play()
    mp3_music.play()
    #click.play()


    i = 0
    while i < 60:
        play_wave(stream, tone(E, L4, 1.0))
        #click.play()
        i+= 1
    stream.close()
    #pyaudioがないと音源が流れない謎

def play_music(bpm):
    pygame.init()

    BPM = bpm
    beats_per_ms = (BPM / 60) / 1000
    ms_per_beat = 1 / beats_per_ms
    PLAY_CLICK = pygame.USEREVENT + 1

    pygame.display.set_mode((200,100))
    click = pygame.mixer.Sound('./assets/click.wav')
    pygame.mixer.init(frequency=mp3(filepath).info.sample_rate)  # 曲のサンプリング周波数を取得しその値で初期化する。
    pygame.mixer.music.load(filepath) # ファイルの読み込み
    mp3_music = pygame.mixer.Sound(filepath)
    mp3_length = mp3(filepath).info.length  # 曲の長さを取得
    pygame.mixer.music.play()
    #mp3_music.play()
    #click.play()
    clock = pygame.time.Clock()
    pygame.time.set_timer(PLAY_CLICK, int(ms_per_beat))
    clock.tick(10)
    while pygame.mixer.music.get_busy():
        click.play()
        pygame.event.poll()
        clock.tick(10)
#main
if __name__ == '__main__':
     thisBpm = bpm_analyze()
     print(thisBpm)
     #make_metronome(thisBpm)
     play_music(thisBpm)