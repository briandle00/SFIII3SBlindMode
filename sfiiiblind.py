from pynput import keyboard as kb
from aupyom import Sampler, Sound
from soundAdjust import bpm_adjustment, pitch_adjustment, removeAndReset

player = True #bool to track which player is hovered p1[True], p2[False]
first_space = True #bool to track first space input
sideSelect = True #bool to keep track of if the game is in sideSelect
def main(soundList):
    global player 
    global first_space
    global sideSelect
    #common terms
    #player1 = p1
    #player2 = p2
    
    #reset pitch and time-scale of each sound file 
    for sound in soundList:
        sound.stretch_factor = 1.0
        sound.pitch_shift = 0

    #declare variables for sound files
    select_sound = soundList[0]
    p1_select_sound = soundList[1]
    p2_select_sound = soundList[2]
    player_ok_sound = soundList[3]
    bpm_sound_right = soundList[4]
    bpm_sound_left = soundList[5]
    pitch_sound_left = soundList[6]
    pitch_sound_right = soundList[7]


    #open sound mixer(library:aupyom [https://github.com/pierre-rouanet/aupyom])
    sampler = Sampler()


    #side selection (p1[left] or p2[right])
    sampler.play(select_sound)
    player = True #bool to track which player is hovered p1[True], p2[False]
    first_space = True #bool to track first space input
    sideSelect = True #bool to keep track of if the game is in sideSelect
    def on_press(key):
        global player 
        global first_space
        global sideSelect
        if sideSelect and key == kb.Key.space: #if space is pressed swap player
            player = not player
            if first_space: #handle space during instructions
                sampler.remove(select_sound)
                sampler.play(p2_select_sound)
                first_space = False
            elif player: #hovering over p1
                sampler.remove(p2_select_sound)
                sampler.play(p1_select_sound)
            elif not player: #hovering over p2
                sampler.remove(p1_select_sound)
                sa
                mpler.play(p2_select_sound)
        elif sideSelect and key == kb.Key.enter: #if enter is pressed confirm selection
            sideSelect = False
            if first_space: #handle enter during instructions
                sampler.remove(select_sound)
            elif player: #confirmed player1 
                sampler.remove(p1_select_sound)
            elif not player: #confirmed player2
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
        pass
    #loop to wait until okay sound finishes playing then remove sound
    # while(player_ok_sound.playing):
    #     pass
    #sampler.remove(player_ok_sound)


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
    sideBool = True #bool to keep track of stereo; left[True], right[False]

    #begin playing base bpm track with correct side
    if player == True:
        sampler.play(bpm_sound_right)
        sideBool = True
    elif player == False:
        sampler.play(bpm_sound_left)
        sideBool = False
    
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
                    if bpm_sound_left in sampler.sounds:
                        removeAndReset(bpm_sound_left,sampler)
                    sampler.play(bpm_sound_right)
                    sideBool = True
                elif player == False:
                    if bpm_sound_right in sampler.sounds:
                        removeAndReset(bpm_sound_right,sampler)
                    sampler.play(bpm_sound_left)
                    sideBool = False
                
            #examine x position for side, change stereo side
            if sideBool == False and playerXpos < enemyXpos: #enemy to the left
                removeAndReset(bpm_sound_right, sampler)
                sampler.play(bpm_sound_left)
                if (pitch_sound_right in sampler.sounds):
                    removeAndReset(pitch_sound_right,sampler)
                    pitch_adjustment(pitch_sound_left, enemyYpos)
                    sampler.play(pitch_sound_left)
                sideBool = True
            elif sideBool == True and playerXpos > enemyXpos: #enemy to the right
                removeAndReset(bpm_sound_left, sampler)
                sampler.play(bpm_sound_right)
                if (pitch_sound_left in sampler.sounds):
                    removeAndReset(pitch_sound_left,sampler)
                    pitch_adjustment(pitch_sound_right, enemyYpos)
                    sampler.play(pitch_sound_right)
                sideBool = False
                
            #calculate lateral difference, adjust bpm
            lateral_dist = abs(playerXpos - enemyXpos)
            if (sideBool):
              bpm_adjustment(bpm_sound_left, lateral_dist,base_lateral)
            else:
              bpm_adjustment(bpm_sound_right, lateral_dist, base_lateral)

            #calculate vertical difference, adjust pitch
            if sideBool and enemyYpos > 0 and not pitch_sound_left in sampler.sounds:
                sampler.play(pitch_sound_left)
            elif not sideBool and enemyYpos > 0 and not  pitch_sound_right in sampler.sounds:
                sampler.play(pitch_sound_right)
            if (sideBool):
              pitch_adjustment(pitch_sound_left, enemyYpos)
            else:
              pitch_adjustment(pitch_sound_right, enemyYpos)

            #play hp sounds if player or enemy crosses a threshold
            if (prevPlayerHP > 120 and playerHealth <= 120): #Player below 75%
                pass #play sound bite
            elif (prevPlayerHP > 80 and playerHealth <= 80): #Player below 50%
                pass #play sound bite
            elif (prevPlayerHP > 40 and playerHealth <= 40): #Player below 25%
                pass #play sound bite
            if (prevEnemyHP > 120 and enemyHealth <= 120): #Player below 75%
                pass #play sound bite
            elif (prevEnemyHP > 80 and enemyHealth <= 80): #Player below 50%
                pass #play sound bite
            elif (prevEnemyHP > 40 and enemyHealth <= 40): #Player below 25%
                pass #play sound bite
            
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

def soundDeclaration():
    output = []
     #sound file declarations (expecting 20-30 second processing delay)'
    output.append(Sound.from_file("initial.wav"))#change to match file name
    output.append(Sound.from_file("p1.wav")) #change to match file name
    output.append(Sound.from_file("p2.wav")) #change to match file name
    output.append(Sound.from_file("ok.wav")) #change to match file name
    output.append(Sound.from_file("bpm_right.wav")) #change to match file name
    output.append(Sound.from_file("bpm_left.wav")) #change to match file name
    output.append(Sound.from_file("pitch_left.wav")) #change to match file name
    output.append(Sound.from_file("pitch_left.wav")) #change to match file name

    #DECLARE HP SOUNDS HERE#
    #DECLARE STAGE INTERVAL HERE#

    return output


if __name__ == "__main__":
    #opens file to ensure that text file is empty before lua script is run
    #open('buffer.txt', 'w').close() #match file name
    
    soundList = soundDeclaration()
    main(soundList)
    #on end prompt to hit enter to replay
