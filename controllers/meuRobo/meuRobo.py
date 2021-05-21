import struct
import socket
import sys
import _thread
import base64

from controller import Robot, GPS

print("Iniciando")

timestep = 64

direction = 0

def get_port():
    return 9001

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))    
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    
    print(IP)
    return IP


def on_new_client(socket, addr):
    global robot_controler
    while True:
        msg = socket.recv(1024)
        if msg:
            break;
        else:
            break;
            
    image_file = open ('./image.png', 'rb')
    msg = 'HTTP/1.1 200 OK\r\n'.encode() + "Content-Type: image/png\r\n".encode() + "Accept-Ranges: bytes\r\n\r\n".encode() + image_file.read()
    
    socket.send(msg)
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

        self.motor_esq.setVelocity(2.0)
        self.motor_dir.setVelocity(2.0)
        
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(timestep)

        self.mainSensor = self.robot.getDevice("main_sensor")
        self.mainSensor.enable(timestep)
        
        self.leftSensor = self.robot.getDevice("left_sensor")
        self.leftSensor.enable(timestep)
        
        self.rightSensor = self.robot.getDevice("right_sensor")
        self.rightSensor.enable(timestep)
        
        self.cv = self.robot.getDevice("camera")
        self.cv.enable(timestep)
        
        img = self.cv.getImage()
       
        self.parado = False
       
    def run(self):
        raise NotImplementedError
        

class TI502(MeuRobot):
    def run(self):
        sentido = 0
        
        while self.robot.step(timestep) != -1:
            self.cv.saveImage("image.png", 720)
            l_dist = self.leftSensor.getValue()
            r_dist = self.rightSensor.getValue()
            distLine = self.mainSensor.getValue()
            
            if distLine == 0:
                #print("Linha")
                sentido = 0
                self.motor_dir.setVelocity(2.0)
                self.motor_esq.setVelocity(2.0)
            else:
                #print("fora")
                #print(f"Left: {l_dist} | Right: {r_dist}")
                if sentido == 1:
                    self.motor_dir.setVelocity(0.0)
                    self.motor_esq.setVelocity(2.0)
                elif sentido == 2:
                    self.motor_dir.setVelocity(2.0)
                    self.motor_esq.setVelocity(0.0)
            
                if r_dist > l_dist:
                    sentido = 1 # go to left
                elif r_dist < l_dist:
                    sentido = 2 # go to right
                else:
                    sentido = 1
             
    def  pararRobo(self, estado):
        self.parado = estado    


robot = Robot()

robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))

robot_controler.run()                

