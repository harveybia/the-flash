import cv2
import time
import Tkinter as tk
import numpy as np
import threading
from matplotlib import pyplot as plt

def profile(fn):
    # A decorator function to determine the run time of functions
    def with_profiling(*args, **kwargs):
        start_time = time.time()
        ret = fn(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print "Time elapsed for function: %s:"%(fn.__name__)
        print "%.3f"%(elapsed_time)
        return ret
    return with_profiling

img = cv2.imread('../tests/1.JPG',0)
WIDTH, HEIGHT = img.shape
img = cv2.resize(img, dsize=(WIDTH//16, HEIGHT//16))
blurred = cv2.medianBlur(img, 5)
#blurred = cv2.GaussianBlur(img, (5,5), 0)
edges = cv2.Canny(blurred,0,500)

@profile
def updatePlot(scale1, scale2, scale3):
    plt.clf()

    plt.subplot(131),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    blurred = cv2.medianBlur(img, scale3.get()//2*2+1)
    #blurred = cv2.GaussianBlur(img, (5,5), 0)
    #blurred = img
    plt.subplot(132),plt.imshow(blurred,cmap = 'gray')
    plt.title('Blurred Image'), plt.xticks([]), plt.yticks([])

    edges = cv2.Canny(blurred,scale1.get(),scale2.get())
    plt.subplot(133),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    fig.canvas.draw()

root = tk.Tk()
root.geometry("500x250+10+10")
scale1 = tk.Scale(root, orient=tk.HORIZONTAL, from_=0, to=500)
scale2 = tk.Scale(root, orient=tk.HORIZONTAL, from_=0, to=500)
scale3 = tk.Scale(root, orient=tk.HORIZONTAL, from_=0, to=50)
scale1.bind("<ButtonRelease-1>", lambda x: updatePlot(scale1, scale2, scale3))
scale2.bind("<ButtonRelease-1>", lambda x: updatePlot(scale1, scale2, scale3))
scale3.bind("<ButtonRelease-1>", lambda x: updatePlot(scale1, scale2, scale3))
scale1.pack()
scale2.pack()
scale3.pack()
fig = plt.figure()

Thd = threading.Thread(target=tk.mainloop)
Thd.start()

updatePlot(scale1, scale2, scale3)

plt.show()
