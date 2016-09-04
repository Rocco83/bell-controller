#!/usr/bin/env python2.7
# script inspirate by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
# GPIO 17: start bell FESTA
# GPIO 27: start bell FUNERALE
# GPIO 22: start bell ORA PIA
# GPIO 26: accendi amplificatore
# GPIO  6: spegni raspberry
# GPIO 13: stop bell
import RPi.GPIO as GPIO
import time
import pygame
import fcntl, sys, os
import thread
import errno

# define variables
pid_file = '/var/run/bell.pid'
sound_basedir="/home/pi/sound/"
fifo_file = '/var/run/bell.fifo'

def audio_filename(pin):
    #print pin
    return {
        17: "1-FESTA.wav",
        27: "2-FUNERALE.wav",
        22: "3-ORA_PIA.wav",
    }.get(pin, "") 

## now we'll define two threaded callback functions
## these will run in another thread when our events are detected
#def my_callback():
#    global time_stamp       # put in to debounce
#    time_now = time.time()
#    if (time_now - time_stamp) >= 0.3:
#        print "falling edge detected on 17"
#    time_stamp = time_now
#
#def my_callback2():
#    global time_stamp2       # put in to debounce - note we need a second time stamp
#    time_now = time.time()
#    if (time_now - time_stamp2) >= 0.3:
#        print "falling edge detected on 23"
#    time_stamp2 = time_now

def play_audio(filename):
    if pygame.mixer.music.get_busy() == True:
        print "another audio is already playing"
        return
    # turn on the main output
    GPIO.output(26, GPIO.LOW)
#    pygame.mixer.init()
    print "start audio"
    #pygame.mixer.music.load(sound_basedir + "sos.mp3")
    pygame.mixer.music.load(sound_basedir + filename)
    print "play " + sound_basedir + filename 
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        time.sleep(0.020)
        continue
    # turn off the main output
    GPIO.output(26, GPIO.HIGH)

def stop_audio(pin):
    print "stop all audio"
    #pygame.mixer.init()
    if pygame.mixer.music.get_busy() == True:
        try:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()
        except pygame.error(e):
            print "error" + e
            pass
    else:
        print "no current audio playing, not stopping"
    
def shutdown_request(channel):
    print "change in GPIO: ", channel
    print GPIO.input(channel)
    # double check current input
    if GPIO.input(channel):
        #print str(datetime.datetime.now()), " Shutdown request"
        print str(time.strftime("%H.%M.%S - %d %m %Y")), " Shutdown request"
        sys.stdout.flush()
        os.system('/sbin/shutdown -h now')
        
def gpio_pressed(pin):
    # debug
    print "current pin status: 17: %s, 27: %s, 22: %s, 13: %s, 6: %s" % (GPIO.input(17), GPIO.input(27), GPIO.input(22), GPIO.input(13), GPIO.input(6))
    print "pin: %s" % pin
    #print pin
    # doublecheck input
    if ( GPIO.input(pin) != 1):
        print "quirk input: asked for pin %s that is off currently" % pin
        return
    audio = audio_filename(pin)
    if ( audio != "" ):
        print "play audio: audio"
        thread.start_new_thread(play_audio, (audio,))
    if ( pin == 13 ):
        stop_audio(pin)
    if ( pin == 6 ):
        shutdown_request(pin)

# main()

# check if another process is running
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print "another instance of this program is running"
    sys.exit(0)

# initialize the mixer to be used later
pygame.mixer.init()

# create the FIFO and open it
try:
    os.mkfifo(fifo_file)
except OSError, e:
    print "Failed to create FIFO: %s, continuing anyway" % e
fifo_fp = os.open(fifo_file, os.O_RDONLY|os.O_NONBLOCK)

# initialize GPIO
# http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
# this set the pin number to BCM
GPIO.setmode(GPIO.BCM)

# pins already have a pull down resistor in the circuit
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(6, GPIO.IN)
#time_stamp = time.time()
#time_stamp2 = time.time()

# initialize variables
input17 = 0
input27 = 0
input22 = 0
input13 = 0
input6 = 0

# only one thread is running for callback
# i need to thread the function if not returning immediately
GPIO.add_event_detect(17, GPIO.RISING, bouncetime=500, callback=gpio_pressed)
GPIO.add_event_detect(27, GPIO.RISING, bouncetime=500, callback=gpio_pressed)
GPIO.add_event_detect(22, GPIO.RISING, bouncetime=500, callback=gpio_pressed)
GPIO.add_event_detect(13, GPIO.RISING, bouncetime=500, callback=gpio_pressed)
GPIO.add_event_detect(6, GPIO.RISING, bouncetime=500, callback=gpio_pressed)

try:
    print "main()"
    print ("17: %s, 27: %s, 22: %s, 13: %s, 6: %s" % ( input17, input27, input22, input13, input6))
    while True:
        prev17 = input17
        input17 = GPIO.input(17)
        prev27 = input27
        input27 = GPIO.input(27)
        prev22 = input22
        #input22 = GPIO.input(22)
        prev13 = input13
        input13 = GPIO.input(13)
        prev6 = input6
        input6 = GPIO.input(6)
        if ( prev17 != input17 or prev27 != input27 or prev22 != input22 or prev13 != input13 or prev6 != input6 ):
            print ("17: %s, 27: %s, 22: %s, 13: %s, 6: %s" % ( input17, input27, input22, input13, input6))
        time.sleep(0.020)
        # TODO implement the code here
        # http://stackoverflow.com/questions/14345816/how-to-read-named-fifo-non-blockingly
        #ext_command = fifo_fp.read()
        #print ext_command
#        try:
#            buffer = os.read(io, BUFFER_SIZE)
#        except OSError as err:
#            if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
#                buffer = None
#            else:
#                raise  # something else has happened -- better reraise
#        
#        if buffer is None: 
#            # nothing was received -- do something else
#        else:
#            # buffer contains some received data -- do something with it
#                #time.sleep(1)
#                

except KeyboardInterrupt:
    print "CTRL+C pressed, exiting"
finally:
    GPIO.cleanup()       # clean up GPIO on exiting from try
    pygame.mixer.quit()  # clean up mixer
    os.close(fifo_fp)
    os.remove(fifo_fp)
    fp.close()
    os.remove(pid_file)

