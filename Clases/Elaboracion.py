class Elaboracion:
    def __init__(self, paso, conjunto):
        self.paso = paso
        self.conjunto = conjunto
        self.linea, self.componente = self.separar_paso(conjunto)

    @staticmethod
    def separar_paso(paso_str):
        linea, componente = paso_str[1:].split('C')
        return int(linea) - 1, int(componente) - 1