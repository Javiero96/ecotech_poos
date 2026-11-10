from dominio.indicador import Indicador

class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos: dict) -> Indicador:
        serie = datos.get("serie", [])
        if not serie:
            raise ValueError("El JSON no contiene la serie de datos esperada.")
        
        ultimo_dato = serie[0]
        # Extraemos solo la parte YYYY-MM-DD de la fecha
        fecha = str(ultimo_dato.get("fecha"))[:10] 
        valor = float(ultimo_dato.get("valor"))
        
        return Indicador(fecha=fecha, valor=valor)