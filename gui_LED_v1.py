# RPi LED control
# Version: 1.0
# Author: Nuno Sidonio Andrade Pereira
# Date: 2017-05-01
# Description: Uses guizero to build an interface to control 5 LEDs with gpiozero
# Developed for: Raspberry Pi B with python 3.4
# License: copy, modify, distribute, delete, be happy and enjoy life :-)
#
# Install guizero: sudo pip3 install guizero

# Import from packages
from guizero import App, Combo, Slider, Text, TextBox, PushButton, info, yesno, error, warn
from gpiozero import LED


# Definition of available GPIOs on your version of Raspberry Pi
GPIO_list = [ '0', '1', '4', '7', '8', '9', '10', '11', '14', '17', '18', '21', '22', '23', '24', '25' ]

# define the objects LED_Color
LED_Red    = LED( 0, active_high=True, initial_value=False )
LED_Orange = LED( 1, active_high=True, initial_value=False )
LED_Yellow = LED( 4, active_high=True, initial_value=False )
LED_Green  = LED( 7, active_high=True, initial_value=False )
LED_Blue   = LED( 8, active_high=True, initial_value=False )

# Functions definition

def set_LED2GPIO():
    Flag = check_GPIO()    
    if Flag == True :
        info( 'RPi LED v1', 'LED-GPIO map ok' )
        print( 'GPIOs ok' )
        print( '\nLEDs set to:\n' )
        print_options()
        map_LED2GPIO()    
    else:
        print( '\nLED-GPIO map not set!' )        

    return    

def map_LED2GPIO(): # this function is only called once
    global LED_Red
    global LED_Orange
    global LED_Yellow
    global LED_Green
    global LED_Blue    

    # We need to close the objects to re-assign the new pins; even if the pins are the same
    LED_Red.close()
    LED_Orange.close()
    LED_Yellow.close()
    LED_Green.close()
    LED_Blue.close()
    
    LED_Red    = LED( eval( LED_Red_gpio.get() ), active_high=True, initial_value=False )
    LED_Orange = LED( eval( LED_Orange_gpio.get() ), active_high=True, initial_value=False )
    LED_Yellow = LED( eval( LED_Yellow_gpio.get() ), active_high=True, initial_value=False )
    LED_Green  = LED( eval( LED_Green_gpio.get() ), active_high=True, initial_value=False )
    LED_Blue   = LED( eval( LED_Blue_gpio.get() ), active_high=True, initial_value=False )

    if LED_Red_mode.get() == 'On':
        LED_Red.on()
    elif LED_Red_mode.get() == 'Blink':
        LED_Red.blink( LED_Red_onTime.get(), LED_Red_offTime.get(), background = True )
         
    if LED_Orange_mode.get() == 'On':
        LED_Orange.on()
    elif LED_Orange_mode.get() == 'Blink':
        LED_Orange.blink( LED_Orange_onTime.get(), LED_Orange_offTime.get(), background = True )

    if LED_Orange_mode.get() == 'On':
        LED_Orange.on()
    elif LED_Orange_mode.get() == 'Blink':
        LED_Orange.blink( LED_Orange_onTime.get(), LED_Orange_offTime.get(), background = True )

    if LED_Yellow_mode.get() == 'On':
        LED_Yellow.on()
    elif LED_Yellow_mode.get() == 'Blink':
        LED_Yellow.blink( LED_Yellow_onTime.get(), LED_Yellow_offTime.get(), background = True )

    if LED_Green_mode.get() == 'On':
        LED_Green.on()
    elif LED_Green_mode.get() == 'Blink':
        LED_Green.blink( LED_Green_onTime.get(), LED_Green_offTime.get(), background = True )

    if LED_Blue_mode.get() == 'On':
        LED_Blue.on()
    elif LED_Blue_mode.get() == 'Blink':
        LED_Blue.blink( LED_Blue_onTime.get(), LED_Blue_offTime.get(), background = True )
        
    return


def exit_mode():
    if yesno( 'Exit', 'Do you want to quit?' ):
        print( "Closing application" )
        app.destroy()
    return

def check_GPIO():
    print( '\nChecking GPIOs' )
    LED_gpio = [LED_Red_gpio.get(), LED_Orange_gpio.get(), LED_Yellow_gpio.get(),
                LED_Green_gpio.get(), LED_Blue_gpio.get() ]
    # check if there are GPIO boxes empty
    if any( gpio == '' for gpio in LED_gpio ):         
        error( 'Error', 'Undefined GPIO(s)!!' )
        print( 'Error: Undefined GPIO(s)!!' )
        print( 'Available GPIOs:', GPIO_list )
        Flag = False
    # check if there are repeated GPIOs in the boxes
    elif any( LED_gpio.count(gpio) > 1 for gpio in LED_gpio ):
        warn( 'Warning', 'Repeated GPIO(s)!!' )
        print( 'Warning: Repeated GPIO(s)!!' )        
        Flag = False
    # check if the gpios are available    
    elif all( gpio in GPIO_list for gpio in LED_gpio ): 
        Flag = True
    else:        
        error( 'Error', 'Unavailable GPIO(s)!!' )
        print( 'Error: Unavailable GPIO(s)!!' )
        print( 'Available GPIOs:', GPIO_list )
        Flag = False
    return  Flag
    
