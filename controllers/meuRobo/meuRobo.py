# MeuRobo.py by SLMM for TI502
#
#
import struct
import socket
import sys
import _thread

from controller import Robot, GPS

print("Iniciando")

timestep = 64

def get_port():
    return 9001

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))    
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    return IP


def on_new_client(socket, addr):
    global robot_controler
    while True:
        msg = socket.recv(1024)
        if msg:
            print('chegou')
            break;
        else:
            break;
    msg1 = msg.decode()
    
    if msg1.__contains__('anda'):
       robot_controler.pararRobo(False)
    else:       
       robot_controler.pararRobo(True)
    print(msg1)

    socket.close()
    return        

def servidor(https, hport):
    sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockHttp.bind((https, hport))
    except:
        sockHttp.bind(('', hport))
        
    sockHttp.listen(1)
    
    while True:
        client, addr = sockHttp.accept()
        _thread.start_new_thread(on_new_client, (client,addr))



class MeuRobot:
    def __init__(self, robot):
        
        self.robot = robot
        self.nome  = robot.getName()
        print("Nome do robo : ", self.nome)
        self.motor_esq = self.robot.getDevice("motor roda esquerda")
        self.motor_dir = self.robot.getDevice("motor roda direita")

        self.motor_esq.setPosition(float('+inf'))
        self.motor_dir.setPosition(float('+inf'))

        self.motor_esq.setVelocity(0.0)
        self.motor_dir.setVelocity(0.0)

        # obtem o sensor de distancia
        self.ir0 = self.robot.getDevice("ir0")
        self.ir0.enable(timestep)

        self.ir1 = self.robot.getDevice("ir1")
        self.ir1.enable(timestep)

        self.gps = self.robot.getDevice("gps")
        self.gps.enable(timestep)

        self.ir3 = self.robot.getDevice("ir3")
        self.ir3.enable(timestep)
# seguindo a logica .
# obter o device
# iniciar o device e assim aplicar ou receber comandos

        self.cv = self.robot.getDevice("camera")
        self.cv.enable(timestep)
        
        img = self.cv.getImage()
        print(img)
            
        self.parado = False
       
    def run(self):
        raise NotImplementedError
        

class TI502(MeuRobot):
    def run(self):
        sentido = 0
        
        img = self.cv.getImage()
        
        last_dist = self.ir3.getValue()
        while self.robot.step(timestep) != -1:
            values = self.gps.getValues()
            
            dist = self.ir0.getValue()
            dist1 = self.ir1.getValue()
    
            dist3 = self.ir3.getValue()
            if (dist3 != last_dist):
               print(dist3,"sentido", sentido)    
               last_dist = dist3
       
            # Process sensor data here.
            if (dist >= 500):
                sentido = 1
        
            if (dist1 >= 500):
                sentido = 0
        
            if (sentido == 0):
                self.motor_esq.setVelocity(2.0)
                self.motor_dir.setVelocity(2.0)
            else:
                self.motor_esq.setVelocity(-2.0)
                self.motor_dir.setVelocity(-2.0)        
                
            if (self.parado):
                self.motor_esq.setVelocity(0.0)
                self.motor_dir.setVelocity(0.0)        
                

    def  pararRobo(self, estado):
        self.parado = estado    


#programa principal



robot = Robot()

robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))

robot_controler.run()                

