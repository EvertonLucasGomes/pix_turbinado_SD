class LockerMult:
    def __init__(self, size):
        self.last_to_enter = [-1] * size
        self.level         = [-1] * size
        self.N             = size
  
    def acquire(self, PID):    
        for i in range(0, self.N):
            #print("locking ", PID, i, self.last_to_enter[i], max(self.level[:PID]+self.level[PID+1:]))
            self.level[PID] = i
            self.last_to_enter[i] = PID
            while self.last_to_enter[i] == PID \
                and max(self.level[:PID]+self.level[PID+1:]) >= i:
                continue
        #print("locker out", PID)
    
    def release(self, PID):
        self.level[PID] = -1 
    
    def get_queue(self):
        return self.level