import Leap
import sys
import winsound
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import os
import pygame
import re
import math
import glob
import time
from pygame.locals import *

timer = pygame.time.Clock()
playsound = USEREVENT + 1
pygame.time.set_timer(playsound, 1000)

b = False
pygame.init()
 #sets hardware surface
resolutions = pygame.display.list_modes()
horiz = resolutions[0][0] // 2
vert = resolutions[0][1] // 2

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
bits = 16
pygame.mixer.pre_init(44100, -bits, 2,64)

songs = [("",1),("E4",.9),("D4",1),("C4",1),("D4",1),("E4",1),("E4",1),("E4",2),("",1),("D4",1),("D4",1),("D4",2),("",1),("E4",1),("G4",1),("G4",2),("",1),("E4",1),("D4",1),("C4",1),("D4",1),("E4",1),("E4",1),("E4",1),("",1),("D4",1),("D4",1),("E4",1),("D4",1),("C4",1),("$",1),("",1)]
print len(songs)
gamecontinue = True
pattern = pygame.image.load("4-4pattern.png")
#print (7.0 / 32.0) *100
class beatbox:
    def __init__(self,display_surf):
	self.display_surf = display_surf
        self.sounders = sounder()
        self.i = 0
        self.score = 0
        self.beatArray = [] # stores array of pygame Rect objects
        self.beatCount = 0  # for looping through beat array
        self.b = False      # True or False triggered every second
        for i in range(4): #appends Rect object to the beat array 
            self.beatArray.append(pygame.Rect(0,0,50,50))
        
        #moves the boxes for collision testing
        self.beatArray[0].center = (int(horiz *.5),int(vert * .75))
        self.beatArray[1].center =(int(horiz*.25),int(vert *.5))
        self.beatArray[2].center =(int(horiz*.75),int(vert *.5))
        self.beatArray[3].center =(int(horiz *.5),int(vert *.25))
        
    def interaction(self,x,y):#checks for collisions and plays current note in song.
        a = 0
        
        if pygame.event.get(playsound): #triggers event every second and updates beat spot and song note
            a = pygame.time.get_ticks()
            #winsound.Beep(440,10)
            self.i += 1
            self.b = True
            if self.beatCount < 3 :
                self.beatCount += 1
                
            else:
                self.beatCount = 0
		
        if (self.beatArray[self.beatCount -1 ].collidepoint(x,y) and self.b == True):
            #pygame.draw.circle(display_surf,(255,0,0),(int(640 * .5) ,int(480 * .25)), 20 + 10)
            if songs[self.i][0] != "":
                pygame.mixer.music.load("C:pianos/Piano_mf_"+ songs[self.i][0] +".wav")#plays note using piano sample
                pygame.mixer.music.play()
                self.score += 1
                self.b = False   
        if songs[self.i][0] == "$":
            gamecontinue = False
            self.check_hit()
    def check_hit(self):#point system for accuracy
        self.perc = self.score / len(songs)
    
        print "You got " + str(self.score) + " beats out of " + str(len(songs))
        print "Percentage right " + str(self.perc * 100)
    
    def blip(self):
	b = 10
	if(self.beatCount == 0 ):
	    pygame.draw.circle(self.display_surf,(255,0,0),(int(horiz * .5) ,int(vert * .75)), 20 + b)
	    
	elif(self.beatCount == 1 ):
	    pygame.draw.circle(self.display_surf,(73,195,240),(int(horiz * .25) ,int(vert * .50)), 20 + b)
	    
	elif(self.beatCount == 2 ):
	    pygame.draw.circle(self.display_surf,(24,161,33),(int(horiz * .75) ,int(vert * .50)), 20 + b)
	    
	elif(self.beatCount == 3 ):
	    pygame.draw.circle(self.display_surf,(168,54,245),(int(horiz * .5) ,int(vert * .25)), 20 + b)     
	
                
