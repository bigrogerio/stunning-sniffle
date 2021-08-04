import pandas as pd
import requests


class BairroCEP:
    """
    This class is intended to (...)
    """

    def __init__(self, bairro):
        self.bairro = bairro
        self.bairro_ceps = self.get_cep_from_bairros(bairro)

    def get_cep_from_bairros(self, bairro):

        bairro_pre_input = bairro
        bairro_input = ""
        if " " in bairro_pre_input:
            bairro_word_list = bairro_pre_input.split()

            for index in bairro_word_list:
                if index == bairro_word_list[-1]:
                    bairro_input = bairro_input + index
                else:
                    bairro_input = bairro_input + index + "%20"
        else:
            bairro_input = bairro_pre_input

        API = "https://buscacepinter.correios.com.br/app/logradouro_bairro/carrega-logradouro-bairro.php"

        payload = "letraLocalidade=&letraBairro=&cepaux=&pagina=%2Fapp%2Flogradouro_bairro%2Findex.php&mensagem_alerta=&uf=SP&localidade=S%C3%A3o%20Paulo&bairro={}".format(
            bairro_input
        )

        headers = {
            "Host": "buscacepinter.correios.com.br",
            "Cookie": "buscacep=lp5gaf7fpm2j7gqa0eqvlqoor6; cws-%3FEXTERNO_2%3Fpool_Proxy_reverso_cws_443=BIABKIMA",
            "Content-Length": "156",
            "Sec-Ch-Ua": "'Chromium';v='91', ' Not;A Brand';v='99'",
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://buscacepinter.correios.com.br",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://buscacepinter.correios.com.br/app/logradouro_bairro/index.php",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close",
        }

        r = requests.post(API, data=payload, headers=headers)
        resultados = r.json()["total"]
        i = 0

        ceps_list = []

        while i < resultados:

            j = i + 50

            if j < resultados:
                payload = "letraLocalidade=&letraBairro=&cepaux=&pagina=%2Fapp%2Flogradouro_bairro%2Findex.php&mensagem_alerta=&uf=SP&localidade=S%C3%A3o%20Paulo&bairro={}&inicio={}&final={}".format(
                    bairro_input, i + 1, j
                )

                r = requests.post(API, data=payload, headers=headers)
                ceps = r.json()["dados"]

                for j in ceps:
                    ceps_list.append(j["cep"])

                i = i + 50

            else:
                j = resultados

                payload = "letraLocalidade=&letraBairro=&cepaux=&pagina=%2Fapp%2Flogradouro_bairro%2Findex.php&mensagem_alerta=&uf=SP&localidade=S%C3%A3o%20Paulo&bairro={}&inicio={}&final={}".format(
                    bairro_input, i + 1, j
                )

                r = requests.post(API, data=payload, headers=headers)
                ceps = r.json()["dados"]

                for j in ceps:
                    ceps_list.append(j["cep"])

                i = i + 50

        return ceps_list
