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
        
        self.motor_diant_esq = self.robot.getDevice("motor_roda_diant_esq")
        self.motor_tras_esq = self.robot.getDevice("motor_roda_tras_esq")
        self.motor_diant_dir = self.robot.getDevice("motor_roda_diant_dir")
        self.motor_tras_dir = self.robot.getDevice("motor_roda_tras_dir")
        
        self.motor_diant_esq.setPosition(float('inf'))
        self.motor_tras_esq.setPosition(float('inf'))
        self.motor_diant_dir.setPosition(float('inf')) 
        self.motor_tras_dir.setPosition(float('inf'))       
        
        self.motor_diant_esq.setVelocity(-2.0)
        self.motor_tras_esq.setVelocity(-2.0)
        self.motor_diant_dir.setVelocity(-2.0)
        self.motor_tras_dir.setVelocity(-2.0)      
        
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
            print(f"Left: {l_dist} | Main: {distLine} | Right: {r_dist}")
            
            #if distLine <= 800:
                #if l_dist >= 800:
                    #vira esquerda
                    #self.motor_tras_dir.setVelocity(-2.0)
                    #self.motor_tras_esq.setVelocity(0)      
                #else: 
                    #vira direita
                    # self.motor_tras_esq.setVelocity(-2.0) 
                     #self.motor_tras_dir.setVelocity(0)            
             
    

robot = Robot()

robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))

robot_controler.run()                

