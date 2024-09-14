import curses
from curses import wrapper
import time
import random

#curses module of python is necesarry for this wpm test implementation
#stdscr is there to manage our output screen on terminal
#.clean will do the needful of cleaning
def start_screen(stdscr):
	stdscr.clear()
    #input message for user
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
    #if we dont use .getkey func then our code will end abruptly after printing the msg
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    #target text will be provided by us in a separate text file in my same folder
	stdscr.addstr(target)
    #(1,0) basically gives it the coordinate on the terminal window
	stdscr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):#Enumerate in Python is used to loop over an iterable and automatically provide an index for each item
		correct_char = target[i]#this line checks what the correct char should have been
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)#if wrong char is selected then it prints coloue 2 which is red

		stdscr.addstr(0, i, char, color)#if char is correct then continue on green colour 

def load_text():
    #this function will provide a random text from a .txt file present in our folder
	with open("text.txt", "r") as f:#this file should be on the same folder
		lines = f.readlines()
		return random.choice(lines).strip()#strip will remove \n bcz we dont want users to type such special char

def wpm_test(stdscr):
    #this function is used to calculate the typing speed of the user 
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()#find the start time using this function
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
        #we need max 1 else at starting we have time_elas=0 so our div will be invalid
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        #for converting to minutes that divide by 5 is necessary
		stdscr.clear()
        #this line will be for our dislpay of wpm for our user
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break
            #to handle the throw exception case we need to add the try and except 
		try:
			key = stdscr.getkey()
		except:
			continue
            #if user presses Esc then program should stop else user plays one more time
		if ord(key) == 27:
			break
            #another edge case is when user types backspace to correct his mistake 
            #backspace is represented by three different symbols in different operating system
		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
                #pop function will remove the last typed char upon doing backspace
		elif len(current_text) < len(target_text):
            #another edge case is that our current txt should not exceed target text length
			current_text.append(key)


def main(stdscr):
    #these three colour pairs will be our terminal display
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #green for correct input by user
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #red for any char that is wrong
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
     #white for initial required text

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
        #for text to come in the next line we specify (2,0)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = stdscr.getkey()
		#if esc given by user then break
		if ord(key) == 27:
			break

wrapper(main)