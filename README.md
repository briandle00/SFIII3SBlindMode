# SFIII3SBlindMode

![Logo](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/277/435/datas/gallery.jpg)

[![GitHub issues](https://img.shields.io/github/issues/briandle00/SFIII3SBlindMode)](https://github.com/briandle00/SFIII3SBlindMode/issues)
[![GitHub forks](https://img.shields.io/github/forks/briandle00/SFIII3SBlindMode)](https://github.com/briandle00/SFIII3SBlindMode/network)
[![GitHub stars](https://img.shields.io/github/stars/briandle00/SFIII3SBlindMode)](https://github.com/briandle00/SFIII3SBlindMode/stargazers)

A blind accessibility mode for the classic 2D fighter Street Fighter III: 3rd Strike.

Created for the Liquid Hacks 2020 hackathon by Phi-Long Bui, Kevin Dai, Brian Le, and Riley Okumura.

[Watch the demo here!](https://www.youtube.com/watch?v=5ECQ7Zk1cZA&feature=emb_title)

## History and Inspiration
Street Fighter III: 3rd Strike is one of the most influential fighting games of all time. It still stands up today against modern games, and was the game behind the well-known Evo Moment 37.

[![Evo Moment 37](https://github.com/briandle00/SFIII3SBlindMode/blob/main/media/37.jpg?raw=true)](https://www.youtube.com/watch?v=JzS96auqau0)

Games today often utilize stereo sound for immersion, but why not take sound further and provide information to the vision impaired? With inspiration from 
novriltataki, we have created a prototype of this idea using FBNeo, the main emulator used for netplay by today's 3rd Strike community.

[![Novriltataki Blind Mode Prototype](https://github.com/briandle00/SFIII3SBlindMode/blob/main/media/novriltataki.jpg?raw=true)](https://www.youtube.com/watch?v=Oxq3RKKolwY)

Some central ideas from the video include:

> "While fighting games have many useful sounds that indicate what is going on, **most of the information is presented visually.** By **converting the visual information to audio,** blind players will be able to grasp what's going on a lot better."

> If we apply the **Pareto Principle** to solve this problem, we can assume that **20% of visual info holds 80% of overall importance,** and the other 80% of visual info only adds 20% importance. Based on our knowledge of fighting games, we think that this crucial 20% is **the position of your character on the screen in relation to the opponent.**

## Setup Instructions

1. Clone this repository onto your desktop, then change directory to the file location in a shell and run ``pip3 install -r requirements.txt``.

    1. Alternatively, run ``pip install soundfile``, ``pip install aupyom``, and ``pip install pynput`` to install the necessary dependencies for the Python scripts.

2. Download [Fightcade](https://www.fightcade.com/), a packaged emulator and netplay program with built-in community channels, and create an account.

3. Place ``sfiii3.zip`` and ``sfiii3nr1.zip`` ROM files into your ``Fightcade/ROMs/FBNeo Roms`` folder. Do not unzip them. You're on your own to find these.
    
    1. These are generic setup instructions for setting up Street Fighter III: 3rd Strike on Fightcade. Other resources to set this up can be found online as well.
    
4. Place ``sfiiiblind.lua``, ``sfiiiblind.py``, and ``soundAdjust.py`` into ``Fightcade\emulator\fbneo``.

5. Upon launching Street Fighter III: 3rd Strike on either Fightcade1.exe or Fightcade2.exe, the FBNeo emulator will launch. In the top right, you can access Lua scripting in the menu below by following ``Game > Lua Scripting > New Lua Scripting...``.

![Lua Part 1](https://github.com/briandle00/SFIII3SBlindMode/blob/main/media/lua1.png?raw=true)

6. Click on the ``Browse...`` button and select ``sfiiiblind.lua`` and click Run.

![Lua Part 2](https://github.com/briandle00/SFIII3SBlindMode/blob/main/media/lua2.PNG?raw=true)

7. Run ``sfiiiblind.py``. Expect to wait about a minute for the sounds to be ready and processed.

8. Start playing Street Fighter III: 3rd Strike! Game information will be sent from the Lua script to the Python script and play sounds for you as you play.

    1. The metronome playing tracks your opponent. The closer they are, the higher the tempo, and the farther they are, the lower the tempo.
    
    2. There is a sound that plays whenever your opponent jumps. It reacts to their exact height on the screen, reacting to differing jump heights, juggles, anti-airs, etc.
    
    3. Whenever a crossover occurs, sound will switch to track your opponent. If the opponent is on the left, sound will play on the left, and if the opponent is on the right, sound will play on the right.
    
    4. A higher pitched melody plays when you cross the 75%, 50%, and 25% health thresholds. A lower pitched melody is played for the same thresholds for your opponent. The longer the melody, the lower the health.
