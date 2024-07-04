# Codebase Info

This is the codebase for the paper titled **"Handwritten Code Recognition for Pen-and-Paper CS Education"**, accepted in [ACM Learning @ Scale 2024](https://learningatscale.hosting.acm.org/las2024/).

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Codebase Structure](#codebase-structure)
  - [Directory Layout](#directory-layout)


## Getting Started

To get started clone the repository and follow the instructions below.

```bash
git clone https://github.com/mdoumbouya/codeocr.git
```

### Prerequisites

- Python 3.9 or higher

### Installation

We recomend starting by creating a virtual environment and installing the dependencies. Here are the steps to do so: 


1. **Navigate to the Project's Root Directory:**
   Open a terminal (macOS/Linux) or a command prompt (Windows) and navigate to the root directory of the repository where you want to set up the virtual environment.

2. **Create the Virtual Environment:**
   Run the following command to create a virtual environment named `env` within the project directory:
   
   - **macOS/Linux:**
     ```sh
     python3 -m venv env
     ```
   - **Windows:**
     ```cmd
     python -m venv env
     ```

3. **Activate the Virtual Environment:**
   Before you can start installing or using packages in your virtual environment, you need to activate it.
    
   - **macOS/Linux:**
     ```sh
     source env/bin/activate
     ```
   - **Windows:**
     ```cmd
     .\env\Scripts\activate
     ```

   You'll know that the virtual environment is activated because the command prompt will now show the name of the virtual environment (in this case, `env`).

Now from the root directory of the repository, you can install the dependencies by running the following commands:
```bash
pip install -e .
pip install -r requirements.txt
```

or simply run the following command in **root directory** of the repository:

```bash
make install
```

Once the installation is complete, just move to `experiments/003` direcotry to reporduce the results in the paper. Further instruction are provided in the `README.md` file in the `experiments/003` directory.

```bash
cd experiments/003
```

## Codebase Structure

### Directory Layout

```
codeocr/
├── app
│   ├── __pycache__
│   ├── blueprints
│   │   ├── advanced_ocr
│   │   └── ocr_compiler
│   ├── static
│   │   ├── css
│   │   ├── js
│   │   └── uploaded_images
│   └── templates
├── codeocr.egg-info
├── experiments
│   ├── 001
│   ├── 002
│   ├── 003
│   │   ├── logs
│   │   ├── output
│   │   └── output-001
│   ├── images
│   └── sigcse-all
│       ├── FINAL DATA
│       ├── __pycache__
│       ├── errordata
│       ├── expired
│       ├── hallucination
│       ├── images
│       └── resultscsv
├── keys
├── logs
├── src
│   ├── code_ocr
│   └── codeocr.egg-info
└── uploaded_images

```

## Downloading the Dataset

Link for downloading the dataset: [codeocr-dataset](https://github.com/mdoumbouya/codeocr/blob/main/code-ocr-dataset-20240516.zip). The guidelines on how to use the dataset is provided in the readme file in the dataset zip.
