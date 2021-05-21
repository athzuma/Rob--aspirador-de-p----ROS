#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
acelera = 0.15
freia = 0.0
gira_direita = -0.15
gira_esquerda = 0.15
espiral = 0.50
ciclos = 0
#rate = rospy.Rate(1)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
def callback(msg):
	global espiral
	global ciclos
	move = Twist()
	direita = round(msg.ranges[315],2)
	frente = round(msg.ranges[0],2)
	esquerda = round(msg.ranges[45],2)
	print('===================================================================')
	print('Esquerda --> ', esquerda, 'Frente --> ', frente, 'Direita --> ', direita)
	print('===================================================================')
	print('')
	#se esquerda ou direita < 0.6, mas frente > 1, ir em frente reto
	#se esquerda ou direita < 0.6 ou frente < 0.6, desviar
	#se esq e dir > 0.6 e frente > 1, espiral
	
	if ((esquerda < 0.6) or (direita < 0.6)) and (frente > 0.7):
		#modo 2
		move.angular.z = 0.0
		move.linear.x = acelera
	
	elif ((esquerda < 0.6) or (direita < 0.6)) and (frente < 0.7):
		#modo 2
		move.linear.x = freia
		print('============================ DESVIANDO ============================')
		if esquerda >= direita:
			move.angular.z = gira_esquerda
		else:
			move.angular.z = gira_direita
	
	else:
		#modo 1
		move.angular.z = espiral
		move.linear.x = acelera
		ciclos = ciclos + 1
		if (ciclos > 8):
			ciclos = 0
			if (espiral > 0.02):
				espiral = espiral - 0.01
				print('============================ RAIO ALTERADO ============================')
				print('Espiral --> ', espiral)
	
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
