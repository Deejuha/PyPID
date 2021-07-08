Hey, this repo was created some years ago before I really become software engineer.
Purpose of this repo was to help me with some minor tasks in exercises in university.
As always if you're looking on your code from the past you can say "Yuck! what's a badly written code".
But hey - as everyone you have to start somehow :)


# PyPID
Discrete Python PID controller supporting PWM for temperature control

Python 3.6

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
           
