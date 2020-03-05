import simpy
import random

RANDOM_SEED = 10 #Secuencia determinada de generador de numeros random
MEMORIA = [1,10]
PROCESOSS = [1,10]
INTERVALO = 10 #intervalo ya definido para la velocidad en la que se generan procesos
PROCESOS = 200 #Procesos que se van a crear
INST_UNIDAD_TIEMPO = 3
TT = 0


def generador(env, procesos, intervalo, RAM, CPU, cola, instrucciones, memoria):
    #Generador genera los procesos a usar jajaja
    for i in range(procesos):
        p = proceso(env, 'Proceso %02d' % i, RAM, CPU, cola, instrucciones, memoria)
        env.process(p)
        t = random.expovariate(1.0/intervalo)
        yield env.timeout(t)

def proceso(env, name, RAM, CPU, cola, instrucciones, memoria):
    """Un proceso llega a nuestro sistema para poder ser ejecutado"""
    tiempoInicial=env.now
    print('%s arriving at system at %f with the need of %a memory' % (name, env.now, memoria))
    if (memoria<RAM.level):
       #Se va a ejecutar
        numero=2
        yield RAM.get(memoria)
        if numero==1:
            I_O = waiting(env, name, cola)
            env.process(I_O)
        else:
            while instrucciones>3 :
                with CPU.request() as req:
                    yield req
                    yield env.timeout(1)
                    instrucciones = instrucciones - INST_UNIDAD_TIEMPO
                    numero = random.randint(1,2)
                    print(name + ": realizado una operacion en "+str(env.now)+"\n")
        RAM.put(memoria)
        print(name + ": terminado en "+str(env.now)+"\n")
        tiempoFinal = env.now
        tiempoTotal = tiempoFinal-tiempoInicial
        global TT
        TT= TT + tiempoTotal
        print(TT)
    else:
        print('The %s process needed %f of memory but the resource didnt have enough' % (name, memoria))
    
def waiting(env,name,cpu):
    with cpu.request() as req1:
        yield req1
        p= proceso(env,name, RAM, CPU,cola, instrucciones, memoria)
        env.process(p)

#Configura con la simulacion
print('Simulador de procesos')
random.seed(RANDOM_SEED)
instrucciones = random.randint(*PROCESOSS)
memoria = random.randint(*MEMORIA)
env = simpy.Environment()
#comienza la simulacion
RAM = simpy.Container(env, init=100, capacity=200)
CPU = simpy.Resource(env, capacity=2)
cola = simpy.Resource(env)
env.process(generador(env, PROCESOS, INTERVALO, RAM, CPU, cola, instrucciones, memoria))
env.run()
print('Porcesos hechos: ' + str(PROCESOS))
print('Intervalo : '+str(INTERVALO))
print('Tiempo promedio: ' +str(TT/PROCESOS))
print('Tiempo total: '+ str(TT))