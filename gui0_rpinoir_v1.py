# giu0_rpinoir
# Version: 1.0
# Author: Nuno Sidonio Andrade Pereira
# Date: 2017-05-24
# Description: Uses guizero to build an interface to control RPi NoIR camera 
# Developed for: Raspberry Pi 3 B with Raspbian PIXEL and python 3.4
# License: copy, modify, distribute, delete, be happy and enjoy life :-)
#
# Install guizero: sudo pip3 install guizero

# Import from packages
import picamera
import time
from guizero import App, Combo, Slider, Text, TextBox, PushButton, CheckBox, info, yesno, error, warn
from bluedot import BlueDot

# Begin: global variables----------------------------------------------------------
ExposureMode_list = [ 'auto', 'off', 'nightpreview', 'backlight', 'spotlight',
                  'sports', 'snow', 'beach', 'verylong', 'fixedfps',
                  'antishake', 'fireworks' ]

EffectMode_list = [ 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint',
                'hatch', 'gpen', 'pastel', 'watercolor', 'film', 'blur', 'saturation',
                'colorswap', 'posterise', 'colourpoint', 'colorbalance', 'cartoon',
                'deinterlace1', 'deinterlace2', 'washedout' ]

MeteringMode_list = [ 'average', 'spot', 'backlit', 'matrix' ]

AWBMode_list = [ 'auto', 'off', 'sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent',
             'incandescent', 'flash', 'horizon' ]

DynamicRangeComp_list = [ 'off', 'low', 'med', 'high' ]

ISO_list = [ 0, 100, 200, 320, 400, 500, 640, 800 ]

Resolution_list = [ '2592x1944', '1920x1080', '1296x972', '1296x730', '1080x720',
                    '1024x768', '800x600', '640x480' ]

Rotation_list = [ 0, 90, 180, 270 ]

picCounter = 1

# Define BluedDot to interact with BluedDot (Android)
BlueDot = BlueDot(auto_start_server=True, print_messages=True)

# Slider values
previewTime_min = 2.
previewTime_max = 20.
AWBgains_scale = 10.

# End: global variables----------------------------------------------------------


# Functions definition

def camera_Modes():

    camera = picamera.PiCamera()

    try:
        print( '\nAWB modes:\n', camera.AWB_MODES )
        print( '\nExposures modes:\n', camera.EXPOSURE_MODES )    
        print( '\nMetering modes:\n', camera.METER_MODES )
        print( '\nImage effects:\n', camera.IMAGE_EFFECTS )

    finally:
        camera.close()


def preview_Image():

    global AWBgains_scale
    camera = picamera.PiCamera()
    
    try:
        camera.framerate = 10
        camera.exposure_mode = Exposure_mode.get()        
        effect =  Effect_mode.get()        
        camera.image_effect = effect
        camera.meter_mode = Metering_mode.get()
        camera.awb_mode = AWB_mode.get()
        camera.drc_strength = DynamicRangeComp_mode.get()
        camera.iso = int( ISO_value.get() )
        camera.rotation = Rotation_value.get()
        camera.hflip = HFlip_chkbox.get_value()
        camera.vflip = VFlip_chkbox.get_value()
        camera.contrast = int( Contrast.get() )
        camera.awb_gains = float( AWBgains.get() ) / AWBgains_scale
        camera.brightness = int( Brightness.get() )
        camera.saturation = int( Saturation.get() )
        camera.shutter_speed = 0 
        camera.start_preview(fullscreen=False, window=(100,100, 640, 480))        
        print( '\nPreview is:', camera.previewing )        
        fileName = 'RPiNoIR_test_imageEffect_{0}{1}'
        time.sleep( int( previewTime.get() ) )
        camera.exif_tags[ 'IFD=.Artist' ] = 'Nuno S. A. Pereira'
        camera.exif_tags[ 'IFD0.Copyrights' ] = '2017 | nsap'
        # the method format() is used to pass variables to the string fileName
        camera.stop_preview()
        print( 'Preview is:', camera.previewing )        
        
    finally:
        camera.close()

    
def capture_Image():

    camera = picamera.PiCamera()

    global picCounter
    global AWBgains_scale
    
    try:        
        camera.exposure_mode = Exposure_mode.get()        
        effect =  Effect_mode.get()        
        camera.image_effect = effect
        camera.meter_mode = Metering_mode.get()
        camera.awb_mode = AWB_mode.get()
        camera.drc_strength = DynamicRangeComp_mode.get()
        camera.iso = int( ISO_value.get() )
        camera.rotation = Rotation_value.get()
        camera.hflip = HFlip_chkbox.get_value()
        camera.vflip = VFlip_chkbox.get_value()
        camera.contrast = int( Contrast.get() )
        camera.awb_gains = float( AWBgains.get() ) / AWBgains_scale
        camera.brightness = int( Brightness.get() )
        camera.saturation = int( Saturation.get() )
        camera.shutter_speed = 0
        camera.resolution = Resolution.get()
        fileName = 'RPiNoIR_%02d_{0}{1}' % picCounter        
        camera.exif_tags[ 'IFD=.Artist' ] = 'Nuno S. A. Pereira'
        camera.exif_tags[ 'IFD0.Copyrights' ] = '2017 | nsap'
        # the method format() is used to pass variables to the string fileName
        camera.capture( fileName.format(effect, '.jpg') )
        picCounter += 1       
    finally:        
        camera.close()


