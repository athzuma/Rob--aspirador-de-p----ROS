#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
acelera = 0.15
freia = 0.0
gira_direita = -0.15
gira_esquerda = 0.15
espiral = 0.50 #Essa variavel armazena a velocidade inicial de giro, que é decrementada com o passar do tempo
ciclos = 0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
def callback(msg):
	global espiral #Traz as variaveis espiral e ciclos para o contexto da funcao
	global ciclos
	move = Twist()
	direita = round(msg.ranges[315],2)
	frente = round(msg.ranges[0],2)
	esquerda = round(msg.ranges[45],2)
	
	
	if ((esquerda < 0.6) or (direita < 0.6)) and (frente > 0.7):
		#modo 2
		#primeiro caso do modo 2, o robo deve segir em frente limpando a lateral da parede
		move.angular.z = 0.0
		move.linear.x = acelera
	
	elif ((esquerda < 0.6) or (direita < 0.6)) and (frente < 0.7):
		#modo 2
		#Segundo caso do modo 2, o robo deve desviar para não bater na parede
		move.linear.x = freia
		if esquerda >= direita:
			move.angular.z = gira_esquerda
		else:
			move.angular.z = gira_direita
	
	else:
		#modo 1
		#no modo 1, o robo anda em espiral
		move.angular.z = espiral #Determina a velocidade da rotacao
		move.linear.x = acelera
		ciclos = ciclos + 1
		if (ciclos > 8): #A variavel ciclos determina a velocidade que o raio do espiral aumenta, quanto maior o valor, mais "profunda" e a limpeza
			ciclos = 0
			if (espiral > 0.02):
				espiral = espiral - 0.01 #Diminui a velocidade de gira, aumentando o raio do espiral
	
	pub.publish(move)
def main():
	rospy.init_node('drive')
	try:
		rospy.Subscriber('/scan', LaserScan, callback)
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
if __name__ == '__main__':
	main()