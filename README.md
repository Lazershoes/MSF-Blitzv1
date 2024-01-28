This script will automate blitz attacks, performing a full rotation of all your saved blitz teams. After a full rotation, it will pause for one hour to wait for the free refresh and then repeat the cycle. It works by using computer vision python module to match the sample .jpg pics in the folder to what is seen on your BlueStacks player screen. As the script requires BlueStacks as the active window, its designed to be run overnight or when you're not using your PC for anything else.

The script will not use cores or blitz energy to attack, only standard free blitz attacks. It also won't use any strategy on attacks, it just attacks the first opponent it finds. Sometimes there's a huge lag from the MSF servers to determine if you win or lose, so I baked in a 9 second delay before it clicks the Continue button. There can also be lag in finding an opponent, and this can cause the script to lose track of what it's doing. Best to watch it run a cycle just to make sure its working properly.

Steps to setup:

1. Download python 3.12. You want the windows installer for 64 bit, scroll to bottom to find it. Or MacOS.
	https://www.python.org/downloads/release/python-3120/

2. Install required python modules
	Click windows start button, type 'cmd' to bring up windows command prompt.
	type 'pip install opencv-python'
	'pip install pyautogui'
	'pip install mss'
	'pip install numpy'
	'pip install pygetwindow'

3. Install BlueStacks App
	https://www.bluestacks.com/

4. Download MSF onto your newly installed BlueStacks emulator. You will need to run it first, as it will create a newbie lvl 1 account. Then you will need to sign in with your main account.

5. Open the Blitz window and desired blitz event. Cycle the team to start at 1/49 or however many blitz teams you have setup. If you have toons spread out over multiple teams, it will skip them as eventually it will start taking blitz energy to attack. So make sure your teams are setup right so you're not overlapping characters.

6. Unzip the MSF Blitz.zip file to your Documents or wherever. Open the Blitz.py script by right-clicking and Edit with IDLE (or whatever IDE (Interactive Development Environment) you wish {Spyder, VS Code etc}). This will open a screen with all the code and variables you can change.

7. Run the script from within your IDLE editor (or any other IDE). Usually F5 in most editors, but there should also be a menu command to run the script.

8. If the script doesn't automatically switch BlueStacks over to the active window, do so at this time. After a 10 second delay or so it should now begin the blitz cycle.

9. Important Variables
	threshold = 0.9 This is the confidence computer vision uses to detect a match of the buttons on screen to the .jpg files. Too low and it could cause it to malfunction, 		but you might lower slightly if you're having issues detecting the buttons. I have a high resolution monitor, so my .jpg files are possibly larger than what you might 	have on your screen. Try 0.8 or 0.7 if it doesn't work.

	Below are the delays in seconds of how long it will take to detect and click various buttons.	

	{"template": "Find Opponent.JPG", "delay": 0.25},
        {"template": "Blitz Battle.JPG", "delay": 0.5, "check_continue": True},
        {"template": "Blitz Next Team.JPG", "delay": 0.25},

	popup_delay = 9 This is the delay in seconds of how long it takes to detect and click the Continue button after a win or loss. 
	Sometimes this can lag out from the MSF servers, 9 seconds seems to work well. It's a marathon not a race.

Happy Blitzing!

--Lazer
