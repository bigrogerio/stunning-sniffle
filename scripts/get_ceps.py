from sniffle import invader
import pandas as pd
from tqdm import tqdm

BAIRROS_PATH = (
    "/home/rogerio/Dropbox/carrefour/coding_projects/stunning-sniffle/data/bairros.txt"
)
XLSX_PATH = (
    "/home/rogerio/Dropbox/carrefour/coding_projects/stunning-sniffle/data/response"
)

with open(BAIRROS_PATH, "r") as f:
    bairros = f.read().splitlines()
    f.close()
print(bairros)

lista_ceps = []
pbar = tqdm(total=len(bairros))
for i in bairros:
    temp = invader.BairroCEP(i)
    lista_ceps.extend(temp.bairro_ceps)
    pbar.update(1)

pbar.close()
payload = {"ZipCodeStart": lista_ceps, "ZipCodeEnd": lista_ceps}
new_df = pd.DataFrame(data=payload)
new_df["PolygonName"] = ""
new_df["WeightStart"] = 0.000001
new_df["WeightEnd"] = 999999999
new_df["AbsoluteMoneyCost"] = 0
new_df["PricePercent"] = 0
new_df["PriceByExtraWeight"] = 0
new_df["MaxVolume"] = 10000000
new_df["TimeCost"] = "00:00:00"
new_df["Country"] = "BRA"
new_df["MinimumValueInsurance"] = 0

new_df.to_excel("{}.xlsx".format(XLSX_PATH), index=False)
print(new_df)
