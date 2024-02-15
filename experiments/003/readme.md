# Research Reproduction Guide

Welcome to our results reproduction guide. This document aims to facilitate a smooth experience as you work to reproduce our results. We have included collected data to streamline your reproduction efforts. Live API services can change; therefore, your results might slightly differ if APIs have updated.

## Table of Contents

- [Quick Start](#quick-start)
- [Detailed Reproduction Steps](#detailed-reproduction-steps)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Generating Results](#generating-results)
    - [removeing Up](#removeing-up)
- [Reproducing From Scratch](#reproducing-from-scratch)
    - [Environment Variables](#environment-variables)
    - [API Keys Collection](#api-keys-collection)
    - [Initial remove-Up Commands](#initial-remove-up-commands)
    - [Complete Reproduction](#complete-reproduction)
- [Warnings and Notes](#warnings-and-notes)
- [Guide to Collecting API Keys for Services](#guide-to-collecting-api-keys-for-services)
    - [OpenAI API Key](#openai-api-key)
    - [Microsoft Azure Cognitive Services](#microsoft-azure-cognitive-services)
    - [Google Cloud Vision API](#google-cloud-vision-api)
    - [AWS Textract](#aws-textract)
    - [Mathpix OCR](#mathpix-ocr)
    - [Troubleshooting](#troubleshooting)
    - [Contact Information](#contact-information)

## Quick Start

For those looking to quickly generate the results used in our paper, execute the following commands from the `experiments/003` directory:

Generate the result table:
```bash
make output/eval_results.txt
```

Generate annotated images and post-corrected code:
```bash
make output/dumped_outputs
```

Remove generated results:
```bash
make remove-results
```

Recreate all results:
```bash
make all-results
```

## Detailed Reproduction Steps

### Prerequisites

Ensure you have the necessary dependencies installed on your system to run the commands provided in this guide.
```bash
pip install -r requirements.txt
```

### Setup

Our repository includes all collected data in the `../apipayload.json` and `/output` directories to streamline the reproduction process. It's crucial not to manually modify the JSON files in the output directory, as it may affect the timestamps and disrupt the expected behavior of `make` commands.

### Generating Results

To generate the result table and dump results, use the commands provided in the [Quick Start](#quick-start) section. These commands will save the results in the output directory.

### removeing Up

To remove generated files (`output/eval_results.txt` and `output/dump_results.py`), run:
```bash
make remove-results
```

## Reproducing From Scratch

If you aim to conduct the entire experiment from scratch, follow the steps below. This process requires your own API keys for the services used in the experiments, which may incur some costs.

There are two differente routes to reproduce the resutls
1. You can use the OCR data that we have stored, and re-execute OCR Post Processing, Indentation Recogntion, and Language Model Post Correction from scratch.
2. Get rid of the OCR data that we have stored, and re execute the entire process from scratch.

### Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```bash
OPENAI_API_KEY=<your_openai_api_key>
```

For OCR reproduction, include additional variables:

```bash
MATHPIX_APP_ID=<your_mathpix_app_id>   # If applicable
MATHPIX_APP_KEY=<your_mathpix_app_key> # If applicable
AZURE_ENDPOINT=<your_azure_endpoint>   # If applicable
AZURE_KEY=<your_azure_key>             # If applicable
```

Place your Google Cloud Vision `gcloud-sacct-cred.json` in the `~/src/code_ocr/` directory.

For AWS Textract, configure the AWS CLI as follows:

```bash
aws configure
```

### API Keys Collection

Scroll down to the bottom of the page for instructions on collecting API keys for the services used in the experiments.

### Initial remove-Up Commands

To remove up existing output data, run:

```bash
make remove-output
```

For a complete reset, including OCR data, use:

```bash
make remove-all-data
```

### Complete Reproduction

With the environment set up and initial data removeed, you can now reproduce the experiment results by running:

```bash
make all-results
```

## Warnings and Notes

- Do not manually modify JSON files in the output directory to prevent issues with file timestamps.
- Ensure all necessary environment variables are set before starting the reproduction process.


To enhance coherence and readability, I'll restructure your guide on collecting API keys for various services, ensuring each section is clearly defined and easy to follow. Here's the revised version:

---

## Guide to Collecting API Keys for Services

This guide provides step-by-step instructions for obtaining API keys from various services used in our experiments. Please note that this information is accurate as of 02/15/2024 and was compiled with the help of an AI tool. For the most current and detailed instructions, refer directly to each service's official documentation.

### OpenAI API Key

To obtain an API key for GPT-4 from OpenAI, follow these steps:

1. **Sign Up**: Visit the [OpenAI website](https://openai.com/) and sign up for an account.
2. **Verify Email**: Confirm your email address by clicking on the verification link sent to your inbox.
3. **API Dashboard**: Log into your OpenAI account and navigate to the API section.
4. **Generate API Key**: Find and click on the "New API Key" or "Create API Key" option.
5. **Receive Key**: Copy the provided API key into your `.env` file.

[More Information](https://openai.com/blog/openai-api)

### Microsoft Azure Cognitive Services

To get an Azure Cognitive Services Vision API key, do the following:

1. **Azure Account**: Sign up at the [Azure website](https://azure.microsoft.com/).
2. **Azure Portal**: Log in and go to the Azure Portal.
3. **Create a Resource**: Click "Create a resource" and search for "Cognitive Services".
4. **Select Cognitive Services**: Choose "Cognitive Services" from the marketplace.
5. **Fill in Details**: Provide the required information for your new resource.
6. **Review and Create**: Deploy your resource by clicking "Create".
7. **Access Keys**: Find your subscription keys and endpoint in the "Keys and Endpoint" section.

[More Information](https://learn.microsoft.com/en-us/rest/api/cognitiveservices/)

### Google Cloud Vision API

Setting up Google Cloud Vision API involves the following steps:

1. **Enable Cloud Vision API**: In your GCP console, enable the Cloud Vision API for your project.
2. **Create a Service Account**: Provide a name and assign the "Vision API User" role to your new service account.
3. **Download Key**: Select JSON format for your service account key and download it. Store this file in the `src/code_ocr/` directory.

[More Information](https://cloud.google.com/vision/docs/setup)

### AWS Textract

To configure AWS Textract using the AWS CLI:

1. **AWS Account**: Create an account on the [AWS website](https://aws.amazon.com/).
2. **Install AWS CLI**: Follow the instructions on the [AWS CLI website](https://aws.amazon.com/cli/) for installation.
3. **Configure AWS CLI**: Run `aws configure` in your terminal and enter your AWS Access Key ID, Secret Access Key, and default region.

[More Information](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)

### Mathpix OCR

For Mathpix OCR API key:

1. **Sign Up for Mathpix**: Register on the [Mathpix website](https://mathpix.com/).
2. **Verify Your Email**: Activate your account by clicking the verification link in your email.
3. **Generate API Key**: In the Mathpix dashboard, find the option to generate a new API key and copy it to your `.env` file.

## Troubleshooting

If you encounter any issues or need to start over, you can clone the repository again using:

```bash
git clone https://github.com/mdoumbouya/codeocr.git
```

## Contact Information

For further assistance, feel free to reach out:

- Moussa Doumbouya - moussa@stanford.edu (@mdoumbouya)
- Sazzad Islam - sazzad14@stanford.edu (@sazzadi-r14)
