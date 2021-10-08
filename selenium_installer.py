import sys
import shutil
import ctypes
from os import listdir
from zipfile import ZipFile
from shutil import rmtree, move
from platform import architecture
from urllib.request import urlretrieve
from winreg import QueryValueEx, OpenKey, KEY_READ, HKEY_CURRENT_USER


def get_msedge_driver():
    if 'msedgedriver.exe' in listdir('C:\\Windows'):
        return True
    else:
        print('[!] Could not find selenium driver')
        print('[!] Automatic driver installation')
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            quit()

    _edge_version = str(
        QueryValueEx(OpenKey(HKEY_CURRENT_USER, "Software\Microsoft\Edge\BLBeacon", 0, KEY_READ), "version")[0])

    if architecture()[0] == '64bit':
        _arch = '64'
    else:
        _arch = '32'

    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        _download_directory = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

        print('[+] Downloading driver from https://msedgedriver.azureedge.net ...')
        urlretrieve(f'https://msedgedriver.azureedge.net/{_edge_version}/edgedriver_win{_arch}.zip', _download_directory + f'\\edgedriver_win{_arch}.zip')
        print(f'[+] Extracting driver to {_download_directory}/edgedriver_win{_arch}.zip')
        with ZipFile(f'{_download_directory}\\edgedriver_win{_arch}.zip', 'r') as _zip:
            _zip.extractall(_download_directory)
        rmtree(f'{_download_directory}\\Driver_Notes')
        move(f'{_download_directory}\\\\msedgedriver.exe', 'C:\\Windows')


if __name__ == '__main__':
    get_msedge_driver()