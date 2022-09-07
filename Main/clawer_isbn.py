import sys
import pandas as pd
from pathlib import Path

sys.path.append(str(Path.cwd()))

from Classes.clawer import SpiderSearch

# install odfpy

def main():
    df_source = pd.read_excel(r'Source/test.ods',sheet_name='工作表1',engine='odf')
    isbn_s = df_source.loc[:,'ISBN'].to_list()
    main_p = SpiderSearch()
    df_book_s = main_p.QuoteByTexts(isbn_s, 5)
    star_s = [df.loc[0, 'star'] if df.empty else None for df in df_book_s]
    df_source.loc[:, '豆瓣评分'] = star_s
    df_source.to_excel(r'Source/test_mode.ods', sheet_name='工作表1', engine='odf')


if __name__ == '__main__':
    main()