from pynput import keyboard as kb
from aupyom import Sampler, Sound
from soundAdjust import bpm_adjustment, pitch_adjustment
from queue import Empty
from threading import Thread
import numpy
import time
import sounddevice as sd
import soundfile as sf

player = True #bool to track which player is hovered p1[True], p2[False]
first_space = True #bool to track first space input
sideSelect = True #bool to keep track of if the game is in sideSelect
sideBool = True #bool to keep track of stereo and enemy; left[True], right[False]

def main(soundList):
    global player 
    global first_space
    global sideSelect
    global sideBool
    #common terms
    #player1 = p1
    #player2 = p2

    #declare variables for sound files
    p1_select_sound = soundList[0]
    p2_select_sound = soundList[1]
    player_ok_sound = soundList[2]
    bpm_sound = soundList[3]
    pitch_sound = soundList[4]
    hp_enemy_1 = soundList[5]
    hp_enemy_2 = soundList[6]
    hp_enemy_3 = soundList[7]
    hp_self_1 = soundList[8]
    hp_self_2 = soundList[9]
    hp_self_3 = soundList[10]


    #open sound mixer(library:aupyom [https://github.com/pierre-rouanet/aupyom])
    sampler = Sampler()

    #declare and play instructions for side selection
    #side selection (p1[left] or p2[right])
    
    # Extract data and sampling rate from file
    data, fs = sf.read("sounds/instructions.wav", dtype='float32')  
    sd.play(data, fs) 

    
    #player = True #bool to track which player is hovered p1[True], p2[False]
    #first_space = True #bool to track first space input
    #sideSelect = True #bool to keep track of if the game is in sideSelect
    def on_press(key):
        global player 
        global first_space
        global sideSelect
        global sideBool
        if sideSelect and key == kb.Key.space: #if space is pressed swap player
            player = not player
            if first_space: #handle space during instructions
                sd.stop()
                sampler.play(p2_select_sound)
                first_space = False
                sideBool = False
            elif player: #hovering over p1
                if p2_select_sound in sampler.sounds:
                    sampler.remove(p2_select_sound)
                sideBool = True
                sampler.play(p1_select_sound)
            elif not player: #hovering over p2
                if p1_select_sound in sampler.sounds:
                    sampler.remove(p1_select_sound)
                sideBool = False
                sampler.play(p2_select_sound)
        elif sideSelect and key == kb.Key.enter: #if enter is pressed confirm selection
            sideSelect = False
            sd.stop()
            if player and p1_select_sound in sampler.sounds: #confirmed player1
                sampler.remove(p1_select_sound)
            elif not player and p2_select_sound in sampler.sounds: #confirmed player2
                sampler.remove(p2_select_sound)
            sampler.play(player_ok_sound)
        elif key == kb.Key.esc: #handle esc key as script ending
            listener.stop
            return
        else: #other keys are ignored
            pass

    listener = kb.Listener(on_press=on_press)
    listener.start()

    #loop to keep script at side selection until side is confirmed
    while(sideSelect):
        time.sleep(.25)

    #open file for input
    filename = 'buffer.txt' #match file name 
    inputFile = open(filename, "r")

    #loop to wait until round begins
    line = inputFile.readline()
    while(not line):
        line = inputFile.readline()
    
    #expected data format: [p1xpos, p1ypos, p2xpos, p2ypos, p1hp, p2hp, gameTimer]
    data = line.strip().split()
   
    base_lateral = abs(int(data[0]) - int(data[2])) #stores starting dist between players

    #set sideBool equal to enemy side
    if player:
        sideBool = False
    else:
        sideBool = True

    #begin playing base bpm track
    sampler.play(bpm_sound)
    
    prevPlayerX = -1
    prevEnemyX = -1
    prevTimer = 100 #declared to be higher than 99 
    prevPlayerHP = 160
    prevEnemyHP = 160

    #run loop for taking in new game input
    while(True):

        #expected line format: "p1xpos p1ypos p2xpos p2ypos p1hp p2hp gameTimer"
        line = inputFile.readline()
        if line:
            #expected data format: [p1xpos, p1ypos, p2xpos, p2ypos, p1hp, p2hp, gameTimer]
            data = line.strip().split()

            #declare variables based on previous player selection
            if player == True:
                playerXpos = int(data[0])
                playerYpos = int(data[1])
                enemyXpos = int(data[2])
                enemyYpos = int(data[3])
                playerHealth = int(data[4])
                enemyHealth = int(data[5])
            elif player == False:
                enemyXpos = int(data[0])
                enemyYpos = int(data[1])
                playerXpos = int(data[2])
                playerYpos = int(data[3])
                playerHealth = int(data[4])
                enemyHealth = int(data[5])

            gameTimer = int(data[6])
            
            #checks to see if round or match has restarted
            if prevTimer < 99 and gameTimer == 99:
                if player == True:
                    sideBool = False
                elif player == False:
                    sideBool = True
                if bpm_sound in sampler.sounds:
                    sampler.remove(bpm_sound)
                sampler.play(bpm_sound)
                
            #examine x position for side, change stereo side
            if sideBool == False and playerXpos > enemyXpos: #enemy crossed to the left
                sideBool = True
            elif sideBool == True and playerXpos < enemyXpos: #enemy crossed to the right
                sideBool = False
                
            #calculate lateral difference, adjust bpm
            lateral_dist = abs(playerXpos - enemyXpos)
            if (sideBool):
              bpm_adjustment(bpm_sound, lateral_dist,base_lateral)
            else:
              bpm_adjustment(bpm_sound, lateral_dist, base_lateral)

            #calculate vertical difference, adjust pitch
            if enemyYpos > 0 and not pitch_sound in sampler.sounds:
                sampler.play(pitch_sound)
        
            pitch_adjustment(pitch_sound, enemyYpos)
            
            #stop playing pitch sound when player lands
            if enemyYpos == 0 and pitch_sound in sampler.sounds:
                sampler.remove(pitch_sound)
           

            #play hp sounds if player or enemy crosses a threshold
            if (prevPlayerHP > 120 and playerHealth <= 120): #Player below 75%
                sampler.play(hp_self_1) 
            elif (prevPlayerHP > 80 and playerHealth <= 80): #Player below 50%
                sampler.play(hp_self_2)
            elif (prevPlayerHP > 40 and playerHealth <= 40): #Player below 25%
                sampler.play(hp_self_3)
            if (prevEnemyHP > 120 and enemyHealth <= 120): #Player below 75%
                sampler.play(hp_enemy_1)
            elif (prevEnemyHP > 80 and enemyHealth <= 80): #Player below 50%
                sampler.play(hp_enemy_2)
            elif (prevEnemyHP > 40 and enemyHealth <= 40): #Player below 25%
                sampler.play(hp_enemy_3)
            
            #examine x position for stage interval
            center = (base_lateral / 2)
            leftMid = (center / 2)
            rightMid = (center + (center/2))

            if (prevPlayerX < center < playerXpos or
                playerXpos > center > prevPlayerX):
              pass # play sound bite
            elif (prevPlayerX < leftMid < playerXpos or
                playerXpos > leftMid > prevPlayerX):
              pass # play sound bite
            elif (prevPlayerX < rightMid < playerXpos or 
              playerXpos > rightMid > prevPlayerX):
              pass # play sound bite
            else:
                pass

            #store previous player X positions for stage interval use
            prevPlayerX = playerXpos
            # prevEnemyX = enemyXpos

            #store prev gameTimer
            prevTimer = gameTimer
            #store prev player healths
            prevPlayerHP = playerHealth
            prevEnemyHP = enemyHealth

        else: #handle no new line of input
            pass