class sounder:
    def __init__(self):
        self.a = 0
        self.i = 0
	self.num = 0
    
        
    def songPlay(self):
        
        
        pygame.mixer.music.load("C:pianos/Piano_mf_"+ songs[self.i][0] +".wav")
        pygame.mixer.music.play()
        #winsound.PlaySound("C:pianos/Piano.mf."+ songs[i][0] +".wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
        
        #time.sleep(i[1])
        #num += 1
        pygame.draw.circle(display_surf,(255,0,0),(int(640 * .5) ,int(480 * .25)), 20)
        pygame.draw.circle(display_surf,(255,0,0),(int(640 * .5) ,int(480 * .75)), 20)
        pygame.draw.circle(display_surf,(255,0,0),(int(640 * .25) ,int(480 * .50)), 20)
        pygame.draw.circle(display_surf,(255,0,0),(int(640 * .75) ,int(480 * .50)), 20)
        
    def theremin(self,freq_l):
        
        #the number of channels specified here is NOT 
        #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
        
        
        
        
        duration = .009        # in seconds
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
            
            
        sound = pygame.sndarray.make_sound(buf)
        #play once, then loop forever
        sound.play(-1)
        

class applistener(Leap.Listener):
    
    def on_init(self,controller):#Initializes pygame and display surface
        self.check = 0
        
	self.directional = {}
	self.directional['x'] = 0
	self.directional['y'] = 0
        x = y = 0
        
        
        self._running = True 
        self.sounders = sounder()
        #self._image_surf = pygame.image.load("myimage.jpg").convert()
        print "Connected"
        timerz = 0
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
    
    
    def on_cleanup(self):
        if self.on_loop == True:
            return False
    
    
    def on_frame(self,controller):#Leap motion loop listens for any interaction with Leap Motion device

        frame = controller.frame()  
         #polls for any user input events
        iBox = frame.interaction_box
            #print pygame.time.get_ticks()
            
        #print pygame.display.list_modes
        
        if not frame.hands.is_empty:#Checks for hands or pointables over Leap
            
            hand = frame.hands[0] # fingers on first hand
            hand2 = frame.hands[1]# fingers on second hand
            
            fingers1 = hand.fingers # list of fingers from first hand
            fingers2 = hand2.fingers # list of fingers from second hand
            if not frame.fingers.is_empty:#checks fingers
                if not fingers1.is_empty: #checks if fingers from first hand are present
                    
                    #print iBox.width , iBox.height
		    screenPosition = iBox.normalize_point(fingers1[0].tip_position)
		    self.directional['x'] = int(screenPosition[0] * horiz)
		    self.directional['y'] = -(vert - int(screenPosition[1] * vert))
		    #print self.directional['x'],self.directional['y']
		    
                    
        for gesture in frame.gestures(): #reads in a swipe gesture
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print self.state_string(gesture.state)
                #print swipe.start_position
                #print swipe.direction
                #print swipe.position
                self.on_cleanup()
       
        
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
def timeSig(time):
    pass

def pygameLoop(controller, listener):
    check = 0
    #beatboxes = beatbox()
    
    x = y = 0
    
    display_surf = pygame.display.set_mode((horiz,vert), pygame.HWSURFACE) #sets hardware surface
    
    beatboxes = beatbox(display_surf)
    _running = True 
    #sounders = sounder()
    #self._image_surf = pygame.image.load("myimage.jpg").convert()
    print "Connected"
    timerz = 0    
    while True:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		controller.remove_listener(listener)
		pygame.quit()
		sys.exit()
	display_surf.fill((0,0,0)) #fills the display surface with black
	display_surf.blit(pattern, ((horiz * .5) + 200, 10))
	pygame.draw.circle(display_surf,(168,54,245),(int(horiz * .5) ,int(vert * .25)), 20)
	pygame.draw.circle(display_surf,(255,0,0),(int(horiz * .5) ,int(vert * .75)), 20)
	pygame.draw.circle(display_surf,(73,195,240),(int(horiz * .25) ,int(vert * .50)), 20)
	pygame.draw.circle(display_surf,(24,161,33),(int(horiz * .75) ,int(vert * .50)), 20)
	pygame.draw.circle(display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10)#prints a circle on the screen
	#print listener.directional['x']
	#print -(listener.directional['y'])
	if gamecontinue == True:
	    beatboxes.blip()
	    beatboxes.interaction(listener.directional['x'], -(listener.directional['y']))
	    
	pygame.draw.circle(display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10)#prints a circle on the screen    
	
	pygame.display.flip()

def main():
    
    
    
    controller = Leap.Controller()
    applistener1 = applistener()
    controller.add_listener(applistener1)
    
    
    print "Press Enter to quit..."
   
    #sys.stdin.readline()
    
    pygameLoop(controller,applistener1)
    controller.remove_listener(applistener1)
    
    
    
    
if __name__ == "__main__":
    main()