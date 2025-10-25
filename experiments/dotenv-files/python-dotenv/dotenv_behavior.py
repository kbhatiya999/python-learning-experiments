#!/usr/bin/env python3
"""
Comprehensive python-dotenv behavior experiment.
Tests all aspects of dotenv file handling in one place.
"""

import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv, set_key, unset_key, find_dotenv, dotenv_values

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def print_env_vars(prefix=""):
    """Print environment variables with a prefix filter."""
    print(f"\nEnvironment variables with prefix '{prefix}':")
    for key, value in sorted(os.environ.items()):
        if key.startswith(prefix):
            print(f"  {key}={value}")

def create_test_dotenv():
    """Create a comprehensive test .env file."""
    content = """# This is a comment at the top
# Another comment

# Basic variables
SIMPLE_STRING=hello world
SIMPLE_NUMBER=42
SIMPLE_BOOLEAN=true

# Variables with spaces and special characters
SPACED_VALUE=hello world with spaces
QUOTED_VALUE="quoted string"
SINGLE_QUOTED='single quoted'
MIXED_QUOTES="mixed 'quotes'"

# Empty and whitespace values
EMPTY_VALUE=
WHITESPACE_VALUE=   
TAB_VALUE=	tabbed

# Variables with equals signs
EQUALS_IN_VALUE=key=value
MULTIPLE_EQUALS=a=b=c=d

# Interpolation (if supported)
BASE_URL=https://api.example.com
API_URL=${BASE_URL}/v1
FULL_URL=${API_URL}/users

# Comments after values
VALUE_WITH_COMMENT=test # inline comment
VALUE_WITH_HASH=test#value

# Multiline values (if supported)
MULTILINE="line1
line2
line3"

# Special characters
SPECIAL_CHARS=!@#$%^&*()_+-=[]{}|;':\",./<>?

# Unicode
UNICODE_VALUE=你好世界
EMOJI_VALUE=🚀🌟

# Numbers and booleans
INTEGER_VALUE=123
FLOAT_VALUE=3.14159
NEGATIVE_VALUE=-42
SCIENTIFIC_VALUE=1.23e-4

# Boolean variations
BOOL_TRUE=true
BOOL_FALSE=false
BOOL_1=1
BOOL_0=0
BOOL_YES=yes
BOOL_NO=no

# End comment
# This is a comment at the end
"""
    return content

def test_basic_loading():
    """Test basic dotenv loading behavior."""
    print_section("BASIC LOADING BEHAVIOR")
    
    # Create test .env file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(create_test_dotenv())
        env_file = f.name
    
    try:
        # Test load_dotenv
        print(f"Loading .env file: {env_file}")
        result = load_dotenv(env_file)
        print(f"load_dotenv returned: {result}")
        
        # Show loaded variables
        print_env_vars("SIMPLE_")
        print_env_vars("QUOTED_")
        print_env_vars("EMPTY_")
        print_env_vars("UNICODE_")
        
        # Test dotenv_values
        print(f"\ndotenv_values result:")
        values = dotenv_values(env_file)
        for key, value in list(values.items())[:10]:  # Show first 10
            print(f"  {key}={repr(value)}")
        
    finally:
        os.unlink(env_file)

def test_set_unset_behavior():
    """Test set_key and unset_key behavior."""
    print_section("SET/UNSET BEHAVIOR")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("EXISTING_VAR=original_value\n")
        env_file = f.name
    
    try:
        # Test set_key
        print(f"Original file content:")
        with open(env_file, 'r') as f:
            print(f.read())
        
        print(f"\nSetting NEW_VAR=test_value")
        set_key(env_file, "NEW_VAR", "test_value")
        
        print(f"Setting EXISTING_VAR=updated_value")
        set_key(env_file, "EXISTING_VAR", "updated_value")
        
        print(f"\nAfter set_key operations:")
        with open(env_file, 'r') as f:
            print(f.read())
        
        # Test unset_key
        print(f"\nUnsetting NEW_VAR")
        unset_key(env_file, "NEW_VAR")
        
        print(f"After unset_key operation:")
        with open(env_file, 'r') as f:
            print(f.read())
        
    finally:
        os.unlink(env_file)

