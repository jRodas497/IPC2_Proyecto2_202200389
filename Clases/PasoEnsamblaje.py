class PasoEnsamblaje:
    def __init__(self, paso_str, linea, componente):
        self.paso_str = paso_str
        self.linea = linea
        self.componente = componente

    @staticmethod
    def separar_paso(paso_str):
        linea, componente = paso_str[1:].split('C')
        return int(linea) - 1, int(componente) - 1  # Ajustar índices a 0-based