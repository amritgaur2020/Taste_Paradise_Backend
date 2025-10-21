# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ('C:\\Users\\NITRO\\AppData\\Local\\Programs\\Python\\Python313\\python313.dll', '.'),
    ],
    datas=[
        ('frontend', 'frontend'),
        ('mongodb', 'mongodb'),
        ('static', 'static'),
        ('license_system.py', '.'),
    ],
    hiddenimports=[
        'clr_loader',
        'pythonnet',
        'webview',
        'webview.platforms.winforms',
        'fastapi',
        'fastapi.responses',
        'fastapi.staticfiles',
        'fastapi.middleware.cors',
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.responses',
        'starlette.staticfiles',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan.on',
        'motor',
        'motor.motor_asyncio',
        'pymongo',
        'passlib.handlers.bcrypt',
        'bcrypt',
        'pandas',
        'openpyxl',
        'apscheduler.schedulers.background',
        'apscheduler.triggers.cron',
        'psutil',
        'cryptography.fernet',
        'pydantic',
        'pydantic_core',
        'multipart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pytest', 'tkinter'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TasteParadise',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TasteParadise',
)
