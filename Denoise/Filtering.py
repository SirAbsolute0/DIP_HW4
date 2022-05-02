from ctypes import sizeof
from threading import local
from unittest import result
import numpy as np

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        
        mXn = np.size(roi)

        sum = 0
        result = 0

        for each in roi:
            sum += each

        result = (1/mXn) * sum
        return result

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        print("testing_geometric_mean")
        return 0

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        
        return 0

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        
        return 0


    def get_adaptive_median(self):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        
        return 0


    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        local_img = self.image
        
        #Get a local copy of the image and initiate padded 0s
        padded_img = np.zeros([local_img.shape[0] + (self.filter_size - 1), local_img.shape[1] + (self.filter_size - 1)])

        #padded 0s
        for x in range(0, local_img.shape[0]):
            for y in range(0, local_img.shape[1]):
                padded_img[x + int((self.filter_size - 1)/2), y + int((self.filter_size - 1)/2)] = local_img[x, y]
        
        temp = []
        
        #pass in roi for each mean calculation
        for x in range(0, padded_img.shape[0] - (self.filter_size - 1)):
            for y in range(0, padded_img.shape[1] - (self.filter_size - 1)):
                for z in range(x, x + (self.filter_size - 1)):
                    for k in range(y, y + (self.filter_size - 1)):
                        temp.append(padded_img[z, k])


                padded_img[x + int((self.filter_size - 1)/2), y + int((self.filter_size - 1)/2)] = self.filter(temp)
                
                temp = []

        result_img = padded_img.copy()

        #Deleting padded zeros from final picture
        result_img = np.delete(result_img, result_img.shape[0] - 1, 0)
        result_img = np.delete(result_img, result_img.shape[1] - 1, 1)
        result_img = np.delete(result_img, 0, 0)
        result_img = np.delete(result_img, 0, 1)

        while(result_img.shape[0] > local_img.shape[0]):
            result_img = np.delete(result_img, 0, 0)
            result_img = np.delete(result_img, local_img.shape[0] + 1, 0)

        while(result_img.shape[1] > local_img.shape[1]):
            result_img = np.delete(result_img, 0, 1)
            result_img = np.delete(result_img, local_img.shape[1] + 1, 1)
        
        return result_img

