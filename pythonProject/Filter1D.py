import cv2
import numpy as np

class Filter1D:

    def __init__(self, values):
        self.values_list = values

    def low_pass_ramp(self):
        """ Return low pass filter of values """
        print("Values: ", self.values_list)
        fft_values = np.fft.fft(self.values_list)
        print("fft_values_shift Values: ", fft_values)
        fft_values_shift = np.fft.fftshift(fft_values)
        print("Values: ", fft_values_shift)
        N = len(fft_values_shift)
        filter_fft_values_shift = fft_values_shift  # filter here
        print("filter_fft_values_shift Values: ", filter_fft_values_shift)
        filter_fft_values_shift_ifftshift = np.fft.ifftshift(filter_fft_values_shift)
        print("filter_fft_values_shift_ifftshift Values: ", filter_fft_values_shift_ifftshift)
        filter_fft_values_shift_ifftshift_ifft = np.fft.ifft(filter_fft_values_shift_ifftshift)
        print("filter_fft_values_shift_ifftshift_ifft Values: ", filter_fft_values_shift_ifftshift_ifft)
        magnitude_filter_fft_values_shift_ifftshift_ifft = self.int_magnitude(filter_fft_values_shift_ifftshift_ifft)
        print("magnitude_filter_fft_values_shift_ifftshift_ifft Values: ", magnitude_filter_fft_values_shift_ifftshift_ifft)
        return filter_fft_values_shift_ifftshift_ifft

    def int_magnitude(self, complex_values):
        """Return magnitude of complex_values"""
        magnitude_values = []
        for complex_value in complex_values:
            magnitude = int(np.round(np.sqrt(np.power(np.real(complex_value), 2) + np.power(np.imag(complex_value), 2))))
            magnitude_values.append(magnitude)
        return magnitude_values
