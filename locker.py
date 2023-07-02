from time import monotonic_ns
from threading import Thread



class LockerMult:
    def __init__(self, tamanho):
        self.ultimo_a_entrar = [-1] * tamanho
        self.nivel = [-1] * tamanho
        self.N = tamanho
  
    def adquirir(self, PID):
        for i in range(0, self.N):
            #print("trancando ", PID, i, self.ultimo_a_entrar[i], max(self.nivel[:PID]+self.nivel[PID+1:]))
            self.nivel[PID] = i
            self.ultimo_a_entrar[i] = PID
            while self.ultimo_a_entrar[i] == PID and max(self.nivel[:PID] + self.nivel[PID+1:]) >= i:
                continue
        #print("liberando trinco", PID)
    
    def liberar(self, PID):
        self.nivel[PID] = -1 
    
    def obter_fila(self):
        return self.nivel

class LockerMultComTimeout:
    def __init__(self, tamanho):
        self._ultimo_a_entrar = [-1] * tamanho
        self._nivel = [-1] * tamanho
        self._N = tamanho
        self.threads_timeout = [None] * tamanho
        self.parar_threads = [False] * tamanho
        self.timeout_grant_in_nsecs = 7000000000
  
    def trancar(self, PID):
        for i in range(0, self._N):
            self._nivel[PID] = i
            self._ultimo_a_entrar[i] = PID
            while self._ultimo_a_entrar[i] == PID and max(self._nivel[:PID] + self._nivel[PID+1:]) >= i:
                continue

        self.parar_threads[PID] = False
        self.threads_timeout[PID] = Thread(target=self._verificar_timeout, args=(PID, lambda: self.parar_threads[PID]))
        self.threads_timeout[PID].start()

    def _verificar_timeout(self, PID, parar):
        tempo_inicial = monotonic_ns()
        while (monotonic_ns() - tempo_inicial) < self.timeout_concedido_em_nsecs and not parar():
            continue

        if not parar():
            print("Thread de timeout executada", PID)
            #self.liberar(PID)
            self._nivel[PID] = -1
    
    def liberar(self, PID):        
        self.parar_threads[PID] = True
        self._nivel[PID] = -1