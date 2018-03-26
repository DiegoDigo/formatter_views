import os
from re import findall, sub
from configparser import ConfigParser
from pathlib import Path
from resouces import resouce
# from infra import dao


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
    return findall(r"(?:[\.\s])([a-zA-Z]+\d{2})(?:[\.\s])", texto)


def gravar_arquivo(caminho: str, texto: str) -> None:
    """ grava o arquivo editado """
    with open(caminho, "w", encoding="iso-8859-1") as arq:
        arq_final = sub(r"PERM"+caminho_conf["num_empresa"] + "\s", "PERM09", trocar_schema(texto))
        arq.write(arq_final)
    # dao.criar_view(trocar_schema(texto))


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
        for key in caminho_conf.keys():
            for i in set(findall(r'\?{}\.'.format(key), texto)):
                line = sub(i, caminho_conf[i], line)
        novo_texto += line + "\n"
    return novo_texto


if __name__ == "__main__":
    print("Lendo arquivos ..")

    pasta_views = os.path.join(
        os.path.join(os.path.join(resouce.NOME_PASTA + "\\views", os.listdir(resouce.extrair_arquivo())[0])),'views')
    pasta_prodeures = os.path.join(
        os.path.join(os.path.join(resouce.NOME_PASTA + "\\views", os.listdir(resouce.extrair_arquivo())[0])), 'procedures')

    config = ConfigParser()
    config.read('settings\config.ini')
    caminho_conf = dict(config['CONFIG'])

    for arquivo in pegar_arquivos(pasta_views):
        ler_arquivo(caminho_conf["destino"], pasta_views, arquivo, "views", caminho_conf["num_empresa"])

    for arquivo in pegar_arquivos(pasta_prodeures):
        ler_arquivo(caminho_conf["destino"], pasta_prodeures, arquivo, "procedures", caminho_conf["num_empresa"])

    input("Press Any key to exit")