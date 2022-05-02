import cmath
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
        
        #variables to calculate arithmetic mean
        mXn = np.size(roi)
        sum = 0
        result = 0
        
        #calculate mean based on roi sum
        for each in roi:
            sum += each
        result = (1/mXn) * sum
        return result

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        #declare variables to calculate geometric mean
        mXn = np.size(roi)
        product = 1
        result = 0

        #caluclate the product mean based on roi 
        for each in roi:
            product *= each
        result = (product)**(1/mXn)
        return result

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        #declare variables to calculate local_noise
        sum1 = sum(roi)
        sum2 = 0
        result = 0
        for each in roi:
            sum2 += each**2
        
        #calculate mean, variance, and g(x, y)
        local_mean = sum1/np.size(roi)
        local_variance = (sum2/np.size(roi)) - (local_mean)**2
        g_xy = roi[int((np.size(roi) - 1)/2)]

        result = g_xy - ((self.global_var**2)/(local_variance**2)) * (g_xy - local_mean)
        return result

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        #declare variables to calculate median
        result = 0
        roi = sorted(roi)

        result = roi[int((np.size(roi) - 1)/2)]
        return result


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
        local_img = self.image.copy()
        
        #Get a local copy of the image and initiate padded 0s
        padded_img = np.zeros([local_img.shape[0] + (self.filter_size - 1), local_img.shape[1] + (self.filter_size - 1)])

        #padded 0s
        for x in range(0, local_img.shape[0]):
            for y in range(0, local_img.shape[1]):
                padded_img[x + int((self.filter_size - 1)/2), y + int((self.filter_size - 1)/2)] = local_img[x, y]
        
        padded_img2 = padded_img.copy()
        #temp holds the temporary list for roi
        temp = []

        #pass in roi for each mean calculation
        for x in range(0, padded_img.shape[0] - (self.filter_size - 1)):
            for y in range(0, padded_img.shape[1] - (self.filter_size - 1)):
                for z in range(x, x + self.filter_size):
                    for k in range(y, y + self.filter_size):
                        temp.append(padded_img2[z, k])

                padded_img[x + int((self.filter_size - 1)/2), y + int((self.filter_size - 1)/2)] = self.filter(temp)
                temp = []


        result_img = padded_img.copy()
        #Deleting padded zeros from final picture
        while(result_img.shape[0] > local_img.shape[0] + ((self.filter_size - 1)/2)):
            result_img = np.delete(result_img, result_img.shape[0] - 1, 0)
        
        while(result_img.shape[0] > local_img.shape[0]):
            result_img = np.delete(result_img, 0, 0)

        while(result_img.shape[1] > local_img.shape[1] + ((self.filter_size - 1)/2)):
            result_img = np.delete(result_img, result_img.shape[1] - 1, 1)
        
        while(result_img.shape[1] > local_img.shape[1]):
            result_img = np.delete(result_img, 0, 1) 
        return result_img

