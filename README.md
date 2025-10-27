---
title: FinnoSQLbot
app_file: FinnoSQLApp.py
sdk/ library: streamlit
lib_version: 1.34.0
lib_author: Snowflake Inc
app_author: Paul Biswa
author_email: replypaul@gmail.com
---


# 💬 FinnoSQL ChatBot : GenAI-Powered SQL Chat Assistant
## An interactive Generative AI-driven chat assistant designed to interpret natural language prompts and execute SQL queries dynamically.
This application enables **financial data exploration** by leveraging **LLM-based prompt parsing** to generate **context-aware SQL** statements. 
It connects to a **Snowflake data warehouse**, executes the queries securely, and returns **structured tabular responses** based on real-time results.

## 🔧 Technical Highlights
- **Natural Language to SQL Translation** using GenAI models

- **Dynamic Query Generation** with semantic understanding of user intent

- **Secure Execution on Snowflake** with parameterized queries"

- **Stuctured Tabular Output Rendering** using interactive UI components (eg, Streamlit, Gradio)}

- **Error Handling & Query Validation** to ensure safe and accurate data access

- **Domain-Specific Optimization** for financial datasets and KPIs


This assistant is ideal for non-technical users, data analysts, or business stakeholders who want to interact with complex datasets without writing SQL manually.


# Access Snowflake Arctic Instruct LLM via the Replicate API
## Snowflake's brand new open-source foundation model Arctic was released on April 24, 2024
Arctic is available for free for a limited time on Snowflake Cortex (until end of May)

## To start using Arctic with Replicate, you’ll need to get your own Replicate API token, which is a simple 3-step process:

### 1. Get API token
Go to https://replicate.com/signin/ 19.
Sign in with your GitHub account.
Proceed to the API tokens page from Profile section and copy your API token.

### 2. Install Replicate
You can install the Replicate 3 Python library in the command-line as follows:

pip install replicate

### 3. Set API token
Next, set the REPLICATE_API_TOKEN environment variable:

export REPLICATE_API_TOKEN=<paste-your-token-here>

### 4. Local development
To set up a local coding environment, enter the following into a command line prompt:

pip install streamlit replicate

### 5. Cloud development
You can set up a cloud environment by deploying to the Streamlit Community Cloud

Add a requirements.txt file to your GitHub repo and include the following prerequisite libraries:

streamlit==1.34.0
replicate
transformers
snowflake-snowpark-python[pandas]




![Landing Page of the FinnoSQLbot App](<FinnoSQLBot App UI.png>)
![Landing Page scroll bottom section of the App ](<FinnoSQLBot App UI 02.png>)
![](<FiinoSQL at Snowflake 2024-05-22.jpeg>)
![](<Project Story Screenshot 2024-05-22.jpeg>)

