#!/usr/bin/env python3
"""
Simple python-dotenv behavior experiment - linear script
"""

import os
import tempfile
from dotenv import load_dotenv, set_key, unset_key, dotenv_values

# Test .env content with comments and variables
test_env_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME=MyApp
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false
"""

print("=" * 60)
print("PYTHON-DOTENV SIMPLE BEHAVIOR EXPERIMENT")
print("=" * 60)

# Create temporary .env file
with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
    f.write(test_env_content)
    env_file = f.name

print(f"\n1. INITIAL .env FILE:")
print("-" * 40)
with open(env_file, 'r') as f:
    print(f.read())

print(f"\n2. LOADING .env FILE:")
print("-" * 40)
result = load_dotenv(env_file)
print(f"load_dotenv returned: {result}")

print(f"\n3. ENVIRONMENT VARIABLES AFTER LOADING:")
print("-" * 40)
for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'APP_NAME', 'DEBUG']:
    print(f"{key}={os.environ.get(key)}")

print(f"\n4. USING dotenv_values:")
print("-" * 40)
values = dotenv_values(env_file)
for key, value in values.items():
    print(f"{key}={repr(value)}")

print(f"\n5. UNSETTING DB_PORT:")
print("-" * 40)
unset_key(env_file, 'DB_PORT')
print("File after unset_key('DB_PORT'):")
with open(env_file, 'r') as f:
    print(f.read())

print(f"\n6. SETTING DB_PORT TO 3306:")
print("-" * 40)
set_key(env_file, 'DB_PORT', '3306')
print("File after set_key('DB_PORT', '3306'):")
with open(env_file, 'r') as f:
    print(f.read())

print(f"\n7. SETTING NEW VARIABLE:")
print("-" * 40)
set_key(env_file, 'NEW_VAR', 'new_value')
print("File after set_key('NEW_VAR', 'new_value'):")
with open(env_file, 'r') as f:
    print(f.read())

print(f"\n8. UPDATING EXISTING VARIABLE:")
print("-" * 40)
set_key(env_file, 'APP_NAME', 'UpdatedApp')
print("File after set_key('APP_NAME', 'UpdatedApp'):")
with open(env_file, 'r') as f:
    print(f.read())

# Cleanup
os.unlink(env_file)

print(f"\n" + "=" * 60)
print("EXPERIMENT COMPLETE")
print("=" * 60)

# ACTUAL OUTPUT
"""
============================================================
PYTHON-DOTENV SIMPLE BEHAVIOR EXPERIMENT
============================================================

1. INITIAL .env FILE:
----------------------------------------
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME=MyApp
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false


2. LOADING .env FILE:
----------------------------------------
load_dotenv returned: True

3. ENVIRONMENT VARIABLES AFTER LOADING:
----------------------------------------
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
APP_NAME=MyApp
DEBUG=false

4. USING dotenv_values:
----------------------------------------
DB_HOST='localhost'
DB_PORT='5432'
DB_NAME='myapp'
DB_USER='postgres'
DB_PASSWORD='secret'
APP_NAME='MyApp'
DEBUG='false'
PORT='8000'
FEATURE_AUTH='true'
FEATURE_API='false'

5. UNSETTING DB_PORT:
----------------------------------------
File after unset_key('DB_PORT'):
# Database Configuration
DB_HOST=localhost
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME=MyApp
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false


6. SETTING DB_PORT TO 3306:
----------------------------------------
File after set_key('DB_PORT', '3306'):
# Database Configuration
DB_HOST=localhost
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME=MyApp
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false
DB_PORT='3306'


7. SETTING NEW VARIABLE:
----------------------------------------
File after set_key('NEW_VAR', 'new_value'):
# Database Configuration
DB_HOST=localhost
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME=MyApp
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false
DB_PORT='3306'
NEW_VAR='new_value'


8. UPDATING EXISTING VARIABLE:
----------------------------------------
File after set_key('APP_NAME', 'UpdatedApp'):
# Database Configuration
DB_HOST=localhost
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Application Settings
APP_NAME='UpdatedApp'
DEBUG=false
PORT=8000

# Feature Flags
FEATURE_AUTH=true
FEATURE_API=false
DB_PORT='3306'
NEW_VAR='new_value'


============================================================
EXPERIMENT COMPLETE
============================================================
"""

# OBSERVATIONS
"""
1. COMMENT PRESERVATION: Comments are preserved when using set_key/unset_key operations
2. LINE POSITION: 
   - unset_key removes the line completely
   - set_key for existing variable updates the line in place
   - set_key for new variable appends to the end of the file
3. QUOTING: set_key automatically adds quotes around values
4. LOADING: load_dotenv loads variables into os.environ
5. PARSING: dotenv_values returns a dict with string values (all values are strings)
6. FILE MODIFICATION: Operations modify the file directly, preserving structure
"""