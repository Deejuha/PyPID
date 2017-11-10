class DiscretePIDController:
    """
    Discrete PID controller to control temperature with analog or on-off heater with implemented PWM.
    ----------
    File :          PID.py
    Author :        Michal Juszczyk
    Mail :          michaljuszczyk2@gmail.com
    Version :       0.1
    Date :          10 november 2017
    Python version : 3.6
    ----------
    How to use :
        Settings :
            1.Create instance
            2.Set kP, kI, kD and refresh time by using set_PID method
            3.Set desire temperature by using set_final_temperature method
            4.If you want to use PWM :
                use PWM_enabled method and set width of each cycle of PWM by using set_PWM_cycle_time

        Main Loop :
            1.Calculate PID by using update method
            2.If you're using percent PID value:
                use return_PID_percent_value method to overwrite your variable responsible for output change
            2.If you're using PWM with PID percent fulfillment
                use return_PWM_value method to overwrite your boolean variable responsible for output change
            3.Update output
    """
    import time
    _kP = 0
    _kI = 0
    _kD = 0
    outputPWM = False
    temperatureFeedback = 0.0
    temperatureSet = 0.0
    temperatureLastSample = 0.0
    cleanOutputValue = 0.0
    refactoredOutputValue = 0.0
    proportionalElement = 0.0
    integralElement = 0.0
    derivativeElement = 0.0
    refreshTime = 0.0
    currentTime = time.time()
    lastSampleTime = currentTime
    lastTemperatureDelta = 0.0
    PWMcycleTime = 2.0
    PWMenabled = False
    PWMlastCycleStartTime = currentTime

    def update(self):
        """
        Method calculating PID - should be used in every cycle of program.
        When it is time to calculate (after refresh time passed) it's changing analog output of PID.
        If PWM is enabled it's also updating boolean value of it, independently of PID algorithm.
        """
        if self.refreshTime <= 0 or self._kP <= 0 and self._kI <= 0 and self._kD <= 0:
            raise Exception("use ,,set_PID'' method to set kP, kI, kD, refresh time to more than 0! ")

        self.currentTime = self.time.time()
        # checking reset (watch clean method)
        if self.lastSampleTime == 0:
            self.lastSampleTime = self.currentTime

        timeDelta = self.currentTime - self.lastSampleTime
        if timeDelta >= self.refreshTime:
            temperatureDelta = self.temperatureSet - self.temperatureFeedback
            self.proportionalElement = self._kP * temperatureDelta
            self.integralElement = self._kI * ((self.temperatureLastSample + self.temperatureFeedback)
                                               * timeDelta / 2)
            self.derivativeElement = self._kD * ((temperatureDelta - self.lastTemperatureDelta)
                                                 / timeDelta)
            self.cleanOutputValue = self.proportionalElement + self.integralElement + self.derivativeElement
            self.lastTemperatureDelta = temperatureDelta
            self.lastSampleTime = self.currentTime
            if self.cleanOutputValue > 100:
                self.refactoredOutputValue = 100
            elif self.cleanOutputValue < 0:
                self.refactoredOutputValue = 0
            else:
                self.refactoredOutputValue = round(self.cleanOutputValue, 2)

        if self.PWMenabled:
            if self.PWMcycleTime <= 0:
                raise Exception("use set_PWM_cycle_time method to set your maximum pulse width to more than 0!")
            PWMtimeDelta = self.currentTime - self.PWMlastCycleStartTime
            if PWMtimeDelta <= (self.refactoredOutputValue * self.PWMcycleTime / 100):
                self.outputPWM = True
            else:
                self.outputPWM = False
            if PWMtimeDelta >= self.PWMcycleTime:
                self.PWMlastCycleStartTime = self.currentTime
        else:
            self.outputPWM = False

    def clean(self):
        """
        Method changing PID variables to default values - 0, so you can forgot about integration and differentiation
        problems after resetting your PID
        """
        self.temperatureLastSample = 0.0
        self.lastTemperatureDelta = 0.0
        self.lastSampleTime = 0.0
        self._kP = 0.0
        self._kI = 0.0
        self._kD = 0.0

    def set_PID(self, Kp, Ki, Kd, PIDrefreshTime):
        """
        Method accepts values to set PID elements. Except Ki and Kd they should be numbers (integer / float) more than 0
        ----------
            Inputs :
                Kp - number
                    Proportional gain

                Ki - number
                    Integration gain

                Kd - number
                    Differential gain

                PIDrefreshTime - number
                    Time in seconds between every run of update method
        """
        self._kP = Kp
        self._kI = Ki
        self._kD = Kd
        self.refreshTime = PIDrefreshTime

    def set_final_temperature(self, setTemperature):
        """
        Method accept number value to set desirable temperature on your object
        ----------
            Inputs :
                setTemperature - number
        """
        self.temperatureSet = setTemperature

    def give_feedback_value(self, feedbackValue):
        """
        Method accept value of feedback sensor
        ----------
            Inputs :
                feedbackValue - number
        """
        self.temperatureFeedback = feedbackValue

    def return_PWM_value(self):
        """
        Method returns temporary boolean value of PWM.
        Pulse width depends on calculated PID percent value.
        That method should overwrite your's physical output every cycle of program
        ----------
            Returns :
                outputPWM - boolean
        """
        if not self.PWMenabled:
            raise Exception("Can't return boolean value when PWM is off. Use PWM_enabled() on your settings")
        return self.outputPWM

    def return_PID_percent_value(self):
        """
        Method returns temporary PID percent output value (0-100%).
        That method should overwrite your's physical output every cycle of program
        ----------
            Returns :
                outputPWM - boolean
        """
        return self.refactoredOutputValue

    def PWM_enabled(self):
        """
        Method toggling on PWM
        """
        self.PWMenabled = True

    def PWM_disabled(self):
        """
        Method toggling off PWM
        """
        self.PWMenabled = False

    def set_PWM_cycle_time(self, setPWMCycleTime):
        """
        Method accept number value to set PWM cycle time
        ----------
            Inputs :
                setPWMCycleTime - number
                    Time of each PWM cycle in seconds
        """
        self.PWMcycleTime = setPWMCycleTime
