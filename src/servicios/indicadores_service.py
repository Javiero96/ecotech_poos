import requests
from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicador_dao import IndicadorDAO

def consultar_indicador():
    url = "https://mindicador.cl/api/dolar"
    try:
        # 1. Intentar consultar la API
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        # 2. Deserializar
        indicador = DeserializadorIndicador.desde_api(datos)
        
        # 3. Guardar en Base de Datos
        IndicadorDAO.guardar(indicador)
        
        return {"origen": "API", "dato": indicador, "mensaje": "Guardado exitosamente en BD local."}
        
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        # 4. Si la API falla, buscar respaldo en la BD local
        historial = IndicadorDAO.listar()
        if historial:
            respaldo = historial[0] # Tomamos el más reciente
            return {"origen": "BD local", "dato": respaldo, "mensaje": "La API falló. Mostrando último respaldo."}
        else:
            return {"origen": "Error", "dato": None, "mensaje": "API caída y no hay historial guardado."}

def obtener_historial():
    return IndicadorDAO.listar()