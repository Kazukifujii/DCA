
import pandas as pd
import subprocess
import time


download_base_address = lambda cifid:f'https://asia.iza-structure.org/IZA-SC/cif/{cifid}.cif'

table = pd.read_html('https://europe.iza-structure.org/IZA-SC/ftc_table.php')[1]


idlist = table.to_numpy().flatten().tolist()
#idlistの要素すべてを大文字のアルファベット3文字になるようにする
idlist = [cifid if len(cifid)==3 else cifid[1:] for cifid in idlist]


for cifid in idlist:
    time.sleep(0.5)
    subprocess.run(f'wget {download_base_address(cifid)}',shell=True)