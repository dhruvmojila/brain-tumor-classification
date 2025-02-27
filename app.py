import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import  image
import numpy as np
import plotly.graph_objects as go
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.metrics import Precision, Recall
from groq import Groq
import PIL.Image
import os
from dotenv import load_dotenv
load_dotenv()
import base64

output_dir = 'saliency_maps'
os.makedirs(output_dir, exist_ok=True)

client = Groq(
   api_key=os.getenv('GROQ_API_KEY')
)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_explanation(img_path, model_prediction, confidence):
  prompt = f"""
    You are a leading neurosurgeon and expert in brain tumor diagnostics. Your task is to analyze a saliency map generated by a deep learning model that classifies brain tumors into four categories: glioma, meningioma, pituitary tumor, or no tumor. You are type of neurosurgeon who thinks everything in great details brainstorm step by step with experience of old cases and then verify it and then give answer on given case. 

    The saliency map highlights critical regions of interest, shown in light cyan, which influenced the model's prediction. The model has predicted the tumor class as '{model_prediction}' with a confidence of {confidence * 100}%.

    In your analysis:
    1. Explain the significance of the highlighted regions in the context of the predicted tumor class.
    2. Provide possible medical reasons for the prediction, based on the location and characteristics of the highlighted areas.
    3. Include relevant historical insights from similar cases to substantiate the prediction.
    4. Suggest next steps for the patient and the medical team, including additional diagnostic imaging, biopsy, or treatment options.

    Ensure that your explanation:
    - Is comprehensive and includes professional medical terminology.
    - Reflects your expertise as a neurosurgeon.
    - Stays concise and within 6 sentences.
  """

  img = encode_image_to_base64(img_path)
  completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[{
          "role": "user",
           "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                       "url" : f"data:image/jpeg;base64,{img}"
                    },
                }
           ],
    }],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
  )

  return completion.choices[0].message.content


