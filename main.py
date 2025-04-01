"""
Gemini Health App - A Streamlit application that analyzes food images and calculates calories
using Google's Gemini AI model.
"""

from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Custom CSS to enhance the UI
def load_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .stButton > button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            padding: 0.5rem;
            font-size: 1.2rem;
            border-radius: 10px;
            border: none;
            margin-top: 1rem;
        }
        .stButton > button:hover {
            background-color: #FF2B2B;
            transition: all 0.3s ease;
        }
        h1 {
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 2rem;
        }
        .upload-section {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .results-section {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .app-header {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }
        .analysis-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# Load environment variables and configure Gemini AI
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Constants
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
MODEL_NAME = "gemini-2.0-flash"
PAGE_TITLE = "CalorieSmart AI"

# Nutrition analysis prompt template
NUTRITION_PROMPT = """
As a professional nutritionist, analyze the food items in the image and provide:
1. A detailed list of identified food items with their estimated calories
2. Total caloric content
3. Basic nutritional insights and health recommendations

Format the response as:

📋 Identified Items:
• [Food Item] - [Calories] kcal
• [Food Item] - [Calories] kcal

📊 Total Calories: [Sum] kcal

💡 Nutritional Insights:
• [Insight 1]
• [Insight 2]

🌟 Health Tips:
• [Recommendation 1]
• [Recommendation 2]
"""

def get_gemini_response(
    user_input: str,
    image_data: List[Dict[str, Union[str, bytes]]],
    prompt: str
) -> str:
    """
    Generate a response from Gemini AI model based on the input image and prompt.
    
    Args:
        user_input (str): Additional input from the user
        image_data (List[Dict]): Processed image data in the required format
        prompt (str): The main prompt for the model
        
    Returns:
        str: The generated response from the model
    
    Raises:
        Exception: If there's an error in generating the response
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([user_input, image_data[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, there was an error analyzing the image. Please try again."

def process_uploaded_image(uploaded_file) -> Optional[List[Dict[str, Union[str, bytes]]]]:

    """
    Process the uploaded image file into the format required by Gemini AI.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        Optional[List[Dict]]: Processed image data or None if processing fails
        
    Raises:
        FileNotFoundError: If no file is uploaded
    """
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")
    
    try:
        bytes_data = uploaded_file.getvalue()
        return [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def setup_page():
    """Configure the Streamlit page settings and layout."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="🍎",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    load_css()
    
    # Custom header with emoji
    st.markdown(
        '<div class="header-container">'
        '<h1 class="app-header">🍎CalorieSmart AI - Emphasizes the calorie counting feature with AI intelligence </h1>'
        '</div>',
        unsafe_allow_html=True
    )

def display_welcome_message():
    """Display a welcoming introduction message."""
    st.markdown("""<div style='text-align: center; padding: 1rem 0;'>
            <p style='font-size: 1.2rem; color: #666;'>
                Welcome to your personal AI nutritionist! Upload a photo of your food, 
                and I'll analyze its caloric content and nutritional value.
            </p>
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function that runs the Streamlit interface."""
    setup_page()
    display_welcome_message()
    
    # Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Create two columns with better proportions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📸 Choose a food image...",
            type=SUPPORTED_IMAGE_TYPES,
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                st.image(
                    image,
                    caption="Your Food Image",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error displaying image: {str(e)}")
                return
    
    with col2:
        st.markdown("### 🔍 Analysis Options")
        user_input = st.text_area(
            "Additional Instructions (optional):",
            placeholder="E.g., 'Include ingredients' or 'Focus on protein content'",
            key="input",
            help="Add any specific instructions for the analysis"
        )
        
        submit = st.button("🔍 Analyze Calories", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Process and generate response
    if submit and uploaded_file:
        with st.spinner("🔄 Analyzing your food..."):
            try:
                image_data = process_uploaded_image(uploaded_file)
                if image_data:
                    response = get_gemini_response(user_input, image_data, NUTRITION_PROMPT)
                    st.markdown('<div class="results-section">', unsafe_allow_html=True)
                    st.markdown("### 📊 Analysis Results")
                    st.markdown(response)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
    elif submit:
        st.warning("⚠️ Please upload an image first.")

if __name__ == "__main__":
    main()

