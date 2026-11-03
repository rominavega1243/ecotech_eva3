# src/servicios/deserializador_indicador.py
from dominio.indicador import Indicador
from servicios.deserializador_indicador import extraer_primero


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
       
        fecha, valor = extraer_primero(datos)
        
        return Indicador(fecha=fecha, valor=valor)
    

