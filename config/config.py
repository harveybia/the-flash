import cv2
import time
import Tkinter as tk
from PIL import Image, ImageTk

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

ex_img = cv2.imread('../tests/1.JPG',0)

WIDTH, HEIGHT = ex_img.shape
ex_img = cv2.resize(ex_img, dsize=(WIDTH//16, HEIGHT//16))
blurred = cv2.medianBlur(ex_img, 5)
#blurred = cv2.GaussianBlur(ex_img, (5,5), 0)
edges = cv2.Canny(blurred,0,500)

def grayToRGB(img):
    # Converts grayscale image into RGB
    # This conversion uses numpy array operation and takes less time
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # By accessing pixel arrays:
    # splited = cv2.split(image)
    # B = splited[:,0]
    # G = splited[:,1]
    # R = splited[:,2]
    # Merged = cv2.merge((R, G, B))

def grayToTkImage(img):
    # Convert the Image object into a TkPhoto object
    im = Image.fromarray(grayToRGB(img))
    return ImageTk.PhotoImage(image=im)

@profile
def findEdges(img, blur_factor, edge_low, edge_high):
    blurred = cv2.medianBlur(img, blur_factor//2*2+1)
    edges = cv2.Canny(blurred, edge_low, edge_high)
    return edges

@profile
def determinePolynominals(img):
    # CORE, Closed source code
    # To be Implemented
    return img

# Create a Tkinter root
root = tk.Tk()
root.geometry("500x500+10+10")

# Temporary Display Code
processed_img = findEdges(ex_img, 5, 55, 200)
tk_img = grayToTkImage(processed_img)
imageLabel = tk.Label(root, image = tk_img, height=500, width=500)
imageLabel.image = tk_img
imageLabel.pack()

tk.mainloop()
