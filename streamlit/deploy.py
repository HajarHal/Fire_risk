import streamlit as st
import pandas as pd
import pickle

with open('model2.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

st.markdown(
    f"""
    <h1 style='color: #ED3237;'>Fire Risk Prediction App</h1>
    """,
    unsafe_allow_html=True
)
def predict_fire_occurrence(model, data):
    X_new = pd.DataFrame(data, index=[0])
    prediction = model.predict(X_new)
    probability = model.predict_proba(X_new)[:, 1]
    return prediction[0], probability[0]

st.sidebar.image('Fire Risk.png', width=270)

st.sidebar.subheader('Paramètres d\'entrée')
brightness = st.sidebar.slider('Luminosité', min_value=0, max_value=500, value=50)
temp = st.sidebar.slider('Température', min_value=20, max_value=60, value=25)
humidity = st.sidebar.slider('Humidité', min_value=0, max_value=100, value=60)
wind_speed = st.sidebar.slider('Vitesse du vent', min_value=0, max_value=100, value=10)
ndvi = st.sidebar.slider('Indice NDVI', min_value=0.0, max_value=1.0, value=0.1)

if st.sidebar.button('Prédire'):
    prediction, probability = predict_fire_occurrence(loaded_model, {
        'brightness': brightness,
        'temp': temp,
        'humidity': humidity,
        'wind_speed': wind_speed,
        '500m 16 days NDVI': ndvi
    })

    st.subheader('Résultat de la prédiction :')
    if prediction == 1:
        st.markdown(
            f"""
            <p style='color: #F58634;'>Prédiction d'occurrence d'incendie.</p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <p style='color: #F58634;'>Pas d\'occurrence d\'incendie prédite.</p>
            """,
            unsafe_allow_html=True
        )


    st.subheader('Probabilité de prédiction :')
    st.markdown(
        f"""
        <p><span style='color: #F58634;'>Probabilité d'occurrence d'incendie :</span> <span style='color: #ED3237; font-weight: bold;'>{probability:.2f}</span></p>
        """,
        unsafe_allow_html=True
    )
