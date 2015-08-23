import prettyplot as ppl
import matplotlib.pyplot as plt
import numpy as np

x1 = np.random.normal(0, scale=0.5, size=500)
y1 = np.random.normal(0, scale=0.5, size=500)
x2 = np.random.normal(0.5, scale=0.5, size=500)
y2 = np.random.normal(0.5, scale=0.5, size=500)
x3 = np.random.normal(1, scale=0.5, size=500)
y3 = np.random.normal(1, scale=0.5, size=500)

ppl.scatter(x1, y1)
ppl.scatter(x2, y2)
ppl.scatter(x3, y3)