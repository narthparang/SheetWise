# SheetWise
# AI Agent for Information Retrieval

![AI Agent](https://img.shields.io/badge/Streamlit-1.0.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## Overview

This project is an **AI Agent** that allows users to extract structured information from web searches based on entities defined in a dataset. The application supports input from both CSV files and Google Sheets, utilizing the **Custom Google Search API** for web searching and the **Gemini API** for language model integration. The user-friendly dashboard is built using **Streamlit**, making it easy to interact with and visualize results.

## Features

- **Data Source Support**: Upload CSV files or connect to Google Sheets.
- **Dynamic Search Queries**: Define search queries with placeholders for entities.
- **Web Search**: Retrieve information using the Custom Google Search API.
- **LLM Integration**: Extract structured information using the Gemini API.
- **Downloadable Results**: View and download extracted information in CSV format.
- **Interactive Dashboard**: Built with Streamlit for a seamless user experience.

## Technologies Used

- **Python**: The programming language used for the application.
- **Streamlit**: For creating the interactive dashboard.
- **Google Custom Search API**: For performing web searches.
- **Google Sheets API**: For integrating Google Sheets data.
- **Gemini API**: For leveraging language models to extract information.

- # AI Agent User Guide

Welcome to the AI Agent! This guide will help you understand how to use the AI Agent for querying data from your CSV files or Google Sheets.

## Getting Started

### Step 1: Upload a CSV File or Insert Google Sheets Link

- **Upload CSV File:** Click on the upload button to select and upload your CSV file.
- **Insert Google Sheets Link:** If you prefer to use a Google Sheet, paste the link to your Google Sheet in the designated input area.

### Step 2: Select the Column for Querying

- After uploading your CSV file or inserting the Google Sheets link, you will see a list of available columns.
- Select the column that you want to search for your query.

### Step 3: Write Your Query

- In the search box provided, enter your query. This is the information you want to search for in the selected column.

### Step 4: Connect to Google Custom Search Engine

- Once you have entered your query, the AI Agent will connect to the Google Custom Search Engine.
- The agent will then parse the retrieved information and process it using Gemini.

### Step 5: Download the Results

- After processing, the AI Agent will generate a CSV file containing all the results related to your query.
- You can download this results file by clicking the "Download" button.

## Conclusion

That's it! You are now ready to use the AI Agent for querying data from your CSV files or Google Sheets. If you have any questions or need further assistance, feel free to reach out.

Happy querying!



