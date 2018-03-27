import pyodbc

USER_SUP = {
    'user': 'suporte',
    'password': 'cuidado'
}


def criar_view(view: str, dsn: str) -> None:
    """  Recria ou cria as views na base do DBMAKER baseado na conexao DSN. """
    try:
        _conn = pyodbc.connect('DSN={}'.format(dsn))
        _cur = _conn.cursor()
        for sql in view.split(";"):
            if sql != '\n':
                if not sql.__contains__("create function"):
                    _cur.execute(sql)
                    _conn.commit()
    except pyodbc.Error as e:
        raise Exception(e)
    finally:
        _conn.close()


def criar_procedure(procedure: str, dsn: str) -> None:
    """  Recria ou cria as Procedures na base do DBMAKER baseado na conexao DSN. """
    try:
        _conn = pyodbc.connect('DSN={}'.format(dsn), autocommit=True)
        _cur = _conn.cursor()
        _cur.execute(procedure)
        _conn.commit()
    except pyodbc.Error as e:
        raise Exception(e)
    finally:
        _conn.close()