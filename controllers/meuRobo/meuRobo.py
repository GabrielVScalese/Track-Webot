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
        
        self.motor_diant_esq = self.robot.getDevice("motor_diant_esq")
        self.motor_tras_esq = self.robot.getDevice("motor_tras_esq")
        self.motor_diant_dir = self.robot.getDevice("motor_diant_dir")
        self.motor_tras_dir = self.robot.getDevice("motor_tras_dir")
        
        self.motor_diant_esq.setPosition(float('inf'))
        self.motor_tras_esq.setPosition(float('inf'))
        self.motor_diant_dir.setPosition(float('inf')) 
        self.motor_tras_dir.setPosition(float('inf'))       
        
        self.motor_diant_esq.setVelocity(1.0)
        self.motor_tras_esq.setVelocity(1.0)
        self.motor_diant_dir.setVelocity(1.0)
        self.motor_tras_dir.setVelocity(1.0)      
       
        self.leftSensor = self.robot.getDevice("left_sensor")
        self.leftSensor.enable(timestep)
        
        self.rightSensor = self.robot.getDevice("right_sensor")
        self.rightSensor.enable(timestep)
        
        self.mainSensor = self.robot.getDevice("main_sensor")
        self.mainSensor.enable(timestep)
         
        self.objSensor = self.robot.getDevice("obj_sensor")
        self.objSensor.enable(timestep)
        
        self.camera = self.robot.getDevice("camera")
        self.camera.enable(timestep)

class TI502(MeuRobot):
    
    def setMotors (self, leftMotor, rightMotor):
        self.motor_diant_esq.setVelocity(leftMotor)
        self.motor_tras_esq.setVelocity(leftMotor)
        self.motor_diant_dir.setVelocity(rightMotor)
        self.motor_tras_dir.setVelocity(rightMotor)
    
    def run(self):
        sentido = 0
        
        while self.robot.step(timestep) != -1:
            self.camera.saveImage("image.png", 720)
            
            # Line sensors
            rightDistance = self.rightSensor.getValue()
            leftDistance = self.leftSensor.getValue()
            mainDistance = self.mainSensor.getValue()
           
            # Object sensors
            #print(f"Left: {lObj} | Right: {rObj}")
            
            if mainDistance == 0:
                self.setMotors(1, 1)
            else:
                if rightDistance != 0: # go to left
                    self.setMotors(-1, 1)
           
                elif leftDistance != 0: # go to right
                    self.setMotors(1, -1)
                    
                          
robot = Robot()

robot_controler = TI502(robot)

_thread.start_new_thread(servidor, (get_ip(),get_port()))

robot_controler.run()                

