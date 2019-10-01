#!/usr/bin/python3

### Program Parameters ###
# VERBOSE=(1/0) : Enable outputing of verbose message of script operation to console.
# DEBUG=(1/0) : Enable debugging mode for easily checking script operations.

### Program Initialization ###
import time,os,threading
if os.getenv('VERBOSE')!=None:
	VERBOSE=int(os.getenv('VERBOSE'))
else:
	VERBOSE=0
if os.getenv('DEBUG')!=None:
	DEBUG=int(os.getenv('DEBUG'))
else:
	DEBUG=0
if VERBOSE:
	print('[INIT] Program has already loaded.')
if VERBOSE:
	print('[INIT] Verbose message displaying enabled.')
if VERBOSE and DEBUG:
	print('[INIT] Debugging mode enabled.')
if VERBOSE:
	print('[INIT] Initialize internal variables...')
H=12
Hf=0
M=0
S=1
WillResetConsole=0
GSnd='./Sounds/GeneralBell.wav'
BbSnd='./Sounds/HoursStrike.wav'
e1hSnd='./Sounds/WestmisterChimes_OnHours.wav'
NA1Snd='./Sounds/Thai_National_Anthem_-_official_version_since_2004.ogg'
NA2Snd='./Sounds/Thai_National_Anthem_-_US_Navy_Band.ogg'
if VERBOSE:
	print('[INIT] Internal variables initialized.')
if VERBOSE:
	print('[INIT] Defining internal functions...')

### Functions Definations ###
def sync():
	global H,Hf,M,S,WillResetConsole,GSnd,BbSnd,e1hSnd,NA1Snd,NA2Snd
	if VERBOSE:
		print('[SYNC] Synchronizing internal time variables...')
	if not DEBUG:
		M=time.localtime()[4]
		if M==0:
			Hf=time.localtime()[3]
			hhf()
	else:
		M=M+S
		if M==60:
			M=0
			Hf=Hf+1
			if Hf==24:
				Hf=0
			hhf()
	if VERBOSE:
		print('[SYNC] Internal time variables synchronized.')
def condition():
	global H,Hf,M,S,WillResetConsole,GSnd,BbSnd,e1hSnd,NA1Snd,NA2Snd
	if VERBOSE:
		print('[CONDITION] Checking conditions and do corresponding actions...')
	if M==0:
		if VERBOSE and not DEBUG:
			if WillResetConsole:
				WillResetConsole=0
			else:
				WillResetConsole=1
		M=0
		playsnd(e1hSnd, 'mute')
		if Hf==8:
			playsnd(NA1Snd, 'mute')
		elif Hf==18:
			playsnd(NA2Snd, 'mute')
		hourstrike()
	elif M==30:
		playsnd_thread = threading.Thread(target=playsnd, args=(GSnd, 'duck')); playsnd_thread.start()
		time.sleep(0.5)
		playsnd_thread = threading.Thread(target=playsnd, args=(GSnd, 'duck')); playsnd_thread.start()
		time.sleep(0.5)
		playsnd(GSnd, 'duck')
	elif M%10==0:
		if M<30:
			playsnd_thread = threading.Thread(target=playsnd, args=(GSnd, 'duck')); playsnd_thread.start()
			time.sleep(1)
			playsnd(GSnd, 'duck')
		else:
			playsnd_thread = threading.Thread(target=playsnd, args=(GSnd, 'duck')); playsnd_thread.start()
			time.sleep(0.5)
			playsnd(GSnd, 'duck')
	if VERBOSE:
		print('[CONDITION] Conditional action done.')
def hourstrike():
	if not DEBUG:
		c=1
		while c<=H:
			playsnd_thread = threading.Thread(target=playsnd, args=(BbSnd, 'duck')); playsnd_thread.start()
			time.sleep(2.4)
			c=c+1
	else:
			print('[HOURSTRIKE@CONDITION] Hour striked for '+str(H)+' times.')
			time.sleep(1)
def hhf():
	global H,Hf,M,S,WillResetConsole,GSnd,BbSnd,e1hSnd,NA1Snd,NA2Snd
	if Hf>12:
		H=Hf-12
	else:
		if Hf!=0:
			H=Hf
		else:
			H=12
def playsnd(sndfile, mode):
	if mode=='duck':
		os.system("PULSE_PROP='media.role=event' mplayer "+sndfile+" </dev/null >/dev/null 2>&1")
	elif mode=='mute':
		os.system("pasuspender -- mplayer -ao alsa:device=plughw=0.0 "+sndfile+" </dev/null >/dev/null 2>&1")
	else:
		os.system("PULSE_PROP='media.role=other' mplayer "+sndfile+" </dev/null >/dev/null 2>&1")

if VERBOSE:
	print('[INIT] Internal functions defined.')
if VERBOSE:
	print('[INIT] Initialization finished.')
if VERBOSE and DEBUG:
	print()

if DEBUG:
	print('[DEBUG] Set the minute time.')
	M=int(input())
	print('[DEBUG] Set the hour time.')
	Hf=int(input())
	print('[DEBUG] Set step the minute is increased.')
	S=int(input())
while True:
	if VERBOSE:
		print()
	if VERBOSE:
		print('[MAIN] Beginning of loop.')
	if VERBOSE and not DEBUG:
		print('[MAIN] Wait for '+str(60-time.localtime()[5])+' seconds to complete a minute.')
	if not DEBUG:
		time.sleep(60-time.localtime()[5])
	if VERBOSE and not DEBUG:
		print('[MAIN] Finished waiting.')
	if DEBUG:
		input('[DEBUG] Press enter to skip to next minutes-step.\n')
	sync()
	if VERBOSE and DEBUG:
		print('[INFO] Tracked internal variable for H,Hf,M values = '+str(H)+':'+str(Hf)+':'+str(M))
	condition()
	if VERBOSE:
		print('[MAIN] End of loop.')

if VERBOSE:
	print()
if VERBOSE:
	print('[MAIN] ERROR: Loop has exited.')
if VERBOSE:
	print('[MAIN] CRITICAL: Program has encountered unknwon error. The program will exit...')
exit(1)
