
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('./data/tgrid2/xd.csv', sep='\t')
data2 = pd.read_csv('./data/tgrid2/xd2.csv', sep='\t')
print(data)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

#ax.scatter(data['x'], data['y'], data['z'], color='blue')
ax.scatter(data2['x'], data2['y'], data2['z'], color='red')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

