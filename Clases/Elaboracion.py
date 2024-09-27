class Elaboracion:
    def __init__(self, linea=None, componente=None, conjunto=None):
        self.linea = linea
        self.componente = componente
        self.conjunto = conjunto
        if conjunto:
            self.linea, self.componente = self.separar_paso(conjunto)

    @staticmethod
    def separar_paso(paso_str):
        linea, componente = paso_str[1:].split('C')
        return int(linea), int(componente)