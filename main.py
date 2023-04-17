

class PID:

    def __int__(self,KP,KI,KD,In,Out,Min,Max,DT):
        self.KP = KP
        self.KI = KI
        self.KD = KD
        self.In = In
        self.Out = Out
        self.Min = Min
        self.Max = Max
        self.DT = DT

    def compute(self):
        pass
