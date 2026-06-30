"""
Script to apply Supabase migration using REST API.
Requires SUPABASE_SERVICE_ROLE_KEY for admin operations.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
    print("Please add these to your .env file")
    exit(1)

# Read the SQL migration file
migration_file = 'supabase_migrations/create_users_table.sql'

try:
    with open(migration_file, 'r') as f:
        sql_content = f.read()
except FileNotFoundError:
    print(f"Error: Migration file '{migration_file}' not found")
    exit(1)

# Execute SQL via Supabase REST API
url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
headers = {
    'apikey': SUPABASE_SERVICE_ROLE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
    'Content-Type': 'application/json'
}

# Try using the SQL endpoint directly
sql_url = f"{SUPABASE_URL}/rest/v1/"
sql_headers = {
    'apikey': SUPABASE_SERVICE_ROLE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'params=single-object'
}

print("Applying migration to Supabase...")
print(f"SQL file: {migration_file}")

# Supabase doesn't have a direct SQL execution endpoint via REST API
# We need to use the SQL Editor or CLI instead
print("\nNote: Supabase REST API doesn't support direct SQL execution.")
print("Please use one of these alternatives:")
print("\n1. Supabase Dashboard:")
print("   - Go to SQL Editor in your Supabase dashboard")
print("   - Copy the SQL from supabase_migrations/create_users_table.sql")
print("   - Paste and run it")
print("\n2. Supabase CLI:")
print("   - Install: npm install -g supabase")
print("   - Run: supabase db execute --file supabase_migrations/create_users_table.sql")
print("\n3. psql command line:")
print(f"   - psql {SUPABASE_URL.replace('https://', 'postgresql://postgres:[YOUR-PASSWORD]@db.').replace('/rest/v1', '/postgres')} -f {migration_file}")
