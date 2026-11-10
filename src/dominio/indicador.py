
class Indicador:
    def __init__(self, fecha: str, valor: float, verificado_en: str = None, fuente: str = "mindicador.cl"):
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en
