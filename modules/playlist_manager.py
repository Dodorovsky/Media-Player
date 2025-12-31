from tkinter import filedialog, messagebox 
import tkinter as tk
import os

def load_playlist(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        rutas = [linea.strip() for linea in f if linea.strip()]
    return rutas
 
def create_playlist(file_path):
    # Create a new empty playlist file
    with open(file_path, "w", encoding="utf-8") as f:
        pass
    return file_path

def add_to_playlist(file_path, rutas):
    """Add paths to a playlist file, avoiding duplicates."""
    # Read existing routes
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            existentes = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        existentes = set()

    new = []
    repeated = []

    for ruta in rutas:
        if ruta not in existentes:
            new.append(ruta)
        else:
            repeated.append(ruta)

     #Write only the new ones
    with open(file_path, "a", encoding="utf-8") as f:
        for ruta in new:
            f.write(ruta + "\n")

    return new, repeated
       