import Leap
import sys

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import os
import pygame

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class applistener(Leap.Listener):
    
    def on_init(self,controller):#Initializes pygame and display surface
        pygame.init()
        x = y = 0
        self.horiz = 1280 #Display horizontal pixels
        self.vert = 720   #Display vertical pixels
        self.display_surf = pygame.display.set_mode((self.horiz,self.vert), pygame.HWSURFACE) #sets hardware surface
        self._running = True 
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
    def on_loop(self):
        print "hello"
    #def on_render(self,x,y):
    #    pygame.draw.circle(self.display_surf,(0,255,0),(x, y), 10)
    #    pygame.display.flip()
    
    #def on_cleanup(self):
    #    pygame.quit()
    
    
    def on_frame(self,controller):#Leap motion loop listens for any interaction with Leap Motion device

        frame = controller.frame()  
        event = pygame.event.poll() #polls for any user input events
        
            
        
        
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
                    
                    pygame.draw.circle(self.display_surf,(0,255,0),(tipx,-(tipy)), 10)#prints a circle on the screen
                    print str(tipx) + " " + str(tipy)
                    
                    
        for gesture in frame.gestures(): #reads in a swipe gesture
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print self.state_string(gesture.state)
                #print swipe.start_position
                #print swipe.direction
                #print swipe.position
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
    applistener = applistener()
    controller.add_listener(applistener)
    
    print "Press Enter to quit..."
    sys.stdin.readline()
    
    controller.remove_listener(applistener)
    
    
if __name__ == "__main__":
    main()