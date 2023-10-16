import base64
import os

from datetime import datetime
from cryptography.fernet import Fernet
from pathlib import Path

folder = 'gamification_logs'


class ConsoleGamification:

    def __init__(self):
        self.file_path = ""
        self.key = b'qpbwoA}91MY2J:{^k!hM>G%f+b5c@,mw'
        self.cipher = Fernet(base64.urlsafe_b64encode(self.key))

        if not os.path.exists(folder):
            Path(folder).mkdir(parents=True, exist_ok=True)

    def write(self, text):
        self.file_path = folder + '/resultados.txt'

        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(text)
            file.close()

    def write_encrypted(self, text, desafio):
        date = datetime.now().strftime("%d-%m-%Y")
        self.file_path = folder + '/desafio_' + str(desafio) + '_{}.txt'.format(date)
        text_encrypted = self.encrypt_text(text)

        with open(self.file_path, 'ab') as file:
            file.write(text_encrypted)
            file.close()

    def write_line(self, desafio):
        date = datetime.now().strftime("%d-%m-%Y")
        self.file_path = folder + '/desafio_' + str(desafio) + 'log_{}.txt'.format(date)

        with open(self.file_path, 'a') as file:
            file.write("\n")
            file.close()

    def encrypt_text(self, text):
        text_encrypted = self.cipher.encrypt(text.encode())
        return text_encrypted

    def decrypt_text(self, text):
        decrypted_text = self.cipher.decrypt(text.decode())
        return decrypted_text
