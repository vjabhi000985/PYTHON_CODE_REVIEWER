# Python Code Reviewer Using Gemini AI

## Overview

Python Code Reviewer is a web application that leverages Google's Generative AI (Gemini AI) to analyze Python code snippets. The app reviews user-submitted Python code, identifying bugs, suggesting optimizations, and providing general guidance to help developers improve their code.

## Features

- **Code Review:** Get a detailed analysis of your code, including bug detection, optimization suggestions, and user guidance.
- **Multi-Language Support:** The app can review code written in JavaScript, Python, and Java.
- **User-Friendly Interface:** Built using Streamlit for a smooth and interactive user experience.
- **Generative AI Integration:** Powered by Google's Generative AI to provide accurate and efficient code feedback.
- **Image to Code Extraction:** Allows users to upload images of handwritten or printed code. The app then processes these images and converts them into editable Python code.

- **Image-Based Code Review:** Review process to handle code extracted from images.

## Screenshot

**Homepage** : ![Image](https://github.com/user-attachments/assets/266c525b-309d-452e-b476-74b5f1bd3e99)

## Deployment

You can access the deployed version of the app here:  
**Deployment link** : [pythoncodereviewer.streamlit.app](https://pythoncodereviewer.streamlit.app)

## Installation and Setup

### Prerequisites

Before running the app locally, you need to have the following installed:

- Python 3.7+
- Streamlit
- `google-generativeai` library
- `python-dotenv` library

### Step 1: Clone the repository

```bash
git clone https://github.com/vjabhi000985/AI_Code_Reviewer.git
cd AI_Code_Reviewer
```

### Step 2: Set up the environment

- Create a .env file in the root directory of the project and add your Google API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

### Step 3: Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Run the app locally

- After the dependencies are installed and the .env file is configured, run the app using Streamlit:

```bash
streamlit run app.py
```

- This will start a local server, and you can open the app in your browser by visiting http://localhost:8501.

## Future Enhancements

We are continuously working to improve the Python Code Reviewer. Some future enhancements include:

- Support for More Languages: Expanding the code review functionality to support other programming languages like JavaScript, C++, and Go.

- Integration with IDEs: Adding the ability to integrate the app directly with popular IDEs like VS Code and PyCharm for real-time code reviews.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is open-source and available under the MIT License.
