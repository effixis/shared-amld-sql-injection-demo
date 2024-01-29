# AMLD SQL Injection Demo

## Introduction

Welcome to the AMLD SQL Injection Demo by Effixis for AMLD EPFL 2024! This project showcases the risks of SQL injections in web applications, particularly when using Large Language Models (LLMs). The repository includes two demonstrations: Basic SQL Injections and LLM Safeguard.

## Features

- **Basic SQL Injections (`Basic_SQL_Injections.py`):** Demonstrates the risks of direct SQL query generation by LLMs, leading to potential SQL injections.
- **LLM Safeguard (`pages/LLM_safeguard.py`):** Illustrates an advanced setup where an LLM Safeguard is employed to detect and filter out malicious SQL queries.
- **Chinook Database Integration:** Uses the Chinook sample database, representing a digital media store.
- **Interactive Web Interface:** Built with Streamlit, offering a user-friendly interface for interacting with both demonstrations.
- **Database Reset Functionality:** Allows users to reset the database to its original state for repeated tests.

## Installation

1. Clone the repository:
    
    ```bash
    git clone https://github.com/effixis/shared-amld-sql-injection-demo.git
    ```

2. Navigate to the cloned directory:

    ```bash
    cd shared-amld-sql-injection-demo
    ```

3. Install the required packages:

    Activate your preferred Python environment and install the required packages using the provided `requirements.txt` file. For example, using Conda:

    ```bash
    conda create -n amld-sql-injection-demo
    conda activate amld-sql-injection-demo
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and set the OpenAI API key:

    ```bash
    echo "OPENAI_API_KEY=enter_your_api_key_here" > .env
    ```

    You can find your API key on the [OpenAI dashboard](https://beta.openai.com/).

## Usage

Run the Streamlit application:

```bash
streamlit run Basic_SQL_Injections.py
```

Follow the instructions on the web interface to interact with the application.

## Disclaimer

This demo is for educational purposes to showcase the risk of SQL injections using LLMs. It should not be used for malicious purposes. Users are responsible for any misuse of the tools and information provided.
