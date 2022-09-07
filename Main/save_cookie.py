import sys
from pathlib import Path

sys.path.append(str(Path.cwd()))

from Classes.cookies import CookiesDouban

uid = '13588267372'
pwd = 'nimingxue1006'

def main():
    main_p = CookiesDouban(uid, pwd)
    main_p.SaveCookie_driver()

if __name__ == '__main__':
    main()