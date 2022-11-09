
from zipfile import ZipFile

import requests
import pandas as pd


SIGLAS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
     'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

def get_url(sigla):
    s_1 = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_2t_"
    s_2 = "_311020221535.zip"
    return s_1+sigla+s_2

def get_boletim_fname(sigla):
    s_1 = "bweb_2t_"
    s_2 = "_311020221535.csv"
    return s_1+sigla+s_2

def run():
    print("Baixando boletins de urna - segundo turno 2022")

    # Baixar dados
    for sigla in SIGLAS:
        # Baixar arquivo
        url = get_url(sigla)
        my_header = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers = my_header, timeout = 10)

        # Salvar arquivo localmente
        if response.ok:
            print("Baixei corretamente boletins de ", sigla)
            local_fname = sigla + ".zip"
            with open(local_fname, mode='wb') as file:
                file.write(response.content)
        else:
            print("Algo deu errado!")
            print("Codigo de resposta:", response.status_code)
            print("Reason:", response.reason)

    # Pré-processar para ficar em um único dataframe
    data_frames = []
    for sigla in SIGLAS:
        print("Abrindo arquivo de:", sigla)
        local_fname = sigla + ".zip"
        boletim_fname = get_boletim_fname(sigla)
        with ZipFile(local_fname, 'r') as zfile:
            boletim = zfile.extract(boletim_fname)
            df_ = pd.read_csv(boletim, encoding='latin1')
            data_frames.append(df_)
        
    df_total = pd.concat(data_frames)
    df_total.to_csv('boletins_2t_presidente_2022.csv')



if __name__ == "__main__":
    run()
