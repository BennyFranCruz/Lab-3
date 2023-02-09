class PorportionalController:   
    
    def __init__(self, Kp, initial_setpoint):
        
        self.Kp = Kp
        self.setpoint = initial_setpoint
        
    def run(self, setpoint, position):
        
        self.p_control_out = -self.Kp*(setpoint - position)
        
        if self.p_control_out > 100:
            self.p_control_out = 100
        elif self.p_control_out <-100:
            self.p_control_out = -100
        
        return(self.p_control_out)
    