def print_options():
    print( 'LED Red:   ', 'gpio:',LED_Red_gpio.get(), '\tstatus:', LED_Red_mode.get(), '\tOn time:', LED_Red_onTime.get(), '\tOff time:', LED_Red_offTime.get() )
    print( 'LED Orange:', 'gpio:',LED_Orange_gpio.get(), '\tstatus:', LED_Orange_mode.get(), '\tOn time:', LED_Orange_onTime.get(), '\tOff time:', LED_Orange_offTime.get() )
    print( 'LED Yellow:', 'gpio:',LED_Yellow_gpio.get(), '\tstatus:', LED_Yellow_mode.get(), '\tOn Time:', LED_Yellow_onTime.get(), '\tOff Time:', LED_Yellow_offTime.get() )
    print( 'LED Green: ', 'gpio:',LED_Green_gpio.get(), '\tstatus:', LED_Green_mode.get(), '\tOn Time:', LED_Green_onTime.get(), '\tOff Time:', LED_Green_offTime.get() )
    print( 'LED Blue:  ', 'gpio:',LED_Blue_gpio.get(), '\tstatus:', LED_Blue_mode.get(), '\tOn Time:', LED_Blue_onTime.get(), '\tOff Time:', LED_Blue_offTime.get() )
    return

    
# Define master App
app = App( title='RPi LED control (v1.0)', width=400, height=300, layout='grid' )

# Slider min-max values
onTime_min = 1
onTime_max = 10
offTime_min = 0
offTime_max = 10

# LED GPIO pin maping
LED_Red_pin = 10
LED_Orange_pin = 11
LED_Yellow_pin = 12
LED_Green_pin = 13
LED_Blue_pin = 14

# Header labels
LED_label         = Text( app, text='LED', grid=[0,0], size=10, font='Helvetica', align='left' )
LED_pin_label     = Text( app, text='GPIO', grid=[0,1], size=10, font='Helvetica', align='left' )
LED_mode_label    = Text( app, text='mode', grid=[0,2], size=10, font='Helvetica', align='left' )
LED_onTime_label  = Text( app, text='On time (s)', grid=[0,3], size=10, font='Helvetica', align='left' )
LED_offTime_label = Text( app, text='Off time (s)', grid=[0,4], size=10, font='Helvetica', align='left' )

# LED RED
LED_Red_label   = Text( app, text='Red', grid=[1,0], size=10, font='Helvetica', color='Red', align='left' )
LED_Red_gpio    = TextBox( app, text='', width=2, grid=[1,1], align='left' )
LED_Red_mode    = Combo( app, options=['Off', 'On', 'Blink'], grid=[1,2], align='left' )
LED_Red_onTime  = Slider( app, start=onTime_min, end=onTime_max, grid=[1,3] )
LED_Red_offTime = Slider( app, start=offTime_min, end=offTime_max, grid=[1,4] )

# LED ORANGE
LED_Orange_label   = Text( app, text='Orange', grid=[2,0], size=10, font='Helvetica', color='Orange', align='left' )
LED_Orange_gpio    = TextBox( app, text='', width=2, grid=[2,1], align='left' )
LED_Orange_mode    = Combo( app, options=['Off', 'On', 'Blink'], grid=[2,2], align='left' )
LED_Orange_onTime  = Slider( app, start=onTime_min, end=onTime_max, grid=[2,3] )
LED_Orange_offTime = Slider( app, start=offTime_min, end=offTime_max, grid=[2,4] )

# LED YELLOW
LED_Yellow_label   = Text( app, text='Yellow', grid=[3,0], size=10, font='Helvetica', color='Yellow', align='left' )
LED_Yellow_gpio    = TextBox( app, text='', width=2, grid=[3,1], align='left' )
LED_Yellow_mode    = Combo( app, options=['Off', 'On', 'Blink'], grid=[3,2], align='left' )
LED_Yellow_onTime  = Slider( app, start=onTime_min, end=onTime_max, grid=[3,3] )
LED_Yellow_offTime = Slider( app, start=offTime_min, end=offTime_max, grid=[3,4] )

# LED GREEN
LED_Green_label   = Text( app, text='Green', grid=[4,0], size=10, font='Helvetica', color='Green', align='left' )
LED_Green_gpio    = TextBox( app, text='', width=2, grid=[4,1], align='left' )
LED_Green_mode    = Combo( app, options=['Off', 'On', 'Blink'], grid=[4,2], align='left' )
LED_Green_onTime  = Slider( app, start=onTime_min, end=onTime_max, grid=[4,3] )
LED_Green_offTime = Slider( app, start=offTime_min, end=offTime_max, grid=[4,4] )

# LED BLUE
LED_Blue_label   = Text( app, text='Blue', grid=[5,0], size=10, font='Helvetica', color='Blue', align='left' )
LED_Blue_gpio    = TextBox( app, text='', width=2, grid=[5,1], align='left' )
LED_Blue_mode    = Combo( app, options=['Off', 'On', 'Blink'], grid=[5,2], align='left' )
LED_Blue_onTime  = Slider( app, start=onTime_min, end=onTime_max, grid=[5,3] )
LED_Blue_offTime = Slider( app, start=offTime_min, end=offTime_max, grid=[5,4] )

# PUSH BUTTONS
set_button  = PushButton( app, command=set_LED2GPIO, text='Set', grid=[6,0], align='left' )
exit_button = PushButton( app, command=exit_mode, text='Exit', grid=[6,4], align='left' )

# Footnote text
footnote = Text( app, text='2017|nsap', grid=[7,0], size='9', font='Helvetica', align='right' )

# execute exit_mode() when user tries to close window
app.on_close( exit_mode )

# Console text
print( '\nRPi LED control (v1.0)\n' )
print( 'Available GPIOs:\n', GPIO_list )

app.display()
