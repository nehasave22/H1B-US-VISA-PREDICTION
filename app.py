import streamlit as st
import re
import pandas as pd
from lightgbm import LGBMClassifier
import pickle
from datetime import date
import requests
from io import BytesIO
# CSS to inject contained in a string
background_image = "https://github.com/nehasave22/H1B-US-VISA-PREDICTION/blob/main/H1B.png" 

html_temp = f"""
    <div style="background-image: {background_image}; background-size: cover;">
    <div style="background-color: rgba(1, 2, 0, 0.5); padding: 10px">
    <h1 style="color:white; text-align:center;">H1B Visa Sponsorship</h1>
    </div>
    </div>
    """    
st.markdown(html_temp, unsafe_allow_html=True)
st.image("https://github.com/nehasave22/H1B-US-VISA-PREDICTION/blob/main/H1B.png", use_column_width=True)

def user_input_features():
    st.subheader('Please Enter the below information')

    # User inputs
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")
    dob = st.date_input("Select your date of birth", min_value=date(1900, 1, 1), max_value=date.today())
    sex = st.selectbox("Select your sex", options=["Male", "Female", "Other"])
    age = st.number_input("Enter your age", min_value=21, max_value=45)
    salary = st.number_input("Enter your salary expectation per annum in USD", min_value=10000, max_value=1000000)
    job_position = st.text_input("Type the job position you are applying for")
    experience_level = st.selectbox("Select your experience level", options=["Entry Level", "Mid Level", "Senior Level"])
    job_start_date = st.date_input("Select your job starting date", min_value=date.today())
    current_visa_status = st.selectbox("Select your current visa status", options=["O1", "L1", "F1", "OPT", "Other", "Not Applicable"])
    work_type = st.selectbox("Select your work type", options=["Full Time", "Part Time", "Internship/Co-op"])
    disability = st.selectbox("Do you have a disability?", options=["Yes", "No"])

    submit_button = st.button("Submit Details")

    if submit_button:
    
        if not re.match("^[A-Za-z ]+$", name):
            st.error("Name should only contain letters and spaces.")
            return None
        # Continue processing if name is valid
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            st.error("Invalid email address.")
            return None
        features = {
            # Define exactly the 12 expected features here
            'Company_Page_Listed': 1 if salary > 50000 else 0, # This is an example condition
            'Is_Supervisor': 1 if 'supervisor' in job_position.lower() else 0,
            'Salary': float(salary),
            'Posting_Listed': 1,  # Assuming always true for this example
            'Views': 100,  # Placeholder, replace with actual logic if available
            'Domain': 123,  # Example domain ID, replace with actual mapping
            'Is_Sponsored': 0,  # Example, set based on logic or input
            'Base_Compensation': float(salary),  # Ensure this is a float if the model expects a float
            'Work_Type_Full-time': 1 if work_type == "Full Time" else 0,
            'Posting_Period_YEARLY': 1,  # Assuming yearly posting for the example
            'Experience_Level_Director': 1 if experience_level == "Senior Level" else 0,
            'Views_scaled': 100 / 1000  # Example scaling, replace with actual logic
        }

        features_df = pd.DataFrame(features, index=[0])
        return features_df

df = user_input_features()

'''if df is not None:
    st.subheader('User Input parameters')
    st.write(df)

    model = pickle.load(open("Final_Project.pkl", 'rb'))
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)

    st.subheader('Prediction Probability')
    st.write('Chance for company to sponsor your H1B visa for the position:', prediction_proba[0][0]*100)
    st.write('Chance for company to not sponsor your H1B Visa for the position:', prediction_proba[0][1]*100)'''

# Function to load model from a GitHub raw URL
def load_model(url):
    response = requests.get(url)
    response.raise_for_status()
    model_file = BytesIO(response.content)
    return pickle.load(model_file)

# URL to the raw .pkl file on GitHub
model_url = 'https://raw.githubusercontent.com/nehasave22/H1B-US-VISA-PREDICTION/main/Final_Project.pkl'

# Load your model
model = load_model(model_url)


# Now you can use 'model' to make predictions
if df is not None:
    st.subheader('User Input parameters')
    st.write(df)
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)
    st.subheader('Prediction Probability')
    st.write('Chance for company to sponsor your H1B visa for the position:', prediction_proba[0][0]*100)
    st.write('Chance for company to not sponsor your H1B Visa for the position:', prediction_proba[0][1]*100)
html_temp1 = """
    <div style="background-color:#010200;">
    <p style="color:white;text-align:center;">Designed & Developed By: <b>Neha Save</b></p>
    </div>
    """
st.markdown(html_temp1, unsafe_allow_html=True)

