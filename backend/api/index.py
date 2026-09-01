"""Entrypoint da Vercel.

A Vercel procura o objeto ASGI `app` neste arquivo.
Ele apenas reexporta o app definido em app/main.py.
"""
import sys
import os

# Garante que o pacote `app` seja encontrado
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402

# A Vercel usa este objeto `app`
