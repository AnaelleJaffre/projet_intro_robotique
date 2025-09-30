import numpy as np

## geometric parameters
Rwheels = 10; #to be defined
Drob = 10; #to be defined

## position rob
XYTHETHA = [0,0,0] # movements along the Y axis 


def consigneAbsolute(Xc,Yc,Tc): #move at the coordinates from the Origin
    #compute vector for the base 
    Xc -= XYTHETHA[0]
    Yc -= XYTHETHA[1]
    Tc -= XYTHETHA[2]
    return(Xc,Yc,Tc)

def goTo(Xc,Yc,Tc):
    Lgoto = np.sqrt(Xc*Xc+Yc*Yc)
    Tgoto = np.arctan(Yc/Xc)

    turn(Tgoto)
    move(Lgoto)
    turn(Tc-Tgoto)

def turn(Angle):
    consigne_motor = Drob/Rwheels * Angle
    motorLeft_turn(-consigne_motor)
    motorRight_turn(consigne_motor)

def move(Lenght):
    consigne_motor = 2/Rwheels * Lenght
    motorLeft_turn(consigne_motor)
    motorRight_turn(consigne_motor)

