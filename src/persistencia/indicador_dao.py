from persistencia.conexion import abrir_conexion

class IndicadorDAO:
    SQL_GUARDAR = """
    INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en
    """


@staticmethod
def guardar(fuente, codigo, fecha, valor, unidad, verificado_en):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                IndicadorDAO.SQL_GUARDAR,
                (fuente, codigo, fecha, valor, unidad, verificado_en)
            )
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()    

@staticmethod
def buscar_ultimo(fuente, codigo):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT fuente, codigo, fecha, valor, unidad, verificado_en
            FROM indicador_api
            WHERE fuente = ? AND codigo = ?
            ORDER BY fecha DESC LIMIT 1
        """
        cursor.execute(sql, (fuente, codigo))
        fila = cursor.fetchone()
        conexion.close()
        return fila            