from numpy import argmax
import PIL.Image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
# from pickle import dump, load
# from numpy import array
# from keras.preprocessing.text import Tokenizer
# from keras.utils import to_categorical
# from keras.layers.merge import add
# from keras.models import load_model
# from keras.layers import Input, Dense, LSTM, Embedding, Dropout
# from keras.callbacks import ModelCheckpoint
def extract_features(filename):
    model = VGG16()
    # model.layers.pop()
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # model._get_distribution_strategy = lambda: None
    image = load_img(filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)
    return feature

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text