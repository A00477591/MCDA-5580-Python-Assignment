import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('digit_classifier_model.h5')

def preprocess_image(image):
    grayscale_image = image.convert('L')
    resized_image = grayscale_image.resize((28, 28))
    image_array = np.array(resized_image)
    normalized_image = image_array / 255.0
    input_image = normalized_image.reshape((1, 28, 28, 1))
    return input_image

def make_prediction(image):
    input_image = preprocess_image(image)
    prediction = model.predict(input_image)
    predicted_class = np.argmax(prediction)
    return predicted_class

def main():
    st.title('Digit Classifier App')
    st.write('Upload an image of a digit to classify it.')

    uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        predicted_digit = make_prediction(image)
        st.write(f'Predicted Digit: {predicted_digit}')

if __name__ == '__main__':
    main()
