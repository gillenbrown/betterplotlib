import prettyplot as ppl
import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(0, 1, size=10000)
ppl.hist(data)