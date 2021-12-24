from flask import Flask, render_template, url_for, request
from gtts import gTTS
from extra_functions import extract_features, generate_desc
from pickle import load
from keras.models import load_model
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method=='POST':
        #getting the image and saving it...
        f = request.files['file']
        f.save("static/img")
        features = extract_features('static/img')
        model = load_model('model_19.h5')
        tokens = load(open('tokenizer.pkl','rb'))
        max_length = 34
        gen_caption = generate_desc(model, tokens, features, max_length)
        #generating the caption/description according to input image...
        # gen_caption = "A beautiful white colored house is sorrounded by lovely mountains."

        #converting text to speech and saving it...
        tts = gTTS(text= "The description for the input image is : " + gen_caption + "Thank You", lang='en', tld="com")
        tts.save('static/gen_sound.mp3')
        return render_template('results.html', input_image= 'static/img', descp=gen_caption, sound='static/gen_sound.mp3')

if __name__ == "__main__":
  app.run()