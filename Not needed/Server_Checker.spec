# -*- mode: python -*-

block_cipher = None


a = Analysis(['Server_Checker.py'],
             pathex=['C:\\Users\\Elliot\\OneDrive\\Documents\\School\\KS5\\Year 13\\Computing\\Python Programs\\Project - Combined Code - PyCharm'],
             binaries=[],
             datas=[],
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
          name='Server_Checker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