def test_comment_preservation():
    """Test comment preservation during modifications."""
    print_section("COMMENT PRESERVATION")
    
    content = """# Header comment
VAR1=value1
# Middle comment
VAR2=value2
# Footer comment
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        env_file = f.name
    
    try:
        print("Original file:")
        with open(env_file, 'r') as f:
            print(f.read())
        
        print("\nAdding VAR3=value3")
        set_key(env_file, "VAR3", "value3")
        
        print("\nAfter adding VAR3:")
        with open(env_file, 'r') as f:
            print(f.read())
        
        print("\nUpdating VAR1=new_value1")
        set_key(env_file, "VAR1", "new_value1")
        
        print("\nAfter updating VAR1:")
        with open(env_file, 'r') as f:
            print(f.read())
        
    finally:
        os.unlink(env_file)

def test_line_placement():
    """Test where new variables are placed."""
    print_section("LINE PLACEMENT BEHAVIOR")
    
    content = """# File start
FIRST_VAR=first
# Middle section
MIDDLE_VAR=middle
# File end
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        env_file = f.name
    
    try:
        print("Original file:")
        with open(env_file, 'r') as f:
            print(f.read())
        
        print("\nAdding multiple variables:")
        set_key(env_file, "NEW_VAR1", "value1")
        set_key(env_file, "NEW_VAR2", "value2")
        set_key(env_file, "NEW_VAR3", "value3")
        
        print("\nAfter adding variables:")
        with open(env_file, 'r') as f:
            print(f.read())
        
    finally:
        os.unlink(env_file)

def test_override_behavior():
    """Test override behavior with existing environment variables."""
    print_section("OVERRIDE BEHAVIOR")
    
    # Set some environment variables
    os.environ['TEST_OVERRIDE'] = 'original_env_value'
    os.environ['TEST_OVERRIDE_2'] = 'original_env_value_2'
    
    print("Environment variables before loading .env:")
    print(f"  TEST_OVERRIDE={os.environ.get('TEST_OVERRIDE')}")
    print(f"  TEST_OVERRIDE_2={os.environ.get('TEST_OVERRIDE_2')}")
    
    content = """TEST_OVERRIDE=dotenv_value
TEST_OVERRIDE_2=dotenv_value_2
TEST_NEW=dotenv_new_value
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        env_file = f.name
    
    try:
        print(f"\nLoading .env with override=False (default):")
        load_dotenv(env_file, override=False)
        print(f"  TEST_OVERRIDE={os.environ.get('TEST_OVERRIDE')}")
        print(f"  TEST_OVERRIDE_2={os.environ.get('TEST_OVERRIDE_2')}")
        print(f"  TEST_NEW={os.environ.get('TEST_NEW')}")
        
        # Reset environment
        os.environ['TEST_OVERRIDE'] = 'original_env_value'
        os.environ['TEST_OVERRIDE_2'] = 'original_env_value_2'
        if 'TEST_NEW' in os.environ:
            del os.environ['TEST_NEW']
        
        print(f"\nLoading .env with override=True:")
        load_dotenv(env_file, override=True)
        print(f"  TEST_OVERRIDE={os.environ.get('TEST_OVERRIDE')}")
        print(f"  TEST_OVERRIDE_2={os.environ.get('TEST_OVERRIDE_2')}")
        print(f"  TEST_NEW={os.environ.get('TEST_NEW')}")
        
    finally:
        os.unlink(env_file)
        # Clean up
        for key in ['TEST_OVERRIDE', 'TEST_OVERRIDE_2', 'TEST_NEW']:
            if key in os.environ:
                del os.environ[key]

def test_parsing_behavior():
    """Test raw parsing behavior using dotenv_values."""
    print_section("PARSING BEHAVIOR")
    
    content = """# Test parsing
SIMPLE=value
QUOTED="quoted value"
SINGLE_QUOTED='single quoted'
UNQUOTED=unquoted value
EMPTY=
SPACES=  spaced value  
TABS=	tabbed	value
COMMENT=value # inline comment
HASH_IN_VALUE=value#with#hashes
EQUALS=key=value=more
MULTILINE="line1
line2"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        env_file = f.name
    
    try:
        print("Raw parsing result using dotenv_values:")
        parsed = dotenv_values(env_file)
        for key, value in parsed.items():
            print(f"  {key}={repr(value)}")
        
    finally:
        os.unlink(env_file)

def test_find_dotenv():
    """Test find_dotenv behavior."""
    print_section("FIND_DOTENV BEHAVIOR")
    
    # Create .env in current directory
    with open('.env', 'w') as f:
        f.write("FIND_TEST=found_in_current_dir\n")
    
    try:
        found = find_dotenv()
        print(f"find_dotenv() returned: {found}")
        
        if found:
            print("File exists and is readable")
            with open(found, 'r') as f:
                print(f"Content: {f.read().strip()}")
        else:
            print("No .env file found")
        
    finally:
        if os.path.exists('.env'):
            os.unlink('.env')

