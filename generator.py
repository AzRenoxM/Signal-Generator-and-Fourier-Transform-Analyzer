import matplotlib.pyplot as plt
from scipy.fft import fft
import keyboard
import numpy
import time
import os

class Generator:
    def __init__(self, sampling:int, time_duration:float) -> None:
        self.sampling = sampling
        self.time_duration = time_duration


    def menu(self) -> None:
        restart_menu = True
        while restart_menu:
            os.system("cls")
            print(f"The sampling frequency you inserted is {self.sampling} Hz, and the wave is generated for {self.time_duration} seconds.")
            print("By pressing the keys 1, 2, and so on, please select the function you wish to operate with")
            print("1 - Sine\n2 - Square\n3 - Triangle\n4 - Sawtooth\n5 - WhiteNoise\nq - exit")
            restart_wait = True
            played_function = True
            while restart_wait:
                one_press = keyboard.is_pressed('1')
                two_press = keyboard.is_pressed('2')
                thr_press = keyboard.is_pressed('3')
                fou_press = keyboard.is_pressed('4')
                fiv_press = keyboard.is_pressed('5')
                q_press = keyboard.is_pressed('q')
                if one_press:
                    restart_wait = self.inner_menu("sine")
                elif two_press:
                    played_function = self.inner_menu("square")
                    if not played_function: restart_wait = False
                elif thr_press:
                    played_function = self.inner_menu("triangle")
                    if not played_function: restart_wait = False
                elif fou_press:
                    played_function = self.inner_menu("sawtooth")
                    if not played_function: restart_wait = False
                elif fiv_press:
                    played_function = self.inner_menu("whiteNoise")
                    if not played_function: restart_wait = False
                
                elif q_press:
                    os.system("cls")
                    print("Are you sure you want to quit(y/n)? ")
                    inner_restart = True
                    while inner_restart:
                        y_press = keyboard.is_pressed('y')
                        n_press = keyboard.is_pressed('n')
                        if y_press:
                            inner_restart = False
                            quit()
                        elif n_press:
                            inner_restart = False
                            restart_wait = False
                            os.system("cls")
                        else: 
                            while not (keyboard.is_pressed('y') or keyboard.is_pressed('n')):
                                time.sleep(0.1)  
                                pass  
                else:
                    while not (keyboard.is_pressed('1') or keyboard.is_pressed('2') or keyboard.is_pressed('3') or keyboard.is_pressed('4') or keyboard.is_pressed('5') or keyboard.is_pressed('q')):
                        time.sleep(0.1)  
                        pass


    def inner_menu(self, function_type:str):
        os.system("cls")
        time.sleep(0.5)
        print(f"1 - Diplay the {function_type} function")
        print(f"2 - Calculate the fourier transform and diplay the {function_type} function")
        print(f"3 - Save the {function_type} function to the .csw file")
        print(f"4 - Save the {function_type} function to the .wav file (sound file)")
        print(f"q - Back ")
        click_wait = True
        while click_wait:
            one_press = keyboard.is_pressed('1')
            two_press = keyboard.is_pressed('2')
            thr_press = keyboard.is_pressed('3')
            fou_press = keyboard.is_pressed('4')
            q_press = keyboard.is_pressed('q')
            if one_press:
                if_white_noise = False
                if str(function_type) == "whiteNoise": if_white_noise = True
                self.generate_function(str(function_type), if_white_noise, False)
                return False
            elif two_press:
                if_white_noise = False
                if str(function_type) == "whiteNoise": if_white_noise = True
                self.generate_function(str(function_type), if_white_noise, True)
                return False
            elif thr_press:
                # TODO MECHANIZM ZAPIS DO PLIKU .CSV
                return False
            elif fou_press:
                # TODO MECHANIZM ZAPIS DO PLIKU .WAV
                return False
            elif q_press:
                os.system("cls")
                time.sleep(0.5)
                return False
            else:
                while not (keyboard.is_pressed('1') or keyboard.is_pressed('2') or keyboard.is_pressed('3') or keyboard.is_pressed('4') or keyboard.is_pressed('q')):
                    time.sleep(0.1)  
                    pass


    def generate_function(self, function_type:str, whiteNoise:bool, ft_function:bool):
        os.system("cls")
        for a in range(0, 5): keyboard.send('backspace') 
        time.sleep(0.3)
        if not whiteNoise:
            Frequency = self.check_positive("frequency", function_type, ft_function)
        Amplitude = self.check_positive("amplitude", function_type, ft_function)
        if function_type == "sine":
            self.sine(Frequency, Amplitude, ft_function) #TODO DLA ft inne wartości
        elif function_type == "square":
            self.square(Frequency, Amplitude, ft_function)
        elif function_type == "triangle":
            self.triangle(Frequency, Amplitude, ft_function)
        elif function_type == "sawtooth":
            self.sawtooth(Frequency, Amplitude, ft_function)
        elif function_type == "whiteNoise":
            self.whiteNoise(Amplitude, ft_function)
        time.sleep(0.5)
        os.system("cls")


    def display_function(self, time_vector:numpy.ndarray, y_line:numpy.ndarray, function_type:str, ft_function:bool) -> None:
        if ft_function:
            time_vector, y_line = self.fourier_transform(time_vector, y_line)
        time_see = self.input_user(function_type)
        plt.plot(time_vector, y_line)
        plt.xlim(0, time_see*(10**(-3))) 
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()       
        

    def check_positive(self, name_value:str, function_type:str, ft_function:bool): 
        while True:
            try:
                if ft_function: a = float(input(f"Please insert the {name_value} of {function_type}\'fourrier transformation function: "))
                else: a = float(input(f"Please insert the {name_value} of {function_type} function: "))
                if a < 0:
                    print(f"The value of the {name_value} needs to be positive")
                else:
                    return a
            except:
                print("The value given is not a number")


    def input_user(self, function:str):
        restart_value = True
        while restart_value:
            xlim_value = int(input(f"Time range of the {function} function that you want to see(0-10 ms): "))
            # if ((xlim_value <= 0) or (xlim_value > 10)): asdasdasdasdassssssssssssssssssssssssssssssssssssssssssssssss
            #     print("write the number between 0 and 10 ms")
            if ((xlim_value > 0) and (xlim_value <= 5000)):
                return xlim_value
            else:
                print("unexpected error, rewrite the number from 0 to 10")


    def fourier_transform(self, t, y):
        N = len(t)
        dt = t[1] - t[0]
        yf = 2.0 / N * numpy.abs(fft(y)[0:N // 2])
        xf = numpy.fft.fftfreq(N, d=dt)[0:N // 2]
        return xf, yf


    def sine(self, frequency:float, amplitude:float, ft_function:bool):
        time_vector = numpy.linspace(0, self.time_duration, self.time_duration*self.sampling)
        y_line = float(amplitude)*numpy.sin(2*numpy.pi*time_vector*float(frequency))
        self.display_function(time_vector, y_line, "sine", ft_function)


    def square(self, frequency:float, amplitude:float, ft_function:bool):
        time_vector = numpy.linspace(0, self.time_duration, self.time_duration*self.sampling)
        y_line = float(amplitude)*numpy.sign(numpy.sin(2*numpy.pi*time_vector*float(frequency)))
        self.display_function(time_vector, y_line, "square", ft_function)
    
    
    def triangle(self, frequency:float, amplitude:float, ft_function:bool):
        time_vector = numpy.linspace(0, self.time_duration, self.time_duration*self.sampling)
        y_line = ((2*float(amplitude))/2*numpy.pi)*numpy.arcsin(numpy.sin(2*numpy.pi*time_vector*float(frequency)))
        self.display_function(time_vector, y_line, "triangle", ft_function)


    def sawtooth(self, frequency:float, amplitude:float, ft_function:bool):
        time_vector = numpy.linspace(0, self.time_duration, self.time_duration*self.sampling)
        y_line = ((2*float(amplitude))/2*numpy.pi)*numpy.arctan(numpy.tan(2*numpy.pi*time_vector*float(frequency)))
        self.display_function(time_vector, y_line, "sawtooth", ft_function)
    

    def whiteNoise(self, amplitude:float, ft_function:bool):
        time_vector = numpy.linspace(0, self.time_duration, self.time_duration*self.sampling)
        y_line = amplitude*(time_vector + numpy.random.rand(len(time_vector)))
        self.display_function(time_vector, y_line, "whiteNoise", ft_function)









                
