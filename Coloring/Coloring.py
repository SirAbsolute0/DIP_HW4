from threading import local
import numpy as np
import random
import cmath
class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''
       #Create variables for slicing
        local_img = image.copy()
        slice_value = int(255/n_slices)
        value = slice_value
        colors = []

        #Create regions depend on the number of slices, if slice is uneven => do n+1 slices
        while(value <= 255):
            R = random.randint(0, 254)
            G = random.randint(0, 254)
            B = random.randint(0, 254)
            colors.append((R, G, B))
            value += slice_value
        
        #Create an empty color picture
        final_img = np.zeros((local_img.shape[0],local_img.shape[1],3))

        #intensity slicing depending on the greyscale level
        for x in range(0, local_img.shape[0]):
            for y in range(0, local_img.shape[1]):
                for i in range(0, n_slices):
                    if(local_img[x, y] <= (slice_value*i)):
                        final_img[x, y] = colors[i]
                        break
                    else:
                        pass

        return final_img

    def color_assign(pixel, theta, i):
        
        k = (255*(i - 1) + 255*i)/2
        R = 255*cmath.sin(k + theta[0])
        G = 255*cmath.sin(k + theta[1])
        B = 255*cmath.sin(k + theta[2])

        result = [R,G,B]
        return result
    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''
       #Create variables for color transformation
        local_img = image.copy()
        slice_value = int(255/n_slices)
        value = slice_value
        colors = []

        #Create regions depend on the number of slices, if slice is uneven => do n+1 slices
        while(value <= 255):
            R = random.randint(0, 254)
            G = random.randint(0, 254)
            B = random.randint(0, 254)
            colors.append((R, G, B))
            value += slice_value

        #Create an empty color picture
        final_img = np.zeros((local_img.shape[0],local_img.shape[1],3))

        #intensity slicing depending on the greyscale level
        for x in range(0, local_img.shape[0]):
            for y in range(0, local_img.shape[1]):
                for i in range(0, n_slices):
                    if(local_img[x, y] <= (slice_value*i)):
                        final_img[x, y] = self.color_assign(final_img[x, y], theta, i)
                        break
                    else:
                        pass

        return final_img



        

