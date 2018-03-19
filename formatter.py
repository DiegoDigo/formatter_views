import os
from re import findall, sub
from configparser import ConfigParser
from pathlib import Path
from infra import dao

def criar_diretorio_destino(destino: str) -> None: 
    path = Path(destino)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        if path.exists():
             os.makedirs(os.path.join(destino, "views"))
             os.makedirs(os.path.join(destino, "procedures"))


def pegar_arquivos(caminho: str) -> list:
    """ lista todos os arquivos do diretorio """
    return os.listdir(caminho)


def pegar_nomes(texto: str) -> list:
    """ retorna os nomes das tabelas """
    return findall(r"\.?([a-zA-Z]{4}\d{2}|[a-zA-Z]{6}\d{2})\.", texto)



def gravar_arquivo(caminho: str, texto: str) -> None:
    """ grava o arquivo editado """
    # with open(caminho, "a", encoding="iso-8859-1") as arq:
    #     arq.write(trocar_schema(texto))
    dao.criar_view(trocar_schema(texto))



def formatar_string(destino: str, texto: str, arquivo: str, tipo: str, num_empresa: int) -> None:
    """ subistitui o nome da tabela pelo novo nome """
    for nome in pegar_nomes(texto):
         texto = sub(nome, nome[:-2] + num_empresa, texto)
    gravar_arquivo(os.path.join(os.path.join(destino, tipo), arquivo), texto)



def ler_arquivo(destino: str, caminho: str, arquivo: str, tipo: str, num_empresa: int) -> None:
    """ ler o arquivo  """
    criar_diretorio_destino(destino)
    print("gerando o arquivo {}".format(arquivo))
    with open(os.path.join(caminho, arquivo), encoding="iso-8859-1") as arq:
        formatar_string(destino, arq.read(), arquivo, tipo, num_empresa)


def trocar_schema(texto: str) -> str:    
    novo_texto = ''
    for line in texto.split('\n'):    
        for key in caminho.keys():                          
            for i in set(findall(r'\?{}\.'.format(key),texto)):
                line = sub(i,caminho[i], line) 
        novo_texto += line + "\n"
    return novo_texto



if __name__ == "__main__":
    
    config = ConfigParser()
    config.read('settings\config.ini')
    caminho = dict(config['CONFIG'])

    for arquivo in pegar_arquivos(caminho["views"]):
        ler_arquivo(caminho["destino"], caminho["views"], arquivo, "views", caminho["num_empresa"])

    for arquivo in pegar_arquivos(caminho["proc"]):
        ler_arquivo(caminho["destino"], caminho["proc"], arquivo, "procedures", caminho["num_empresa"])

    input("Press Any key to exit")