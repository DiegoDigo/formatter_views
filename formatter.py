import getpass
import os
from configparser import ConfigParser
from re import findall, sub
from infra import dbmaker
from resouces import resouce


def criar_diretorio_destino(destino: str) -> None:
    """ cria a estrutura de pasta que vem do arquivo de configuração. """

    path_view = os.path.join(destino, 'views')
    path_procs = os.path.join(destino, 'procedures')

    if not os.path.exists(path_view):
        os.makedirs(path_view)

    if not os.path.exists(path_procs):
        os.makedirs(path_procs)


def pegar_arquivos(caminho: str) -> list:
    """ lista todos os arquivos do diretorio. """
    return os.listdir(caminho)


def pegar_nomes(texto: str) -> list:
    """ retorna os nomes das tabelas. """
    return findall(r"(?:[\.\s])([a-zA-Z]+\d{2})(?:[\.\s])", texto)


def gravar_arquivo(caminho: str, texto: str) -> None:
    """ grava o arquivo editado. """
    with open(caminho, "w", encoding="iso-8859-1") as arq:
        arq_final = sub(r"PERM" + caminho_conf["num_empresa"] + "\s", "PERM09", trocar_schema(texto))
        arq.write(arq_final)


def formatar_string(destino: str, texto: str, arquivo: str, tipo: str, num_empresa: int) -> None:
    """ subistitui o nome da tabela para o padrão configurado. """
    for nome in pegar_nomes(texto):
        texto = sub(nome, nome[:-2] + num_empresa, texto)
    gravar_arquivo(os.path.join(os.path.join(destino, tipo), arquivo), texto)


def ler_arquivo(destino: str, caminho: str, arquivo: str, tipo: str, num_empresa: int) -> None:
    """ ler o arquivo e formata a string com o padrao de schama. """
    criar_diretorio_destino(destino)
    print("gerando o arquivo {}".format(arquivo))
    with open(os.path.join(caminho, arquivo), encoding="iso-8859-1") as arq:
        formatar_string(destino, arq.read(), arquivo, tipo, num_empresa)


def trocar_schema(texto: str) -> str:
    """  troca o schema das tabelas. """
    novo_texto = ''
    for line in texto.split('\n'):
        for key in caminho_conf.keys():
            for i in set(findall(r'\?{}\.'.format(key), texto)):
                line = sub(i, caminho_conf[i], line)
        novo_texto += line + "\n"
    return novo_texto


def salvar_dbmaker(dsn: str, tipo: str) -> None:
    """ ler o diretorio do arquivos formatado e salva no dbmaker. """
    print("Salvando {} dbmaker, aguarde...".format(tipo))
    path_views = os.path.join(caminho_conf['destino'], tipo)
    for view in os.listdir(path_views):
        with open(os.path.join(path_views, view), 'r', encoding="iso-8859-1") as arq:
            if tipo == "views":
                dbmaker.criar_view(arq.read(), dsn)
            else:
                dbmaker.criar_procedure(arq.read(), dsn)


if __name__ == "__main__":

    default = dict(dbmaker='True')

    user = input("Digite usuario: ")
    password = getpass.getpass()

    if user == dbmaker.USER_SUP['user'] and password == dbmaker.USER_SUP['password']:
        print("Lendo arquivos ..")

        pasta_views = os.path.join(
            os.path.join(os.path.join(resouce.NOME_PASTA + "\\views",
                                  os.listdir(resouce.extrair_arquivo())[0])), 'views')
        pasta_prodeures = os.path.join(
            os.path.join(os.path.join(resouce.NOME_PASTA + "\\views",
                                  os.listdir(resouce.extrair_arquivo())[0])), 'procedures')

        config = ConfigParser(default, allow_no_value=True)
        config.read('settings\config.ini')
        caminho_conf = dict(config['CONFIG'])

        for arquivo in pegar_arquivos(pasta_views):
            ler_arquivo(caminho_conf["destino"], pasta_views, arquivo, "views", caminho_conf["num_empresa"])

        for arquivo in pegar_arquivos(pasta_prodeures):
            ler_arquivo(caminho_conf["destino"], pasta_prodeures, arquivo, "procedures", caminho_conf["num_empresa"])

        if caminho_conf['dbmaker'] == 'true':
            salvar_dbmaker(caminho_conf['dsn'], 'views')
            salvar_dbmaker(caminho_conf['dsn'], 'procedures')

        input("Press Any key to exit")
    else:
        print("usuario e senha invalido !")
