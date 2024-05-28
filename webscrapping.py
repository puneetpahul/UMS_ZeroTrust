import pandas as pd
import requests
from bs4 import BeautifulSoup
# Load the CSV file
data = pd.read_csv('app_customuser.csv')  # Change to your actual file path

# URLs
login_url = 'http://127.0.0.1:8000/accounts/login/'
logout_url = 'http://127.0.0.1:8000/accounts/logout/'  # Adjust if different

# Start a session with requests
session = requests.Session()

# Loop through each row in the CSV to log in
for index, row in data.iterrows():
    # First, fetch the login page to get the CSRF token
    initial_page = session.get(login_url)
    soup = BeautifulSoup(initial_page.text, 'html.parser')
    csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
    
    # Form data for login including the CSRF token
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'login': row['username'],  # Adjust the form field names if necessary
        'password': 'defaultpassword'
    }
    
    # Make a POST request to the login page with the CSRF token and login credentials
    response = session.post(login_url, data=login_data, headers={'Referer': login_url})
    
    # Check if login was successful
    if response.status_code in [200, 302]:  # Successful login usually redirects
        print(f"Login successful for {row['username']}")
        # Optionally handle the logout
        session.get(logout_url)
    else:
        print(f"Login failed for {row['username']} with status code {response.status_code}")

# Close the session
session.close()
