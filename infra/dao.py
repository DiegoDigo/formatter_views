import pyodbc
from configparser import ConfigParser


config = ConfigParser()
config.read('settings\config.ini')
caminho = dict(config['CONFIG'])


def criar_view(view: str):
    try:
        print(view)
        _conn = pyodbc.connect('DSN={}'.format(caminho['dsn']))
        _cur = _conn.cursor()
        for sql in view.split(";\n"):
            _cur.execute(sql)
        _conn.commit()        
    except pyodbc.Error as e:
        raise Exception(e)
    finally:
        _conn.close()