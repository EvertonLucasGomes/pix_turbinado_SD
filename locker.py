class LockerMult:
    def __init__(self, tamanho):
        self.ultimo_a_entrar = [-1] * tamanho
        self.nivel = [-1] * tamanho
        self.N = tamanho
  
    def adquirir(self, PID):
        for i in range(0, self.N):
            self.nivel[PID] = i
            self.ultimo_a_entrar[i] = PID
            while self.ultimo_a_entrar[i] == PID and max(self.nivel[:PID] + self.nivel[PID+1:]) >= i:
                continue
    
    def liberar(self, PID):
        self.nivel[PID] = -1 
    
    def obter_fila(self):
        return self.nivel