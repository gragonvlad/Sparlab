# Sparlab

What is Sparlab?

Sparlab is an application with built-in features made to give fighting gamers increased control of their training experience.

Does Sparlab give you frame perfect timing of inputs?

No, but you can customize time intervals and adjust Sparlab's frames per second to get you your desired result.

What games can Sparlab be used for?

Fighting games. Examples of franchised games include Street Fighter, Mortal Kombat, Soul Calibur, Tekken, Super Mario Bros, and many more!

How are inputs recorded?

From the notation entry box, Pre-defined notations are converted to their corresponding joy functions and game functions that are sent into a virtual controller when the user presses their corresponding hotkeys or presses play.
Joy Functions are basic button/analog movements off of an XBOX 360 controller (B button down, A button up,
Left Analog Up-Right, Just-frame, etc.). Game Functions are made up of a string of inputs, with additional complexity added to make the functions more useful for certain games. For example, in Tekken, you can name a few of your functions Up-right, Down-left, Left-punch, Electric Wind God Fist, etc. For Street Fighter, you can name them Hadoken, Shoryuken, etc.

Do I have to play with an XBOX 360 controller for Sparlab to work?

No, your character in the game cannot tell the difference between different controllers, as Steam converts all detected input into Xinput. For the purposes of creating action scripts for specific joysticks, we want Sparlab to have multiple virtual joystick APIs as opposed to JUST an XBOX 360 joystick.

What makes Sparlab different from other tools such as TekkenBot and AutoHotkey?

Sparlab is made specifically for training purposes, where AutoHotkey is commonly used to input keyboard shortcuts during competition. It is also easy to plugin and adapt Sparlab to any fighting game because it operates a virtual joystick rather than injecting data into frames. You do not have to be a hacker to use Sparlab.

Why makes Sparlab better than the built-in training tools in fighting games?

In most games, bots have to be re-recorded every training session. Using the recording feature to create
complicated setups takes up a lot of time, as inputs have to be placed very precisely. They also have to be re-recorded every time a gamer trains with a different character or game. With Sparlab, you can save setups in-app or quickly upload setups to the app for quick implementation and re-use. You can also use those same scripts for other games as well.

What platforms/consoles does Sparlab work on?

PC (64-bit) on Steam. Sparlab has only been tested on a Windows 10 OS, but it should work on Linux, Mac OS, and other PC systems. Our goal is for Sparlab to be adapted for other consoles and platforms as well.

What features will Sparlab have in the future?

That is for our users to suggest!


Developers

Python version: 3.6.5

This is an open-source project with a general public license. This gives you the freedom to make your own changes and distribute your own copies of Sparlab. 

Contributing: if you submit a pull request and it is accepted, your Github username will be added to the CONTRIBUTORS.txt file on the master branch. 

Objective: build a tool for fighting gamers to become better fighters without hacking/injecting into frame data. 

Help needed for: built-in Settings & Functions menus, built-in virtual gamepads besides virtual xbox 360 controller (BotController), auto updater (updater.py), joystick recorders that convert input to notation, notation cursor to show what notation is being played in the script (while playing), object detection feature that can accurately predict the X,Y coordinates of each player (for direction detection, hit-boxes, etc.) using ONLY pixel data, health bar readers using ONLY pixel data, and more. Feel free to think of your own ideas for improving Sparlab!  


Build/Distrib. 

Make sure you have all packages installed, including cx_Freeze. 
In powershell inside the __main__ directory, type 'python .\setup.py build' for building executable and 'python .\setup.py bdist_msi' for distributable. 


Virtual Bus Driver Install 
1) Verify that you have Microsoft Visual Studio Community 2017 installed. -https://visualstudio.microsoft.com/downloads/

2) Open admin command prompt, enter 'cd *PATH TO drivers INSERTED HERE*'
To install: 'devcon.exe install ScpVBus.inf Root\ScpVBus'
To uninstall:'devcon.exe remove Root\ScpVBus'


Link to built & signed application download: https://www.umensch.com/downloads/


For more information, email john.ward@umensch.com 