def generate_saliency_map(model, img_array, class_index, img_size):
  with tf.GradientTape() as tape:
    img_tensor = tf.convert_to_tensor(img_array)
    tape.watch(img_tensor)
    predictions = model(img_tensor)
    target_class = predictions[:, class_index]
  gradients = tape.gradient(target_class, img_tensor)
  gradients = tf.math.abs(gradients)
  gradients = tf.reduce_max(gradients, axis=-1)
  gradients = gradients.numpy().squeeze()
  # Resize gradients to match original image size
  gradients = cv2.resize(gradients, img_size)
  # Create a circular mask for the brain area
  center = (gradients.shape [0] // 2, gradients.shape [1] // 2)
  radius = min(center [0], center [1]) - 10
  y, x = np.ogrid[:gradients.shape [0], :gradients.shape[1]]
  mask = (x - center [0])**2 + (y - center [1])**2 <= radius**2
  # Apply mask to gradients
  gradients = gradients * mask
  # Normalize only the brain area
  brain_gradients = gradients[mask]
  if brain_gradients.max() > brain_gradients.min():
    brain_gradients = (brain_gradients - brain_gradients.min()) / (brain_gradients.max() - brain_gradients.min())
  gradients[mask] = brain_gradients
  # Apply a higher threshold
  threshold = np.percentile(gradients[mask], 80)
  gradients[gradients < threshold] = 0
  gradients = cv2.GaussianBlur(gradients, (11, 11), 0)
  # Create a heatmap overlay with enhanced contrast
  heatmap = cv2.applyColorMap(np.uint8(255 * gradients), cv2.COLORMAP_JET)
  heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
  # Resize heatmap to match original image size
  heatmap = cv2.resize(heatmap, img_size)

  original_img = image.img_to_array(img)
  superimposed_img = heatmap * 0.7 + original_img * 0.3
  superimposed_img = superimposed_img.astype(np.uint8)
  img_path = os.path.join(output_dir, uploaded_file.name)
  with open(img_path, "wb") as f:
    f.write(uploaded_file.getbuffer())
  saliency_map_path = f'saliency_maps/{uploaded_file.name}'
  # Save the saliency map
  cv2.imwrite(saliency_map_path, cv2.cvtColor(superimposed_img, cv2.COLOR_RGB2BGR) )
  return superimposed_img

def load_xception_model(model_path):
  img_shape=(128,128,3)
  base_model = tf.keras.applications.Xception(include_top=False, weights="imagenet",
                                              input_shape=img_shape, pooling='max')
  model = Sequential([base_model, Flatten(),
                      Dropout(rate=0.3),
                      Dense(128, activation='relu'),
                      Dropout(rate=0.25),
                      Dense(4, activation='softmax')
  ])
  model.build( (None,) + img_shape)
  # Compile the model
  model.compile(Adamax(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy',
                         Precision(),
                         Recall()])
  model.load_weights(model_path)
  return model

def load_resnet_model(model_path):
  img_shape=(128,128,3)
  base_model = tf.keras.applications.ResNet50(include_top=False, weights="imagenet",
                                              input_shape=img_shape, pooling='max')
  model = Sequential([base_model, Flatten(),
                      Dropout(rate=0.3),
                      Dense(128, activation='relu'),
                      Dropout(rate=0.25),
                      Dense(4, activation='softmax')
  ])
  model.build( (None,) + img_shape)
  # Compile the model
  model.compile(Adamax(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy',
                         Precision(),
                         Recall()])
  model.load_weights(model_path)
  return model

st.title("Brain Tumor Classification")

st.write("Upload an image of a brain MRI scan to classify")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    selected_model = st.radio(
    "Select Model",
    ("Transfer Learning - Xception", "Transfer Learning - ResNet50", "Custom CNN")
    )
    if selected_model == "Transfer Learning - Xception":
        model = load_xception_model('./xception_model.weights.h5')
        img_size = (128, 128)
    elif selected_model == "Transfer Learning - ResNet50":
        model = load_resnet_model('./resnet_model.weights.h5')
        img_size = (128, 128)
    else:
        model = load_model('./cnn_model.h5')
        img_size=(128, 128)

    labels = ['Glioma', 'Meningioma', 'No tumor', 'Pituitary']
    img = image.load_img(uploaded_file, target_size=img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    prediction = model.predict(img_array)
    # Get the class with the highest probability
    class_index = np.argmax(prediction[0])
    result = labels [class_index]
    st.write(f"Predicted Class: {result}")
    st.write("Predictions:")
    for label, prob in zip(labels, prediction[0]):
        st.write(f"{label}: {prob:.4f}")

    saliency_map = generate_saliency_map(model, img_array, class_index, img_size)

    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption='Uploaded Image',use_column_width=True)
    with col2:
        st.image(saliency_map, caption='Saliency Map',use_column_width=True)

    st.write("## Classification Results")
    result_container = st.container()
    result_container = st.container()
    result_container.markdown(
        f"""
        <div style="background-color: #000000; color: #ffffff; padding: 30px; border-radius: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1; text-align: center;">
                <h3 style="color: #ffffff; margin-bottom: 10px; font-size: 20px;">Prediction</h3>
                <p style="font-size: 36px; font-weight: 800; color: #FF0000; margin: 0;">
                {result}
                </р>
            </div>
            <div style="width: 2px; height: 80px; background-color: #ffffff; margin: 0 20px;"></div>
            <div style="flex: 1; text-align: center;">
            <h3 style="color: #ffffff; margin-bottom: 10px; font-size: 20px;">Confidences</h3>
            <p style="font-size: 36px; font-weight: 800; color: #2196F3; margin: 0;">
                {prediction[0][class_index]:.4%}
            </р>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True
        )
    # Prepare data for Plotly chart
    probabilities = prediction[0]
    sorted_indices = np.argsort(probabilities)[::-1]
    sorted_labels = [labels[i] for i in sorted_indices]
    sorted_probabilities = probabilities[sorted_indices]

    fig = go.Figure(go.Bar(
        x=sorted_probabilities,
        y=sorted_labels,
        orientation='h',
        marker_color=['red' if label == result else 'blue' for label in sorted_labels]
    ))
    # Customize the chart layout
    fig.update_layout(
        title='Probabilities for each class',
        xaxis_title='Probability',
        yaxis_title='Class',
        height=400,
        width=600,
        yaxis=dict(autorange="reversed")
    )
    # Add value labels to the bars
    for i, prob in enumerate(sorted_probabilities):
        fig.add_annotation(
        x=prob, y=i,
        text=f'{prob:.4f}',
        showarrow=False, xanchor='left',
        xshift=5)
    # Display the Plotly chart
    st.plotly_chart(fig)

    saliency_map_path = f'saliency_maps/{uploaded_file.name}'
    explanation = generate_explanation(saliency_map_path, result, prediction[0][class_index])

    st.write("## Explanation")
    st.write(explanation)