def refactoredRun(self): #adjusted aupyom's Sampler.run to use 2 channels
    """ Play loop, i.e. send all sound chunk by chunk to the soundcard. """
    self.running = True

    def chunks_producer():
        while self.running:
            self.chunks.put(self.next_chunks())

    t = Thread(target=chunks_producer)
    t.start()

    with self.BackendStream(samplerate=self.sr, channels=2) as stream:
        while self.running:
            try:
                stream.write(self.chunks.get(1))  # timeout so stream.write() thread can exit
            except Empty:
                self.running = False  # let play_thread exit

def refactored_next_chunks(self):
    global sideBool
    """ Gets a new chunk from all played sound and mix them together. """
    with self.chunk_available:
        while True:
            playing_sounds = [s for s in self.sounds if s.playing]

            chunks = []
            for s in playing_sounds:
                try:
                    chunks.append(next(s.chunks))
                except StopIteration:
                    s.playing = False
                    self.sounds.remove(s)
                    #self.is_done.set()  # sound was played, release is_done to end the wait in play

            if chunks:
                break

            self.chunk_available.wait()

        a = numpy.mean(chunks, axis=0)
        store = len(a)
        a = numpy.expand_dims(a, axis = 0)

        b = numpy.zeros((1, store), dtype=numpy.float32)
        if sideBool:
            a = numpy.append(a,b,axis=0)
        else:
            a = numpy.append(b,a,axis=0)

       
        return numpy.ascontiguousarray(a.transpose(), dtype=numpy.float32)
    
def soundDeclaration():
    Sampler.run = refactoredRun
    Sampler.next_chunks = refactored_next_chunks
    output = []
    #sound file declarations (expecting 20-30 second processing delay)
    #change file strings to match file name
    #Declare side select sounds
    output.append(Sound.from_file("sounds/player1.wav")) 
    output.append(Sound.from_file("sounds/player2.wav")) 
    output.append(Sound.from_file("sounds/confirm.wav")) 
    
    #Declare bpm sounds
    output.append(Sound.from_file("sounds/bpm.wav")) 

    #Declare pitch sounds
    output.append(Sound.from_file("sounds/pitch.wav")) 

    #Declare hp indicators
    output.append(Sound.from_file("sounds/hp_enemy_1.wav")) 
    output.append(Sound.from_file("sounds/hp_enemy_2.wav")) 
    output.append(Sound.from_file("sounds/hp_enemy_3.wav")) 
    output.append(Sound.from_file("sounds/hp_self_1.wav")) 
    output.append(Sound.from_file("sounds/hp_self_2.wav")) 
    output.append(Sound.from_file("sounds/hp_self_3.wav")) 
        
    #DECLARE STAGE INTERVAL HERE#
    
    print("finished loading")
    return output


if __name__ == "__main__":
    #opens file to ensure that text file is empty before lua script is run
    open('buffer.txt', 'w').close() #match file name

    soundList = soundDeclaration()
    main(soundList)
