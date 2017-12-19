from gtts import gTTS 
import speech_recognition as sr
import os
import webbrowser
import smtplib

def containsWords(wordArr, sentence, option):
  found = []
  for word in wordArr:
    if word in sentence:
      if option == 'or':
        return True
      else:
        found.append(word)
  if option == 'and' and found == wordArr:
    return True
  return False

def talkToMe(audio):
  print(audio)
  tts = gTTS(text=audio, lang='en')
  tts.save('audio.mp3')
  os.system('mpg123 audio.mp3')

def myCommand():
  r = sr.Recognizer()
  print('Awaiting input')
  command = 'nothing'
  with sr.Microphone() as source:
    audio = r.listen(source)
    print('Parsing input')
    try:
      command = r.recognize_google(audio)
      print('You said: ' + command + '\n')
    except sr.UnknownValueError:
      return myCommand()
    return command

def sendMail(to, message):
  mail = smtplib.SMTP('smtp.gmail.com:587')
  mail.ehlo()
  mail.starttls()
  mail.login(email, password)
  mail.sendmail(to, to, message)
  mail.close()
  talkToMe('Email sent')

def assistant(command):
  chrome_path = '/usr/bin/google-chrome'
  command = command.lower()
  if (command == None):
    return 0
  elif (containsWords(['lookup', 'search', 'google'], command, 'or')):
    url = 'http://google.com/search?q='
    keyWords = ['lookup', 'search', 'google']
    split = command.split()
    query = [word for word in split if word.lower() not in keyWords]
    query = '+'.join(query)
    webbrowser.get(chrome_path).open(url + query)
  elif 'rock with us' in command:
    url = 'https://www.youtube.com/watch?v=3IXP_h1WnFc&feature=youtu.be&t=35&autoplay=1'
    webbrowser.get(chrome_path).open(url)
  elif (containsWords(['python', 'subreddit'], command, 'and')):
    url = 'https://www.reddit.com/r/python'
    webbrowser.get(chrome_path).open(url)
  elif 'youtube' in command:
    url = 'https://www.youtube.com/results?search_query='
    keyWords = ['youtube']
    split = command.split()
    query = [word for word in split if word.lower() not in keyWords]
    query = '+'.join(query)
    webbrowser.get(chrome_path).open(url + query)
  elif 'tearing me apart lisa' in command:
    url = 'https://www.youtube.com/watch?v=mPBPa2BQFRM&feature=youtu.be'
    webbrowser.get(chrome_path).open(url)
  elif 'email' in command:
    talkToMe('Who is the recipient?')
    recipient = myCommand()
    if 'myself' in recipient:
      talkToMe('What should I say?')
      content = myCommand()
      talkToMe('Here\'s the message, ' + content)
      talkToMe('Is this okay?')
      approval = myCommand()
      if (containsWords(['sure','yeah','great','yup','yes'], approval, 'or')):
        sendMail('myself', content)
      else:
        talkToMe('Okay I won\'t send that')
    else:
      talkToMe('I don\'t know who ' + recipient + ' is')

talkToMe('I am ready for your command')

while True:
  assistant(myCommand())

