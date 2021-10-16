from scipy.integrate import odeint
import numpy as np
class ODE_system:
    def __init__(self, N, I0, R0, beta, gamma, block_size = 10, epsilon = 0.1, max_iter = 50): 
        print("Constructor")
        #Initialize values
        self.N = N
        self.beta = beta
        self.gamma = gamma
        self.S0 = N - I0 - R0
        self.I0 = I0
        self.R0 = R0
        self.block_size = block_size
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.t0 = 0
        #Initialize dependient variables
        self.S = np.array([])
        self.I = np.array([])
        self.R = np.array([])
        self.t = np.array([])

    def __sir(self, y, t, N, beta, gamma):
        #SIR model (will change when Ingo Dreyer send the information)
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt #Returns differentials

    def solve(self):
        #Solve system
        t0 = self.t0
        i = 0
        while(i < self.max_iter):#Bucle, will break when standar desviation will be less than epsilon.
            self.y0 = self.N - self.I0 - self.R0, self.I0, self.R0 #Dependient variables
            t = np.linspace(t0, t0 + self.block_size, num = 50) #Temporal values
            #Solve ODE system
            system = odeint(self.__sir, self.y0, t, args=(self.N, self.beta, self.gamma))
            #Asign dependient variables to vector self.y0
            self.y0 = self.S0, self.I0, self.R0 
            #Adds block solutions to global solution vectors
            self.S = np.concatenate((self.S, system.T[0]), axis = 0)
            self.I = np.concatenate((self.I, system.T[1]), axis = 0)
            self.R = np.concatenate((self.R, system.T[2]), axis = 0)
            self.t = np.concatenate((self.t, t), axis = 0)
            #Set S0, I0 and R0 for the next iteration
            self.S0 = self.S[-1]
            self.I0 = self.I[-1]
            self.R0 = self.R[-1]
            #When standart desviation is less than epsilon for all 
            # dependient variables, stop calculus
            if((np.std(system.T[0]) < self.epsilon and 
                np.std(system.T[1]) < self.epsilon and 
                np.std(system.T[2]) < self.epsilon) or system.T[0][-1] < 0):
                break
            #Iteration variables
            i+=1
            t0 = i*self.block_size
        if(i < self.max_iter):
            print("\nAfter {iter} iterations, solution converges for epsilon = {epsilon}".format(iter = i, epsilon = self.epsilon))
            print("S:", self.S[-1])
            print("I:", self.I[-1])
            print("R:", self.R[-1])
            print("t:", self.t[-1])
        else:
            print("\nAfter {iter} iterations, solution don't converge for epsilon = {epsilon}".format(iter = i, epsilon = self.epsilon))
    def get_results(self):
        return({"t": list(self.t), "S": list(self.S), "I": list(self.I), "R": list(self.R)})