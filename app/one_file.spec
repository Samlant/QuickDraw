# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app.py'],
    pathex=[
        '..\\..\\..\\..\\virtualenvs\\QuickDraw\\Lib\\site-packages', 
        '.\\model',
        '.\\model\\api',
        '.\\model\\api\\ms_graph',
        '.\\model\\api\\ms_graph\\utils',
        '.\\model\\api\\ms_graph\\workbooks_and_charts',
        '.\\model\\dir_handler',
        '.\\model\\email',
        '.\\model\\base_model.py',
        '.\\presenter',
        '.\\view',
        '.',
    ],
    binaries=[],
    datas=[
        ('.\\resources\\img\\app.ico', '.\\resources\\img'),
        ('.\\resources\\img\\sys_tray.ico', '.\\resources\\img'),
        ('.\\resources\\msedgedriver.exe', '.\\resources'),
        ],
    hiddenimports=[],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuickDraw',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\img\\app.ico'],
)
