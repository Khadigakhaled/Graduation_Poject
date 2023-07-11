# Improved ingredients-based recipe recommendation software using machine learning

A mobile application that helps useres find different recipes based on their preferences and available ingredients. The frontend is built using Flutter and backend is built using Python and Flask.

## Requirements

To run the application, you will need to have the following installed:

1. Flutter
2. Python 3
3. Flask

## Getting started

First navigate to the app (backend) folder and create a virtual environment by running the following command:

python3 -m venv venv

Next, Activate the virtual environment by running the following command:

source venv/bin/activate

Then, install the necessary Python dependencies by running the following command:

pip install -r requirements.txt

Finally, start the Flask API by running the following command:

python app.py

You can now navigate to the frontend directory and run the following command to install the necessary Flutter dependencies:

flutter pub get

You can then run the Flutter app by opening the project in Android Studio or VS Code and clicking the "run" button.

## Usage

The application allows users to input their dietary preferences, such as healthy, vegetarian, etc., and suggests recipes that meet those requirements. Users can also search for specific recipes by name or ingredient.
