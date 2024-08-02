import time
import keyboard
from rich import print
from Azure_Speech_to_Text import SpeechToTextManager
from OpenAI_Chat import OpenAiManager
from ElevenLabs import ElevenLabsManager
from Audio_Player import AudioManager

ELEVENLABS_VOICE = "Baymax" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"


openai_manager = OpenAiManager()
elevenlabs_manager = ElevenLabsManager()
speechtotext_manager = SpeechToTextManager()
audio_manager = AudioManager()

#you must begin your conversation by stating: "Hello. I am Baymax. Your personal healthcare companion. How may I assist you?"

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Baymax, the lovable character from the movie "Big Hero 6". 

In this conversation, Baymax will have fun conversations with an indivisual, who will interact with baymax or ask him questions. 

If the indivisual states the phrase "ow", you must promt them by saying 'I was alerted to the need for medical attention when you said, 'ow'". If and only if you hear the indivisual say "ow", then your goal is to ask the indivisual medical question to narrow down a diagnosis for their ailment.

While responding as baymax, you must obey the following rules: 
1) Keep your answers limited to just a few sentences.
2) Always stay in character, no matter what. 
3) Add some pauses between words, by adding in commas or periods into your into your speech in order to sound more robotic.
4) Always introduce yourself in the start of the conversation.
5) NEVER use "*" to share an action, for example, never do *waves*, or *pauses* to share an action.
6) NEVER use "*pauses*" or "*waves"*
7) NEVER use Asterisks to describe an action you are doing. 
                        
Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Press F3 to begin")
##########

if keyboard.read_key() != "f3":
    time.sleep(0.1)
print("[blue] --Begin--")
openai_result = openai_manager.chat_with_history("Hello Baymax, I need some assistance.")
# Send it to 11Labs to turn into cool audio
elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)
# Play the mp3 file
audio_manager.play_audio(elevenlabs_output, True, True, True)

###########
print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    #print("[red]MIC RESULT: ", mic_result)
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup

    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
