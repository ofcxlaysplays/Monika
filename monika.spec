# monika.spec
from kivy_deps import sdl2, glew
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['monika.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=collect_submodules('kivy'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MonikaPrank',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Set to True if you want a console for debugging
)

# THIS IS THE CRITICAL PART FOR KIVY
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    name='cool'
)
