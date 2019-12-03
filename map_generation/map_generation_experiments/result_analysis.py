from mpl_toolkits import mplot3d
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ga_experiment_at_1575354237.csv")

print(df.info())

print(df.columns)

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(df["map_size"], df["population_size"], df["experiment_duration"],
c=df["experiment_duration"], cmap="Greens")
ax.set_xlabel('Map Size')
ax.set_ylabel('Population')
ax.set_zlabel('Duration')
plt.show()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(df["mutation_rate"], df["population_size"], df["best_fitness"],
c=df["best_fitness"], cmap="Greens")
ax.set_xlabel('Mutation Rate')
ax.set_ylabel('Population')
ax.set_zlabel('Best Fitness')
plt.show()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(df["map_size"], df["population_size"], df["best_fitness"],
c=df["best_fitness"], cmap="Greens")
ax.set_xlabel('Map Size')
ax.set_ylabel('Population')
ax.set_zlabel('Best Fitness')
plt.show()

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(df["mutation_rate"], df["map_size"], df["best_fitness"],
c=df["best_fitness"], cmap="Greens")
ax.set_xlabel('Mutation Rate')
ax.set_ylabel('Map Size')
ax.set_zlabel('Best Fitness')
plt.show()