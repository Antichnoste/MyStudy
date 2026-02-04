import ctypes
import ctypes.util
import os

# Просто пример как можно интегрировать ctypes в Python
user32 = ctypes.windll.user32
user32.MessageBoxW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
user32.MessageBoxW.restype = ctypes.c_int
user32.MessageBoxW(0, "Привет из Python!", "ctypes Демо (Windows)", 0x00000040)
print("Диалоговое окно закрыто.")