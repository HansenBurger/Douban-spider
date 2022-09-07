import json
from pathlib import Path

def ConfigRead(cate: str,
               name: str = '',
               file: Path = Path('config.json')) -> str:

    if not file.is_file():
        print('Json File Not Exist !')
        return None
    else:
        with open(str(file), encoding="utf-8") as f:
            data = json.load(f)

        if not name:
            return data[cate]
        else:
            return data[cate][name]