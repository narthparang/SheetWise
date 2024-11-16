from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import requests
import json
import os
import re
import google.generativeai as genai


# Load API keys and Search Engine ID from environment variables
sheet_api_key = os.getenv("GOOGLE_SHEETS_API")
gsearch_api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")
cse_id = os.getenv("search_engine_id")

# Debugging: Print loaded API keys
# st.write("Google Custom Search API Key:", gsearch_api_key)
# st.write("Search Engine ID:", cse_id)

# st.write("Google gemini api key: " + gemini_api_key)

# Function to load CSV file
def load_csv(file):
    return pd.read_csv(file)

def get_sheet_url():
    sheet_url = st.text_input("Please enter your Google Sheet URL here: ")
    return sheet_url

def extract_sheet_id(sheet_url):
    # Regular expression to find the sheet ID in the URL
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
    if match:
        sheet_id = match.group(1)  # Extract the sheet ID
        return sheet_id  # Return the sheet ID
    else:
        raise ValueError("Invalid Google Sheet URL. Please ensure it is correct.")

def load_google_sheet(sheet_id, sheet_api_key):
    # Construct the URL for the Google Sheets API
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1?key={sheet_api_key}"
    
    # Make a GET request to the Google Sheets API
    response = requests.get(url)
    
    # Debugging: Print the response status and content
    st.write("Google Sheets API Response Status:", response.status_code)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the values from the response
        values = data.get('values', [])
        
        # Convert to DataFrame
        if values:
            headers = values[0]  # First row as headers
            rows = values[1:]    # Remaining rows as data
            return pd.DataFrame(rows, columns=headers)
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no values
    else:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return None

# Function to perform Google Custom Search
def search_google(query, gsearch_api_key, cse_id):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={gsearch_api_key}&cx={cse_id}"
   # st.write("Google Search API Request URL:", search_url)  # Debugging: Print the request URL
    response = requests.get(search_url)
    
    # Debugging: Print the response status and content
    st.write("Google Search API Response Status:", response.status_code)
    
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get('error', {}).get('message', 'Unknown error occurred.')
        st.error(f"Error fetching data from Google Search API: {response.status_code} - {error_message}")
        return None




def extract_with_gemini(search_results, entity):
    # Configure the Gemini API with the provided API key
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Prepare the prompt for the model
    prompt = f"Extract structured information for {entity} from the following search results: {json.dumps(search_results)}, avoid adding any special characters, bold , italic in the answer, so the response remains consitent with further application."
    
    # Generate content using the model
    try:
        response = model.generate_content(prompt)
        print(response)
        st.write("Gemini API Response Status: Success")  # Indicate success in Streamlit
        
        # Return the generated text from the response
        return response.text
    except Exception as e:
        st.error(f"Error fetching data from Gemini API: {str(e)}")
        return None

# Streamlit app
def main():
    st.title("SheetWise: AI Agent for Information Retrieval")

    # Step 1: Load CSV or Google Sheet
    option = st.selectbox("Choose Data Source", ["Upload CSV", "Connect Google Sheet"])
    
    if option == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        if uploaded_file is not None:
            data = load_csv(uploaded_file)
            st.write(data)
            entity_column = st.selectbox("Select Entity Column", data.columns)
    
    elif option == "Connect Google Sheet":
        sheet_url = st.text_input("Enter Google Sheet URL")
        if sheet_url:
            try:
                sheet_id = extract_sheet_id(sheet_url)  
                data = load_google_sheet(sheet_id, sheet_api_key)
                st.write(data)
                entity_column = st.selectbox("Select Entity Column", data.columns)
            except ValueError as e:
                st.error(str(e))

    # Step 2: User Input for Search Query
    if 'data' in locals():
        user_query = st.text_input("Enter your search query")
        
        # Step 3: Perform Search and Extract Information
        if st.button("Extract Information"):
            results = []

            for entity in data[entity_column]:
                search_query = user_query.format(entity=entity)
                search_results = search_google(search_query, gsearch_api_key, cse_id)

                if search_results:
                    structured_info = extract_with_gemini(search_results, entity)
                    results.append({"Entity": entity, "Extracted Info": structured_info})

            # # Step 4: Display Results
            # if results:
            #     st.write(pd.DataFrame(results), "download the results")
            if results:
                # Convert results to DataFrame
                results_df = pd.DataFrame(results)
                
                # Apply custom styling to make text cells scrollable
                st.markdown("""
                    <style>
                        .streamlit-expanderContent div[data-testid="stDataFrame"] div[class^="stDataFrame"] {
                            max-height: 600px;
                            overflow: auto;
                        }
                        .streamlit-expanderContent div[data-testid="stDataFrame"] td {
                            white-space: pre-wrap;
                            height: 100px !important;
                            max-height: 100px !important;
                            overflow-y: auto !important;
                            display: block;
                            padding: 8px;
                            line-height: 1.4;
                        }
                        .streamlit-expanderContent div[data-testid="stDataFrame"] th {
                            padding: 8px;
                            text-align: left;
                            font-weight: bold;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                # Display results in an expander
                with st.expander("View Results", expanded=True):
                    st.dataframe(
                        results_df,
                        height=500,  # Set overall height of the DataFrame
                        use_container_width=True
                    )
                
                # Add download button
                st.download_button(
                    "Download Results",
                    results_df.to_csv(index=False),
                    "results.csv",
                    "text/csv",
                    key='download-csv'
                )

if __name__ == "__main__":
    main()
