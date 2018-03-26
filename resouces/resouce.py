from requests import get as _get
from zipfile import ZipFile
import os

URL = 'https://github.com/DiegoDigo/viewsPortal/archive/master.zip'
USER = ('di3g0d0ming05@gmail.com', 'amesma1012')
NOME_PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOME_ARQUIVO = URL.split('/')[-1]


def baixar_views() -> str:
    """  faz o download das views do arquivo vindo do github. """
    local_filename = os.path.join(NOME_PASTA, NOME_ARQUIVO)
    r = _get(URL, auth=USER, stream=True)
    if r.status_code == 200:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    # f.flush()
        return local_filename
    return None


def extrair_arquivo() -> str:
    """  Desconpactando arquivo baixado do github.  """
    pasta_zip = os.path.join(NOME_PASTA, "views")
    if not os.path.exists(pasta_zip):
        os.makedirs(pasta_zip)
    aquivo_zip = ZipFile(baixar_views())
    aquivo_zip.extractall(pasta_zip)
    aquivo_zip.close()
    return pasta_zip
