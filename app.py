from flask import Flask, render_template, url_for, request
from gtts import gTTS
import os
app=Flask(__name__, static_folder='static', template_folder='templates')
import os

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method=='POST':
        gen_caption = "Tree on Earth"
        tts = gTTS(text=gen_caption, lang='en',tld="com")
        tts.save('static/gen_sound.mp3')
        path = 'static/gen_sound.mp3'
        return render_template('results.html',  input_image="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg", descp=gen_caption, sound=path)


if __name__ == "__main__":
  app.run()