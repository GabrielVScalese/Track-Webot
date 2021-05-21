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

        self.cv = self.robot.getDevice("camera")
        self.cv.enable(timestep)
        
        img = self.cv.getImage()
            
        self.parado = False
       
    def run(self):
        raise NotImplementedError
        

class TI502(MeuRobot):
    def run(self):
        sentido = 0
        
        #img = self.cv.getImage()
        print("a")
        while self.robot.step(timestep) != -1:
           self.motor_esq.setVelocity(2.0)
           self.motor_dir.setVelocity(2.0)        
                
                
#programa principal



robot = Robot()

robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))

robot_controler.run()                

