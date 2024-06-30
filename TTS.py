import tkinter as tk
import pyaudio
import wave
import threading
import time
from tkinter import messagebox
import transcription_voice  
import answers_to_questions  
import STT  

class VoiceRecorderApp:
    def __init__(self, root, filename, language):
        self.root = root
        self.filename = filename
        self.language = language
        self.root.title("Voice Recorder")

        self.recording = False
        self.max_duration = 60  # Максимальная длительность записи в секундах

        self.start_button = tk.Button(root, text="Старт", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Стоп", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.frames = []

        # Настройки для записи
        self.chunk = 1024  # Размер блока данных
        self.sample_rate = 44100  # Частота дискретизации
        self.format = pyaudio.paInt16  # Формат аудио
        self.channels = 1  # Количество каналов (1 для моно, 2 для стерео)

        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        if self.recording:
            messagebox.showinfo("Info", "Запись уже идет.")
            return

        self.recording = True
        self.frames = []
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        self.record_thread = threading.Thread(target=self.record_audio)
        self.record_thread.start()

    def record_audio(self):
        start_time = time.time()
        while self.recording and (time.time() - start_time) < self.max_duration:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        if self.recording:
            self.stop_recording()

    def stop_recording(self):
        if not self.recording:
            messagebox.showinfo("Info", "Запись не идет.")
            return

        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Сохранение записи в файл
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

        messagebox.showinfo("Info", f"Запись завершена и сохранена в файл {self.filename}.")

        # Запускаем транскрипцию и синтез речи
        self.process_recording()

        # Закрытие приложения после остановки записи
        self.root.destroy()

    def process_recording(self):
        if self.language == 'rus':
            rus_phrase = transcription_voice.audio_transcription(self.filename, 'ru-RU')
            tts_answers_rus = answers_to_questions.create_answer(rus_phrase)
            STT.text_to_speech_rus(tts_answers_rus)
        elif self.language == 'uzb':
            uzb_phrase = transcription_voice.audio_transcription(self.filename, 'uz-UZ')
            tts_answers_uzb = answers_to_questions.create_answer(uzb_phrase)
            STT.text_to_speech_uzb(tts_answers_uzb)


def open_recorder(filename, language):
    root = tk.Tk()
    app = VoiceRecorderApp(root, filename, language)
    root.mainloop()


def open_language_selection():
    lang_window = tk.Tk()
    lang_window.title("Выбор языка")

    rus_button = tk.Button(lang_window, text="RUS", command=lambda: (lang_window.destroy(), open_recorder("recording_rus.wav", 'rus')))
    rus_button.pack(pady=10)

    uzb_button = tk.Button(lang_window, text="UZB", command=lambda: (lang_window.destroy(), open_recorder("recording_uzb.wav", 'uzb')))
    uzb_button.pack(pady=10)

    lang_window.mainloop()

if __name__ == "__main__":
    open_language_selection()
