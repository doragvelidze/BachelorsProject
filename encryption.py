import pyAesCrypt
from pathlib import PureWindowsPath
import os, shutil
BUFFER_SIZE = 64 * 1024

def encrypt(input_path, output_path, password):
    in_file = PureWindowsPath(input_path)
    out_path = f"{output_path}\\{in_file.name}.aes"
    pyAesCrypt.encryptFile(input_path, out_path, password, BUFFER_SIZE)


def decrypt(input_path, output_path, password):
    in_file = PureWindowsPath(input_path).name[:-4]
    out_path = f"{output_path}\\{in_file}"
    pyAesCrypt.decryptFile(input_path, out_path, password, BUFFER_SIZE)

                 


