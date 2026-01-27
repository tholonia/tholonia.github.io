import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random
import math
center = (0.0, 0.0)
radius = 1
points = 9
circle = Circle(center, radius,color='k', fill=False)

fig, ax = plt.subplots()
ax.add_patch(circle)
ax.set_aspect('equal')

plt.ylim(-1.2, 1.2)
plt.xlim(-1.2,1.2)

x=[]
y=[]
for i in range(0,points):
    ang = math.radians(360)/points
    angle = ang*i
    print(angle)
    x.append(math.cos(angle));
    y.append(math.sin(angle));

for i in range(0,points):
  for j in range(0, points):
    xv = [x[i],x[j]]
    yv = [y[i],y[j]]
    plt.plot(xv,yv,'ko',linestyle="solid")

plt.scatter(x,y)

plt.axis('off')
# plt.grid(b=None)
# plt.show()
plt.savefig(f'foo_{points}.png')
plt.close()
