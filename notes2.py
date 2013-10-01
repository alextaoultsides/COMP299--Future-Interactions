import winsound
import time

#every note including acidentals with frequencey. 
#in the same dicionary have A:23 B: 24 C:25 Df:38
#for each note in song, dictiony.get(note )
#songName = [A3, B3, C3]
#songName[0][1] prints 3
#play the frequency dict.get(songName[i]^[1]) or dict[songName[i]^[1]]

#---Dictionaries------
NOTES_2_FREQ = {' ':37, 'D3':147, 'E3':165, 'F3':174, 'G3':196, 'A3':220, 'C4':261, 'D4':293, 'E4':329, 'F4':349, 'G4':391, 'A4':440, 'C5':523}
BEET_2_MILISEC = {'W':2000, 'H':1000, 'Q':500, 'E':250}
#---Songs---

FrereJaques = ['C4', 'D4', 'E4', 'C4', 'C4', 'D4', 'E4', 'C4', 'E4', 'F4', 'G4', 'E4', 'F4', 'G4', ' ', 'G4', 'A4', 'G4', 'F4', 'E4', 'C4','G4', 'A4', 'G4', 'F4', 'E4', 'C4', 'C4', 'G4', 'C4', ' ', 'C4', 'G4', 'C4' ]

MaryLittleLamb = ['A4', 'G4', 'F4', 'G4', 'A4', 'A4', 'A4', 'G4', 'G4', 'G4', 'A4', 'C5', 'C5', ' ', 'A4', 'G4', 'F4', 'G4', 'A4', 'A4', 'A4', 'A4', 'G4', 'G4', 'A4', 'G4', 'F4']



SongOfStorms = ['D3', 'F3', 'D4','D3', 'F3', 'D4', 'E4', 'F4', 'E4', 'F4', 'E4', 'C4', 'A3', 'A3', 'D3', 'D3', 'F3', 'A3', 'A3', 'D3', 'F3', 'G3', 'E3']

#TwinkleStar['C4', 'C4', 'G4', 'G4']
#-------------------------------------------------------------------

def playSong(song):
    time = 1000
    note = 0 #index number in song's list of note names
    for note in song:
        freq = NOTES_2_FREQ.get(note)
        winsound.Beep(freq, time)
        time = time - 50

def main():
    
    print('''\nSong Codes (use quotes)''')
    print('''-----------------------------------''')
    print('''Frere` Jaques -- "fj"''')
    print('''Mary Had a Little Lamb -- "mll" ''')
    print('''Song of Storms -- "sos" ''')
    print('''---------------------------------------------\n''')
    
    getSong = input("enter song code: ", )
    
    if getSong == "fj":
        playSong(FrereJaques)
    elif getSong == "mll":
        playSong(MaryLittleLamb)
    elif getSong == "sos":
        playSong(SongOfStorms)
    else:
        print ("no song code")
    
    
    
main()
    