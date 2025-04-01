# CalorieSmart AI 🍎

CalorieSmart AI is an intelligent food analysis application that uses Google's Gemini AI model to analyze food images and provide detailed nutritional information, calorie estimates, and health recommendations.

## Features

- 📸 Upload food images for instant analysis
- 🔍 Get detailed calorie estimates for each food item
- 📊 Receive comprehensive nutritional insights
- ⭐ Get personalized health recommendations
- 🎯 Add custom analysis instructions
- 💫 Modern, user-friendly interface

## Technologies Used

- Python 3.9+
- Streamlit
- Google Generative AI (Gemini)
- PIL (Python Imaging Library)
- python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rafiqdevhub/CalorieSmart-AI.git
cd CalorieSmart-AI
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Google API key:
```env
GOOGLE_API_KEY="your_api_key_here"
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the displayed local URL (typically http://localhost:8501)

3. Upload a food image using the file uploader

4. (Optional) Add any specific instructions for the analysis

5. Click "Analyze Calories" to get your results

## Requirements

- Python 3.9 or higher
- Google API key with access to Gemini AI
- Internet connection for API calls

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini AI for providing the image analysis capabilities
- Streamlit for the wonderful web framework
- All contributors and users of CalorieSmart AI