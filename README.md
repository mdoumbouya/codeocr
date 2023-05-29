# Code OCR Demo

This is our prototype Flask-based web application to test out the Handwritten Code Recognition System. Users can upload images of code snippets, and the application will extract the source code and display it, along with the compilation results.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Application Structure](#application-structure)
  - [Directory Layout](#directory-layout)
  - [Code Components](#code-components)
- [Usage](#usage)
- [Contributing](#contributing)

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Flask web framework

### Installation

1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your local machine.

2. (Optional) Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Linux or macOS
venv\Scripts\activate  # For Windows, in CMD
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

The application will start on `http://localhost:4444`. Open this URL in your browser to access the Code OCR Demo.

## Application Structure

### Directory Layout

```
my_flask_app/
  |---app/
  |     |---templates/
  |     |     |---index.html
  |     |
  |     |---static/
  |     |     |---css/
  |     |     |---js/
  |     |     |---images/
  |     |
  |     |---blueprints/
  |     |     |---ocr_compiler/
  |     |     |     |---__init__.py
  |     |     |     |---routes.py
  |     |
  |     |---__init__.py
  |     |---config.py
  |     |---models.py
  |     |---routes.py
  |---run.py
  |---requirements.txt
  |---keys/
  |     |---gcloud-sacct-cred.json (Google Cloud Vision API credentials)
  |---README.md
  |---LICENSE
  |---dowload_from_google_drive.py
  |---Makefile
  |---.gitignore

```

### Code Components

- `app/__init__.py` initializes the Flask app and brings together all the components like routes, models, etc.
- `app/blueprints/ocr_compiler/` contains the core functionality of the OCR compiler.
  - `__init__.py` initializes and registers the `ocr_compiler` Blueprint.
  - `routes.py` contains the route functions for the OCR compiler, including handling image uploads, OCR processing, and displaying results.
- `app/templates/` holds the HTML templates.
  - `index.html` is the main template that contains the form for image uploads and displays the OCR and compilation results.
- `config.py` contains the configuration settings for the Flask app.
- `requirements.txt` lists all the packages required by the Flask app, which can be installed via pip.

## Usage

- Users can upload images of code snippets through the "Take a picture of your code" input field.
- Once the image is uploaded and processed, the application will display the extracted source code and compilation results.

## Contributing

This app is following the standard flas app structure. To add new features, you can create new Blueprints for specific functionalities and register them in `app/__init__.py`. Intention behind this was to make it easier to maintain, and debug as there is a lot of moving pieces.

Let's update the README file and document our changes accordingly.