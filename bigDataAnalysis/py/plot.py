import numpy as np
import matplotlib.pyplot as plt

def draw_line_chart(x,y):
    plt.plot(x,y)
    plt.ylabel('Sunlight')
    plt.xlabel('Time')
    plt.show()

draw_line_chart([x for x in range(10)],[y for y in range(10)])
