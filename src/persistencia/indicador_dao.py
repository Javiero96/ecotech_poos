from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, marcador_sql
from datetime import datetime

class IndicadorDAO:
    @staticmethod
    def guardar(indicador: Indicador) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        
        # Fecha de la verificación actual
        indicador.verificado_en = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Comprobar si ya existe esa fecha en esa fuente
        sql_check = f"SELECT id_indicador FROM indicador_api WHERE fuente={m} AND codigo={m} AND fecha={m}"
        cursor.execute(sql_check, (indicador.fuente, indicador.codigo, indicador.fecha))
        fila = cursor.fetchone()

        if fila:
            # 2. ACTUALIZAR (Evita duplicados)
            id_existente = fila[0]
            sql_update = f"UPDATE indicador_api SET valor={m}, unidad={m}, verificado_en={m} WHERE id_indicador={m}"
            cursor.execute(sql_update, (indicador.valor, indicador.unidad, indicador.verificado_en, id_existente))
        else:
            # 3. INSERTAR
            sql_insert = f"""
                INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad, verificado_en)
                VALUES ({m}, {m}, {m}, {m}, {m}, {m})
            """
            cursor.execute(sql_insert, (indicador.fuente, indicador.codigo, indicador.fecha, indicador.valor, indicador.unidad, indicador.verificado_en))
        
        conexion.commit()
        conexion.close()
        return True

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "SELECT fecha, valor, verificado_en, fuente FROM indicador_api ORDER BY fecha DESC"
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()

        historial = []
        for fila in filas:
            historial.append(Indicador(fecha=fila[0], valor=fila[1], verificado_en=fila[2], fuente=fila[3]))
        return historial


SQL_GUARDAR = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en
"""