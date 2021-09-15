# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['wplaty2.py'],
             pathex=['C:\\Users\\ROBERT\\Desktop\\IT\\PYTHON\\PYTHON 37 PROJEKTY\\wpłaty'],
             binaries=[],
             datas=[('C:\\Users\\Robert\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\ahk', 'ahk')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='wplaty2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