def main():
    """Run all experiments."""
    print("PYTHON-DOTENV COMPREHENSIVE BEHAVIOR EXPERIMENT")
    print("=" * 60)
    
    test_basic_loading()
    test_set_unset_behavior()
    test_comment_preservation()
    test_line_placement()
    test_override_behavior()
    test_parsing_behavior()
    test_find_dotenv()
    
    print_section("EXPERIMENT COMPLETE")
    print("All python-dotenv behaviors have been tested!")

# REAL EXPERIMENT OUTPUTS (captured from actual execution):
"""
PYTHON-DOTENV COMPREHENSIVE BEHAVIOR EXPERIMENT
============================================================

============================================================
 BASIC LOADING BEHAVIOR
============================================================
Loading .env file: /tmp/tmp3j3ie1oa.env
load_dotenv returned: True

Environment variables with prefix 'SIMPLE_':
  SIMPLE_BOOLEAN=true
  SIMPLE_NUMBER=42
  SIMPLE_STRING=hello world

Environment variables with prefix 'QUOTED_':
  QUOTED_VALUE=quoted string

Environment variables with prefix 'EMPTY_':
  EMPTY_VALUE=

Environment variables with prefix 'UNICODE_':
  UNICODE_VALUE=你好世界

dotenv_values result:
  SIMPLE_STRING='hello world'
  SIMPLE_NUMBER='42'
  SIMPLE_BOOLEAN='true'
  SPACED_VALUE='hello world with spaces'
  QUOTED_VALUE='quoted string'
  SINGLE_QUOTED='single quoted'
  MIXED_QUOTES="mixed 'quotes'"
  EMPTY_VALUE=''
  WHITESPACE_VALUE=''
  TAB_VALUE='tabbed'

============================================================
 SET/UNSET BEHAVIOR
============================================================
Original file content:
EXISTING_VAR=original_value

Setting NEW_VAR=test_value
Setting EXISTING_VAR=updated_value

After set_key operations:
EXISTING_VAR='updated_value'
NEW_VAR='test_value'

Unsetting NEW_VAR
After unset_key operation:
EXISTING_VAR='updated_value'

============================================================
 COMMENT PRESERVATION
============================================================
Original file:
# Header comment
VAR1=value1
# Middle comment
VAR2=value2
# Footer comment

Adding VAR3=value3

After adding VAR3:
# Header comment
VAR1=value1
# Middle comment
VAR2=value2
# Footer comment
VAR3='value3'

Updating VAR1=new_value1

After updating VAR1:
# Header comment
VAR1='new_value1'
# Middle comment
VAR2=value2
# Footer comment
VAR3='value3'

============================================================
 LINE PLACEMENT BEHAVIOR
============================================================
Original file:
# File start
FIRST_VAR=first
# Middle section
MIDDLE_VAR=middle
# File end

Adding multiple variables:

After adding variables:
# File start
FIRST_VAR=first
# Middle section
MIDDLE_VAR=middle
# File end
NEW_VAR1='value1'
NEW_VAR2='value2'
NEW_VAR3='value3'

============================================================
 OVERRIDE BEHAVIOR
============================================================
Environment variables before loading .env:
  TEST_OVERRIDE=original_env_value
  TEST_OVERRIDE_2=original_env_value_2

Loading .env with override=False (default):
  TEST_OVERRIDE=original_env_value
  TEST_OVERRIDE_2=original_env_value_2
  TEST_NEW=dotenv_new_value

Loading .env with override=True:
  TEST_OVERRIDE=dotenv_value
  TEST_OVERRIDE_2=dotenv_value_2
  TEST_NEW=dotenv_new_value

============================================================
 PARSING BEHAVIOR
============================================================
Raw parsing result using dotenv_values:
  SIMPLE='value'
  QUOTED='quoted value'
  SINGLE_QUOTED='single quoted'
  UNQUOTED='unquoted value'
  EMPTY=''
  SPACES='spaced value'
  TABS='tabbed\tvalue'
  COMMENT='value'
  HASH_IN_VALUE='value#with#hashes'
  EQUALS='key=value=more'
  MULTILINE='line1\nline2'

============================================================
 FIND_DOTENV BEHAVIOR
============================================================
find_dotenv() returned: /workspace/experiments/dotenv-files/python-dotenv/.env
File exists and is readable
Content: FIND_TEST=found_in_current_dir

============================================================
 EXPERIMENT COMPLETE
============================================================
All python-dotenv behaviors have been tested!
"""

if __name__ == "__main__":
    main()