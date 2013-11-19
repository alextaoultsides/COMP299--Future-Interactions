import Leap
import sys
import winsound
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import os
import pygame
import math
from pygame.locals import *

class sounder:
    def __init__(self):
        self.a = 0 
        
    def player(self,freq_l):
        bits = 16
        #the number of channels specified here is NOT 
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
        
        pygame.mixer.pre_init(44100, -bits, 2)
        #pygame.init()
        #_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        
        duration = .05          # in seconds
        #freqency for the left speaker
        frequency_l = 880
        #frequency for the right speaker
        frequency_r = 550
        
        #this sounds totally different coming out of a laptop versus coming out of headphones
        
        sample_rate = 44100
        
        n_samples = int(round(duration*sample_rate))
        
        #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
        buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
        max_sample = 2**(bits - 1) - 1
        
        for s in range(n_samples):
            t = float(s)/sample_rate    # time in seconds
        
            #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
            buf[s][0] = int(round(max_sample*math.sin(2*math.pi*freq_l*t)))        # left
            #buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*freq_l*t)))    # right
            
        sound = pygame.sndarray.make_sound(buf)
        #play once, then loop forever
        sound.play(loops = 1)

class applistener(Leap.Listener):
    
    def on_init(self,controller):#Initializes pygame and display surface
        pygame.init()
        x = y = 0
        self.horiz = 640 #Display horizontal pixels
        self.vert = 480  #Display vertical pixels
        self.display_surf = pygame.display.set_mode((self.horiz,self.vert), pygame.HWSURFACE) #sets hardware surface
        
        self._running = True 
        self.sounders = sounder()
        #self._image_surf = pygame.image.load("myimage.jpg").convert()
        print "Connected"
        
    def on_connect(self,controller):
        print "Connected"
        
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        
    def on_disconnect(self,controller):
        print "Disconnected"
        
    def on_exit(self,controller):
        print "Exited"
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        return self._running
    def on_loop(self, end):
        print "hello"
        
        if self.running == False:
            return False
        else:
            return True
    def exits(self):
        return False
    #def on_render(self,x,y):
    #    pygame.draw.circle(self.display_surf,(0,255,0),(x, y), 10)
    #    pygame.display.flip()
    
    def on_cleanup(self):
        if self.on_loop == True:
            return False
    
    
    def on_frame(self,controller):#Leap motion loop listens for any interaction with Leap Motion device

        frame = controller.frame()  
         #polls for any user input events
        
            
        #print pygame.display.list_modes
        
        if not frame.hands.is_empty:#Checks for hands or pointables over Leap
            
            hand = frame.hands[0] # fingers on first hand
            hand2 = frame.hands[1]# fingers on second hand
            
            fingers1 = hand.fingers # list of fingers from first hand
            fingers2 = hand2.fingers # list of fingers from second hand
            if not frame.fingers.is_empty:#checks fingers
                if not fingers1.is_empty: #checks if fingers from first hand are present
                    self.display_surf.fill((0,0,0)) #fills the display surface with black
                    tipx = int(fingers1[0].tip_position[0]) #takes the x coordinate of the first finger
                    tipy = int(fingers1[0].tip_position[1]) #takes the y coordinate of the second finger
                    
                    tipx = tipx + (self.horiz / 2)# math to map x coordinate from Leap to the display surface
                    tipy = tipy - self.vert #same as above except for the y coordinate
                    
                    pygame.draw.circle(self.display_surf,(0,255,0),(tipx ,-(tipy) ), 10)#prints a circle on the screen
                    percentage = float(tipy) / float(self.horiz)
                    #print percentage
                    self.sounders.player(3200.0 * -(percentage))
                    print 3200.0 * -(percentage)
        """
        event = pygame.event.poll()     
        if event.type is pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)
    
            if event.key == pygame.K_ESCAPE:
                print "shit"
                self.running == False
        """
        for gesture in frame.gestures(): #reads in a swipe gesture
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print self.state_string(gesture.state)
                #print swipe.start_position
                #print swipe.direction
                #print swipe.position
                self.on_cleanup()
        pygame.display.flip()
        
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
        

 

def main():
    
    
    
    controller = Leap.Controller()
    applistener1 = applistener()
    controller.add_listener(applistener1)
    
    print "Press Enter to quit..."
   
    sys.stdin.readline()
    
    
    
    controller.remove_listener(applistener1)
    
    
    
    
if __name__ == "__main__":
    main()