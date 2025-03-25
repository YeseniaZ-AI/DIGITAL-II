# main.py -- put your code here!
from time import sleep
from machine import Pin 
from machine import mem32
from machine import ADC


#semaforo colegio mayor 
Rojopeatonal=Pin(15,Pin.OUT)
verdepeatonal=Pin(2,Pin.OUT)
Rojovehicular=Pin(4,Pin.OUT)
Amrillovehicular=Pin(16,Pin.OUT)
verdevehicular=Pin(17,Pin.OUT)

#Semafor para robledo vertical, es decir curva 
RojovehicularV=Pin(5,Pin.OUT)
AmrillovehicularV=Pin(18,Pin.OUT)
verdevehicularV=Pin(19,Pin.OUT)

#semaforo calle del D1 ir al centro y a sopetran 
Rojopeatonal=Pin(13,Pin.OUT)
verdepeatonal=Pin(12,Pin.OUT)
Rojovehicular=Pin(14,Pin.OUT)
Amrillovehicular=Pin(27,Pin.OUT)
verdevehicular=Pin(26,Pin.OUT)

#semaforo de la curva para el itm 
Rojovehicularitm=Pin(22,Pin.OUT)
Amrillovehicularitm=Pin(23,Pin.OUT)
verdevehicularitm=Pin(21,Pin.OUT)


global variable
variable=0

def interrupcion(Pin):
    global variable
    print("Entre a la funcion interrupcion")
    variable=1
pulsador=Pin(35,Pin.IN)
pulsador.irq(trigger=Pin.IRQ_FALLING,handler=interrupcion)


#Definir pin del sensor MCP9700
sensor_tempe = ADC(Pin(25)) #se debe conectar al pin analogico de la ESP32 
sensor_tempe.atten(ADC.ATT-N_11DB) # 0-3.6V, 11dB attenuation (150mV-2450mV), evitar que la esp se queme 

factor_conversion = 3.3 / 4095 * 100 #conversion de lectura a grados celsius 

global variable, evalua_temperatura 
variable=0
evalua_temperatura = False # Variable para activar la medicion de temperatura 

def interrupcion(Pin):
    print("Entre a la fuincion Emergencia")
    variable=1 
def temperatura(Pin):
    global evalua_temperatura
    if evalua_temperatura: # si ya esta en modo temperatura, volver al semaforo 
        evalua_temperatura = False
       print("saliendo de modo temperatura,volviendo al semaforo")
       else:
        evalua_temperatura= True
        print("Modo temperatura activado.")

pulsador_MCP9700=Pin(34,Pin.IN)
pulsador_MCP9700.irq(trigger=Pin.IR-Q_RISING,handler=temperatura)

GPIO_SET=const(0x3FF44004)



while True:
 
 if evalua_temperatura:
    lectura = sensor_tempe.read()
    temperatura = lectura * factor_conversion # Convertir a  °c
    pint("Temperatura:",temperatura,"°c")
    sleep(1)
         
    mem32[GPIO_SET]=0B0000000000000010010101100000000000000
    sleep(6)
    mem32[GPIO_SET]=0B0000000000000010010101110000000000000 #Titular verde vehicular CM
    sleep(3)
    mem32[GPIO_SET]=0B0000000000000010000001110000000000000 #titilar verde CM (verde 0ff)
    sleep(2)
    mem32[GPIO_SET]=0B0000000000000010010101110000000000000 #Titular verde vehicular CM (verde oN)
    sleep(2)
    mem32[GPIO_SET]=0B0000000000000100011011110000000000000 #titilar amarillo
    sleep(2)
    mem32[GPIO_SET]=0B0000000000000100010001110000000000000 #TITILAR AMARILLO OFF
    sleep(1)
    mem32[GPIO_SET]=0B0000000000000100011011110000000000000 #titilar amarillo ON
    sleep(2)
    mem32[GPIO_SET]=0B0000000000000010000000101000000110100 #PEATON
    sleep(5)
    mem32[GPIO_SET]=0B0000000000100001010001010000000000000 # verde on para curva ITM, d1, y curva exito
if variable==1:
    mem32[GPIO_SET]=0b0000000000000010000000101000000110100 #activar pulsador
    sleep(10)
    variable=0