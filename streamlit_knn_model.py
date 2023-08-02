import streamlit as st
import pyttsx3
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

excel = pd.read_excel('Crop.xlsx', header=0)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
engine.setProperty('voice', voices[0].id)

le = preprocessing.LabelEncoder()
crop = le.fit_transform(list(excel["CROP"]))

NITROGEN = list(excel["NITROGEN"])
PHOSPHORUS = list(excel["PHOSPHORUS"])
POTASSIUM = list(excel["POTASSIUM"])
TEMPERATURE = list(excel["TEMPERATURE"])
HUMIDITY = list(excel["HUMIDITY"])
PH = list(excel["PH"])
RAINFALL = list(excel["RAINFALL"])

features = list(zip(NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL))
features = np.array(features)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(features, crop)

st.title('Crop Recommendation System')

nitrogen_content = st.number_input('Enter ratio of Nitrogen in the soil', 1, 100)
phosphorus_content = st.number_input('Enter ratio of Phosphorus in the soil', 1, 100)
potassium_content = st.number_input('Enter ratio of Potassium in the soil', 1, 100)
temperature_content = st.number_input('Enter average Temperature value around the field', 0.0, 50.0, step=0.1)
humidity_content = st.number_input('Enter average percentage of Humidity around the field', 1, 100)
ph_content = st.number_input('Enter PH value of the soil', 0.0, 14.0, step=0.1)
rainfall = st.number_input('Enter average amount of Rainfall around the field', 0, 500)

if st.button('Submit'):
    predict1 = np.array([nitrogen_content, phosphorus_content, potassium_content, temperature_content,
                         humidity_content, ph_content, rainfall])
    predict1 = predict1.reshape(1, -1)
    predict1 = model.predict(predict1)

    crop_name = str()
    if predict1[0] == 0:              
        crop_name = 'Apple'
    elif predict1[0] == 1:
        crop_name = 'Banana'
    elif predict1[0] == 2:
        crop_name = 'Blackgram'
    elif predict1[0] == 3:
        crop_name = 'Chickpea'
    elif predict1[0] == 4:
        crop_name = 'Coconut'
    elif predict1[0] == 5:
        crop_name = 'Coffee'
    elif predict1[0] == 6:
        crop_name = 'Cotton'
    elif predict1[0] == 7:
        crop_name = 'Grapes'
    elif predict1[0] == 8:
        crop_name = 'Jute'
    elif predict1[0] == 9:
        crop_name = 'Kidneybeans'
    elif predict1[0] == 10:
        crop_name = 'Lentil'
    elif predict1[0] == 11:
        crop_name = 'Maize'
    elif predict1[0] == 12:
        crop_name = 'Mango'
    elif predict1[0] == 13:
        crop_name = 'Mothbeans'
    elif predict1[0] == 14:
        crop_name = 'Mungbeans'
    elif predict1[0] == 15:
        crop_name = 'Muskmelon'
    elif predict1[0] == 16:
        crop_name = 'Orange'
    elif predict1[0] == 17:
        crop_name = 'Papaya'
    elif predict1[0] == 18:
        crop_name = 'Pigeonpeas'
    elif predict1[0] == 19:
        crop_name = 'Pomegranate'
    elif predict1[0] == 20:
        crop_name = 'Rice'
    elif predict1[0] == 21:
        crop_name = 'Watermelon'

    st.write(f'The best crop that you can grow is {crop_name}')

    humidity_level = 'low humid'
    if 34 <= humidity_content <= 66:
        humidity_level = 'medium humid'
    elif humidity_content > 66:
        humidity_level = 'high humid'

    rainfall_level = 'less'
    if 101 <= rainfall <= 200:
        rainfall_level = 'moderate'
    elif rainfall > 200:
        rainfall_level = 'heavy rain'

    speak_text = (
        f"Sir, according to the data that you provided, the best crop that you can grow is {crop_name}. "
        f"The humidity level around the field is {humidity_level} and the amount of rainfall is {rainfall_level}."
    )
    engine.say(speak_text)
    engine.runAndWait()
