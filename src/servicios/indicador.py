import requests

from servicios.permisos import exigir_sesion
from servicios.deserializador_indicador import deserializador_indicador
from persistencia.indicador_dao import IndicadorDAO



def obtener_datos():
    url = "https://mindicador.cl/api/dolar"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    respuesta = requests.get(url, headers=headers, timeout=30, verify=False)
    respuesta.raise_for_status()
    return respuesta.json()


def buscar_respaldo():
    fila = IndicadorDAO.buscar_ultimo("mindicador", "dolar")
    if fila:
        return {
            "fuente": fila[0],
            "codigo": fila[1],
            "fecha": fila[2],
            "valor": fila[3],
            "unidad": fila[4],
            "verificado_en": fila[5]
        }
    return {
        "fuente": "mindicador",
        "codigo": "dolar",
        "fecha": "2026-10-29",
        "valor": 981.08,
        "unidad": "CLP"
    }    


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        datos = obtener_datos()
        dato = deserializador_indicador.desde_api(datos)

        IndicadorDAO.guardar(
            getattr(dato, "fuente", "mindicador"),
            getattr(dato, "codigo", "dolar"),
            getattr(dato, "fecha", ""),
            getattr(dato, "valor", 0.0),
            getattr(dato, "unidad", "CLP"),
            getattr(dato, "verificado_en", None)
        )

        return  dato
    except (requests.exceptions.RequestException,
            ValueError, KeyError, TypeError):
        return buscar_respaldo()

def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()
