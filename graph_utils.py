# author: Justin Feng
import random
import numpy as np
import matplotlib.pyplot as plt

def graph_daily(list):
    list = np.array(list)

    plt.plot(list)
    plt.show()
    
    return


if __name__ == "__main__":
    ls = [random.randint(1,100) for i in range(100)]
    graph_daily(ls)