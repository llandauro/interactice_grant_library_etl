from dotenv import load_dotenv
import os
import openai
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file 
# So it is always activated when exterior source tries to run the code)
load_dotenv()

# Set up OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI()

def get_website_content(url):
    """
    Fetches the content of a website and returns the HTML content
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def clean_text(text):
    """
    Cleans the extracted text by removing extra spaces, empty lines, and irrelevant content.
    """

    lines =[line.strip() for line in text.splitlines()]

    cleaned_lines = [line for line in lines if line]

    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text
      
def extract_text(html_content):
    """
    Uses BeautifulSoup to extract text content from HTML.
    Returns the extracted clean text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract all text from the website
    all_text = soup.get_text(separator='\n').strip()

    cleaned_text = clean_text(all_text)
    
    return cleaned_text

def verify_deadline_with_gpt(text_content, given_date):
    """
    Uses the OpenAI API to check if the deadline in the test matches the given date.
    """
    prompt = (f"Given the text content:\n\n{text_content}\n\n"
        f"Is the current deadline for the grant the same as {given_date}? "
        f"If it is, return 'true'. If not, return the exact deadline date with this format ideally: MM/DD/YYYY"
        "as it would appear in an Excel file. If there's a date range, provide the start and end dates."
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are in charge of verifying the accuracy of an excel and you can only answer with the response that would go on the case of the excel sheet."},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content

def check_grant_deadline(url, given_date):
    """
    Main function to check if the grant deadline on the website matches the given date.
    """
    try:
        # Step 1: Get the website content
        html_content = get_website_content(url)
        # Step 2: Extract text content from HTML
        text_content = extract_text(html_content)
        #print(text_content)
        # Step 3: Verify the deadline using GPT
        result = verify_deadline_with_gpt(text_content, given_date)
        # Print the result
        print(f"GPT-4 Response:\n{result}")
    except Exception as e:
        print(f"An error occurred: {e}")

test_cases = [
    #('https://www.farmtocafeteriacanada.ca/our-work/farm-to-school-grants/', '2/18/2022')
    #('https://www.nutritionnorthcanada.gc.ca/eng/1659529347875/1659529387998','N/A')
    #('https://www.firstnations.org/projects/gather-food-sovereignty-grants/','N/A')
    #('https://www.sac-isc.gc.ca/eng/1386530682712/1615722928307', '3/31/2024')
    ]

# Iterate through the test cases
for url, given_date in test_cases:
    html_content = get_website_content(url)
    text_content = extract_text(html_content)
    print(text_content)
    #check_grant_deadline(url, given_date)
