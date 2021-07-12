import pyttsx3;
import os
import subprocess

def speak(textStr):
    programCommand = "pico2wave --wave=test.wav \""+textStr+"\" & mplayer test.wav"
    subprocess.check_output(programCommand, shell=True) 

def speak1(textStr):
    engine = pyttsx3.init()
    #voices = engine.getProperty('voices')
    #print("Voice : ["+str(29) +"]: "+str(voices[29]))
    #engine.setProperty('voice', voices[29].id)  # changes the voice    
    engine.setProperty('rate', 125)     # setting up new voice rate
    engine.say(textStr)
    #engine.say('मिले हो तुम हमको. बड़े नसीबों से. चुराया है मैंने. किस्मत की लकीरों से.  मिले हो तुम हमको. बड़े नसीबों से. चुराया है मैंने. किस्मत की लकीरों से.  तेरी मोहब्बत से साँसें मिली हैं. सदा रहना दिल में करीब हो के.  मिले हो तुम हमको. बड़े नसीबों से. चुराया है मैंने. किस्मत की लकीरों से.  मिले हो तुम हमको. बड़े नसीबों से. चुराया है मैंने. किस्मत की लकीरों से.  तेरी चाहतों में कितना तड़पे हैं. सावन भी कितने तुझ बिन बरसे हैं. ज़िन्दगी है मेरी सारी जो भी कमी थी. तेरे आ जाने से अब नहीं रही.  सदा ही रहना तुम, मेरे करीब होके. चुराया है मैंने, किस्मत की लकीरों से.  बाहों में तेरी अब यारा जन्नत है. मांगी खुदा से तू वो मन्नत है. तेरी वफ़ा का सहारा मिला है. तेरी ही वजह से अब मैं जिंदा हूँ.  तेरी मोहबात से ज़रा अमीर होक. चुराया है मैंने किस्मत की लकीरों से')
    engine.runAndWait()
