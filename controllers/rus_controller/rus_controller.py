"""rus_controller controller."""

#by slmm for TI502

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, GPS, DifferentialWheels

print("Iniciando")
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64 #int(robot.getBasicTimeStep())

nome = robot.getName()
print("Nome do robo : ", nome)


motor_esq = robot.getDevice("motor roda esquerda")
motor_dir = robot.getDevice("motor roda direita")

motor_esq.setPosition(float('+inf'))
motor_dir.setPosition(float('+inf'))

motor_esq.setVelocity(0.0)
motor_dir.setVelocity(0.0)

# obtem o sensor de distancia
ir0 = robot.getDevice("ir0")
ir0.enable(timestep)

ir1 = robot.getDevice("ir1")
ir1.enable(timestep)

gps = robot.getDevice("gps")
gps.enable(timestep)

ir3 = robot.getDevice("ir3")
ir3.enable(timestep)


#valores = gps2.getValues()
#print("Objeto esta na posicao: %g %g %g" % (values[0], values[1], values[2]))

sentido = 0
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)
last_dist = ir3.getValue()


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    values = gps.getValues()
    
    dist = ir0.getValue()
    dist1 = ir1.getValue()
    
    dist3 = ir3.getValue()
    if (dist3 != last_dist):
       print(dist3)    
       last_dist = dist3
   
    
    # Process sensor data here.
    if (dist >= 500):
        sentido = 1
        
    if (dist1 >= 500):
        sentido = 0
        
    if (sentido == 0):
        motor_esq.setVelocity(2.0)
        motor_dir.setVelocity(2.0)
    else:
        motor_esq.setVelocity(-2.0)
        motor_dir.setVelocity(-2.0)
    


# Enter here exit cleanup code.
