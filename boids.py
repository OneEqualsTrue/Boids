from random import *
from tkinter import *

X 		= 800 # Window horizontal
Y 		= 600 # Window diagonal
SIZE 	= 5 # Radius of boid draw
SPEED 	= 40 # Smaller is faster
N 		= 25 # Number of boids

class Boid:
	def __init__(self, name):
		self.position = [randint(0,X-1), randint(0,Y-1)]
		self.velocity = [0, 0]
		boids.append(self)

	def draw(self):

		# Simulate walls
		if self.position[0] <= 120: self.velocity[0] += 3
		if self.position[1] <= 80: self.velocity[1] += 3
		if self.position[0] > X-80: self.velocity[0] -= 3
		if self.position[1] > Y-130: self.velocity[1] -= 3

		graph.create_oval((
			self.position[0]-SIZE,
			self.position[1]-SIZE,
			self.position[0]+SIZE,
			self.position[1]+SIZE), fill='red')

''' 
Cohesion: Boids tend to fly towards the center of mass of neighboring boids
'''
def rule1(bj):
	pcj = [0,0]

	for b in boids:
		if b != bj:
			pcj[0] = pcj[0] + b.position[0]
			pcj[1] = pcj[1] + b.position[1]

	pcj[0] = ((pcj[0] / (N-1)) - bj.position[0]) / 100
	pcj[1] = ((pcj[1] / (N-1)) - bj.position[1]) / 100

	return pcj

''' 
Separation: Boids tend to keep a small distance away from other objects and boids
'''
def rule2(bj):
	c = [0,0]

	for b in boids:
		if b != bj:
			temp = [(b.position[0]-bj.position[0]), (b.position[1]-bj.position[1])]
			if (temp[0]**2 + temp[1]**2)**0.5 <= 70:
				c[0] = c[0] - temp[0] / 60
				c[1] = c[1] - temp[1] / 60
	return c

'''
Alignment:Boids tend to match velocity with nearby boids.
'''
def rule3(bj):
	pvj = [0,0]

	for b in boids:
		if b != bj:
			pvj[0] += b.velocity[0]
			pvj[1] += b.velocity[1]

	pvj[0] = ((pvj[0] / (N-1)) - bj.velocity[0]) / 25
	pvj[1] = ((pvj[1] / (N-1)) - bj.velocity[1]) / 25

	return pvj

def update():
	graph.delete(ALL)

	for b in boids:
		v1 = rule1(b)
		v2 = rule2(b)
		v3 = rule3(b)

		b.velocity[0] = b.velocity[0] + v3[0] + v2[0] + v1[0]
		b.velocity[1] = b.velocity[1] + v3[1] + v2[1] + v1[1]

		# Limit velocity
		if b.velocity[0] >= 10: b.velocity[0] = 8
		if b.velocity[1] >= 10: b.velocity[1] = 8

		b.position[0] = b.position[0] + b.velocity[0]
		b.position[1] = b.position[1] + b.velocity[1]

		b.draw()

	graph.after(SPEED, update)

def main():
	global graph
	global boids
	boids = []

	root = Tk()
	root.geometry('%dx%d+%d+%d' % (X, Y, (root.winfo_screenwidth()-X)/2, (root.winfo_screenheight()-Y)/2))
	root.bind_all('<Escape>', lambda event: event.widget.quit())

	graph = Canvas(root, width=X, height=Y, background='#ecede8')
	Label(root, text="Press ESC to exit").pack()
	
	for i in range(N): Boid(i)

	graph.after(SPEED, update)
	graph.pack()

	mainloop()

main()