def BlueDot_control():

    if BlueDot.is_connected == True:
        info( 'BlueDot', 'Press bluedot when ready to capture' )
        try:
            BlueDot.wait_for_press()
            BlueDot.wait_for_release()
            capture_Image()
        finally:
            return
    else:
        error( 'BlueDot', 'Device not connected' )
    

def exit_mode():
    if yesno( 'Exit', 'Do you want to quit?' ):
        print( "Closing application" )
        app.destroy()
    return

    
# Define master App
app = App( title='RPi NoIR control (v1.0)', width=425, height=335, layout='grid' )

# Exposure mode combo
ExposureMode_label = Text( app, text='Exposure', grid=[1,0], size=10, font='Helvetica', color='Blue', align='left' )
Exposure_mode = Combo( app, options=ExposureMode_list, grid=[1,1], align='left' )

# Image Effect combo
EffectMode_label = Text( app, text='Effect', grid=[2,0], size=10, font='Helvetica', color='Blue', align='left' )
Effect_mode = Combo( app, options=EffectMode_list, grid=[2,1], align='left' )

# Metering mode combo
MeteringMode_label = Text( app, text='Metering', grid=[3,0], size=10, font='Helvetica', color='Blue', align='left' )
Metering_mode = Combo( app, options=MeteringMode_list, grid=[3,1], align='left' )

# AWB mode combo
AWBMode_label = Text( app, text='AWB', grid=[4,0], size=10, font='Helvetica', color='Blue', align='left' )
AWB_mode = Combo( app, options=AWBMode_list, grid=[4,1], align='left' )

# Dynamic range compression combo
DynamicRangeComp_label = Text( app, text='DynRangComp', grid=[5,0], size=10, font='Helvetica', color='Blue', align='left' )
DynamicRangeComp_mode  = Combo( app, options=DynamicRangeComp_list, grid=[5,1], align='left' )

# ISO combo
ISO_label = Text( app, text='ISO', grid=[6,0], size=10, font='Helvetica', color='Blue', align='left' )
ISO_value = Combo( app, options=ISO_list, grid=[6,1], align='left' )

# Rotation combo
Rotation_label = Text( app, text='Rotation', grid=[1,2], size=10, font='Helvetica', color='Blue', align='left' )
Rotation_value = Combo( app, options=Rotation_list, grid=[1,3], align='left' )

# Push buttons
preview_button = PushButton( app, command=preview_Image, text='Preview (s)', grid=[7,0], align='left' )
capture_button = PushButton( app, command=capture_Image, text='  Capture  ', grid=[8,0], align='left' )
exit_button = PushButton( app, command=exit_mode, text='Exit', grid=[9,2], align='left' )
modes_button = PushButton( app, command=camera_Modes, text='Modes', grid=[9,3], align='left' )

# Resolution combo
Resolution_label = Text( app, text='Resolution', grid=[8,1], size=10, font='Helvetica', color='Blue', align='left' )
Resolution = Combo( app, options=Resolution_list, grid=[8,2], align='left')

# BlueDot_button
BlueDot_label = Text( app, text='BlueDot available', grid=[7,2], size=10, font='Helvetica', color='Blue', align='left' )
BlueDot_button = PushButton( app, command=BlueDot_control, text='BlueDot', grid=[8,3], align='left' )

# Check boxes
HFlip_chkbox = CheckBox(app, text='Hflip', grid=[2,2], align="left")
VFlip_chkbox = CheckBox(app, text='Vflip', grid=[2,3], align="left")

# Sliders
previewTime = Slider( app, start=previewTime_min, end=previewTime_max, grid=[7,1] )

# Contrast slider
Contrast_label = Text( app, text='Contrast', grid=[3,2], size=10, font='Helvetica', color='Blue', align='left' )
Contrast = Slider( app, start=-100, end=100, grid=[3,3] )

# AWB gain slider
AWBgains_label = Text( app, text='AWB gains (x10)', grid=[4,2], size=10, font='Helvetica', color='Blue', align='left' )
AWBgains = Slider( app, start=0, end=8*AWBgains_scale, grid=[4,3] )

# Brightness slider
Brightness_label = Text( app, text='Brightness', grid=[5,2], size=10, font='Helvetica', color='Blue', align='left' )
Brightness = Slider( app, start=0, end=100, grid=[5,3] )

# Saturation slider
Saturation_label = Text( app, text='Saturation', grid=[6,2], size=10, font='Helvetica', color='Blue', align='left' )
Saturation = Slider( app, start=-100, end=100, grid=[6,3] )

# Footnote text
footnote = Text( app, text='2017|nsap', grid=[9,0], size='9', font='Helvetica', align='left' )

# execute exit_mode() when user tries to close window
app.on_close( exit_mode )

# Console text
print( '\nRPi NoIR control (v1.0)\n2017|nsap' )


app.display()

