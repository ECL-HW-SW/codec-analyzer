import cv2
import numpy as np
import PIL.Image as im

def get_image_array(path, color_space, package = 'PIL'):
    """Acquires numpy array from an image using either PIL or CV2"""

    if package.lower() == 'pil':
        if color_space.lower() == "rgb":
            imgArray = np.array(im.open(path))
        elif color_space.lower() == "ycbcr":
            imgArray = np.array(im.open(path).convert('YCbCr'))
        else:
            print("That is not a valid color space.")
    elif package.lower() == 'cv2':
        if color_space.lower() == "rgb":
            imgArray = cv2.imread(path, 1)
        elif color_space.lower() == "ycbcr":
            imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
        elif color_space.lower() == "y":
            imgArray = cv2.cvtColor(cv2.imread(path, 1), cv2.COLOR_BGR2YCR_CB)
            return imgArray[:,:,0]
        else:
            print("That is not a valid color space.")
    
    return imgArray