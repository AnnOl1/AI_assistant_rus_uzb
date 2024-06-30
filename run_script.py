import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}\n{stderr.decode('utf-8')}")
    else:
        print(stdout.decode('utf-8'))

# Получение переменных окружения
face = os.getenv('FACE')
audio = os.getenv('AUDIO')

# Клонирование репозитория
run_command("git clone https://github.com/zabique/Wav2Lip")

# Скачивание модели
run_command("wget 'https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA' -O './Wav2Lip/checkpoints/wav2lip_gan.pth'")

# Установка пакета GHC
run_command("pip install https://raw.githubusercontent.com/AwaleSajil/ghc/master/ghc-1.0-py3-none-any.whl")

# Установка зависимостей Wav2Lip
run_command("cd Wav2Lip && pip install -r requirements.txt")

# Скачивание модели s3fd
run_command("wget 'https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth' -O 'Wav2Lip/face_detection/detection/sfd/s3fd.pth'")

# Запуск inference.py с указанными аргументами
run_command(f"cd Wav2Lip && python inference.py --checkpoint_path './checkpoints/wav2lip_gan.pth' --face '{face}' --audio '{audio}'")
