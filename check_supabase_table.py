"""
Script to check if a table exists in Supabase using REST API.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    exit(1)

# Check if table exists by querying it
table_name = input("Enter table name to check: ")

try:
    # Try to query the table with limit 0 to check existence
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*&limit=0"
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Table '{table_name}' exists in Supabase")
        print(f"  Response: {response.json()}")
    elif response.status_code == 404:
        print(f"✗ Table '{table_name}' does not exist in Supabase")
    else:
        print(f"✗ Error checking table '{table_name}'")
        print(f"  Status code: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Error checking table '{table_name}'")
    print(f"  Error: {e}")
