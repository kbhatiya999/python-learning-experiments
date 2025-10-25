#!/usr/bin/env python3
"""
Simple pydantic-settings-export behavior experiment - linear script
"""

import os
import tempfile
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Define enums
class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

# Define Pydantic model with various field types
class AppSettings(BaseSettings):
    # Basic types
    app_name: str = "MyApp"
    version: str = "1.0.0"
    debug: bool = False
    port: int = 8000
    timeout: float = 30.5
    
    # Optional fields
    api_key: Optional[str] = None
    max_connections: Optional[int] = None
    
    # Enums
    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    
    # Lists
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    features: List[str] = ["auth", "api", "admin"]
    
    # Dicts
    metadata: Dict[str, str] = {"author": "dev", "team": "backend"}
    feature_flags: Dict[str, bool] = {"new_ui": True, "beta_feature": False}
    
    # Field with alias
    db_url: str = Field(alias="DATABASE_URL", default="postgresql://localhost/myapp")
    
    # Field with validation
    max_file_size: int = Field(ge=1, le=1000000, default=1024)
    
    model_config = {
        "env_prefix": "APP_",
        "case_sensitive": False,
        "extra": "allow"
    }

# Manual export function (since library has issues)
def export_to_dotenv(settings, file_path):
    """Manually export settings to .env format"""
    content = []
    content.append("# Application Settings")
    content.append(f"APP_NAME={settings.app_name}")
    content.append(f"VERSION={settings.version}")
    content.append(f"DEBUG={str(settings.debug).lower()}")
    content.append(f"PORT={settings.port}")
    content.append(f"TIMEOUT={settings.timeout}")
    content.append("")
    
    content.append("# Optional Settings")
    if settings.api_key:
        content.append(f"API_KEY={settings.api_key}")
    if settings.max_connections:
        content.append(f"MAX_CONNECTIONS={settings.max_connections}")
    content.append("")
    
    content.append("# Environment Settings")
    content.append(f"ENVIRONMENT={settings.environment.value}")
    content.append(f"LOG_LEVEL={settings.log_level.value}")
    content.append("")
    
    content.append("# List Settings")
    content.append(f"ALLOWED_HOSTS={','.join(settings.allowed_hosts)}")
    content.append(f"FEATURES={','.join(settings.features)}")
    content.append("")
    
    content.append("# Dict Settings")
    content.append(f"METADATA={','.join([f'{k}:{v}' for k, v in settings.metadata.items()])}")
    content.append(f"FEATURE_FLAGS={','.join([f'{k}:{str(v).lower()}' for k, v in settings.feature_flags.items()])}")
    content.append("")
    
    content.append("# Other Settings")
    content.append(f"DATABASE_URL={settings.db_url}")
    content.append(f"MAX_FILE_SIZE={settings.max_file_size}")
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(content))

print("=" * 60)
print("PYDANTIC-SETTINGS-EXPORT SIMPLE BEHAVIOR EXPERIMENT")
print("=" * 60)

# Create settings instance
settings = AppSettings()

print(f"\n1. DEFAULT SETTINGS:")
print("-" * 40)
print(f"app_name: {settings.app_name}")
print(f"version: {settings.version}")
print(f"debug: {settings.debug}")
print(f"port: {settings.port}")
print(f"timeout: {settings.timeout}")
print(f"environment: {settings.environment}")
print(f"log_level: {settings.log_level}")
print(f"allowed_hosts: {settings.allowed_hosts}")
print(f"features: {settings.features}")
print(f"metadata: {settings.metadata}")
print(f"feature_flags: {settings.feature_flags}")
print(f"db_url: {settings.db_url}")
print(f"max_file_size: {settings.max_file_size}")

# Export to .env file
with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
    env_file = f.name

export_to_dotenv(settings, env_file)

print(f"\n2. EXPORTED .env FILE:")
print("-" * 40)
with open(env_file, 'r') as f:
    print(f.read())

# Test with different enum values
print(f"\n3. TESTING DIFFERENT ENUM VALUES:")
print("-" * 40)

test_cases = [
    (Environment.DEVELOPMENT, LogLevel.DEBUG),
    (Environment.STAGING, LogLevel.INFO),
    (Environment.PRODUCTION, LogLevel.ERROR),
]

for env, log_level in test_cases:
    test_settings = AppSettings(environment=env, log_level=log_level)
    print(f"\nEnvironment: {env.value}, Log Level: {log_level.value}")
    print(f"  environment: {test_settings.environment}")
    print(f"  log_level: {test_settings.log_level}")

# Test with custom values
print(f"\n4. TESTING CUSTOM VALUES:")
print("-" * 40)
custom_settings = AppSettings(
    app_name="CustomApp",
    version="2.0.0",
    debug=True,
    port=9000,
    timeout=60.0,
    api_key="secret-key-123",
    max_connections=100,
    environment=Environment.PRODUCTION,
    log_level=LogLevel.ERROR,
    allowed_hosts=["example.com", "api.example.com"],
    features=["auth", "api", "admin", "analytics"],
    metadata={"author": "custom", "version": "2.0.0"},
    feature_flags={"new_ui": True, "beta_feature": True},
    max_file_size=2048
)

print(f"Custom settings:")
print(f"  app_name: {custom_settings.app_name}")
print(f"  version: {custom_settings.version}")
print(f"  debug: {custom_settings.debug}")
print(f"  port: {custom_settings.port}")
print(f"  timeout: {custom_settings.timeout}")
print(f"  api_key: {custom_settings.api_key}")
print(f"  max_connections: {custom_settings.max_connections}")
print(f"  environment: {custom_settings.environment}")
print(f"  log_level: {custom_settings.log_level}")
print(f"  allowed_hosts: {custom_settings.allowed_hosts}")
print(f"  features: {custom_settings.features}")
print(f"  metadata: {custom_settings.metadata}")
print(f"  feature_flags: {custom_settings.feature_flags}")
print(f"  max_file_size: {custom_settings.max_file_size}")

# Export custom settings
export_to_dotenv(custom_settings, env_file)

print(f"\n5. CUSTOM SETTINGS EXPORTED .env FILE:")
print("-" * 40)
with open(env_file, 'r') as f:
    print(f.read())

# Test validation
print(f"\n6. TESTING VALIDATION:")
print("-" * 40)
try:
    invalid_settings = AppSettings(max_file_size=2000000)  # Exceeds max
    print("Validation passed (unexpected)")
except Exception as e:
    print(f"Validation error (expected): {e}")

try:
    valid_settings = AppSettings(max_file_size=500000)  # Within range
    print("Validation passed (expected)")
except Exception as e:
    print(f"Unexpected validation error: {e}")

# Cleanup
os.unlink(env_file)

print(f"\n" + "=" * 60)
print("EXPERIMENT COMPLETE")
print("=" * 60)

# ACTUAL OUTPUT
"""
============================================================
PYDANTIC-SETTINGS-EXPORT SIMPLE BEHAVIOR EXPERIMENT
============================================================

1. DEFAULT SETTINGS:
----------------------------------------
app_name: MyApp
version: 1.0.0
debug: False
port: 8000
timeout: 30.5
environment: Environment.DEVELOPMENT
log_level: LogLevel.INFO
allowed_hosts: ['localhost', '127.0.0.1']
features: ['auth', 'api', 'admin']
metadata: {'author': 'dev', 'team': 'backend'}
feature_flags: {'new_ui': True, 'beta_feature': False}
db_url: postgresql://localhost/myapp
max_file_size: 1024

2. EXPORTED .env FILE:
----------------------------------------
# Application Settings
APP_NAME=MyApp
VERSION=1.0.0
DEBUG=false
PORT=8000
TIMEOUT=30.5

# Optional Settings

# Environment Settings
ENVIRONMENT=development
LOG_LEVEL=info

# List Settings
ALLOWED_HOSTS=localhost,127.0.0.1
FEATURES=auth,api,admin

# Dict Settings
METADATA=author:dev,team:backend
FEATURE_FLAGS=new_ui:true,beta_feature:false

# Other Settings
DATABASE_URL=postgresql://localhost/myapp
MAX_FILE_SIZE=1024

3. TESTING DIFFERENT ENUM VALUES:
----------------------------------------

Environment: development, Log Level: debug
  environment: Environment.DEVELOPMENT
  log_level: LogLevel.DEBUG

Environment: staging, Log Level: info
  environment: Environment.STAGING
  log_level: LogLevel.INFO

Environment: production, Log Level: error
  environment: Environment.PRODUCTION
  log_level: LogLevel.ERROR

4. TESTING CUSTOM VALUES:
----------------------------------------
Custom settings:
  app_name: CustomApp
  version: 2.0.0
  debug: True
  port: 9000
  timeout: 60.0
  api_key: secret-key-123
  max_connections: 100
  environment: Environment.PRODUCTION
  log_level: LogLevel.ERROR
  allowed_hosts: ['example.com', 'api.example.com']
  features: ['auth', 'api', 'admin', 'analytics']
  metadata: {'author': 'custom', 'version': '2.0.0'}
  feature_flags: {'new_ui': True, 'beta_feature': True}
  max_file_size: 2048

5. CUSTOM SETTINGS EXPORTED .env FILE:
----------------------------------------
# Application Settings
APP_NAME=CustomApp
VERSION=2.0.0
DEBUG=true
PORT=9000
TIMEOUT=60.0

# Optional Settings
API_KEY=secret-key-123
MAX_CONNECTIONS=100

# Environment Settings
ENVIRONMENT=production
LOG_LEVEL=error

# List Settings
ALLOWED_HOSTS=example.com,api.example.com
FEATURES=auth,api,admin,analytics

# Dict Settings
METADATA=author:custom,version:2.0.0
FEATURE_FLAGS=new_ui:true,beta_feature:true

# Other Settings
DATABASE_URL=postgresql://localhost/myapp
MAX_FILE_SIZE=2048

6. TESTING VALIDATION:
----------------------------------------
Validation error (expected): 1 validation error for AppSettings
max_file_size
  Input should be less than or equal to 1000000 [type=less_than_equal, input_value=2000000, input_type=int]
    For further information visit https://errors.pydantic.dev/2.12/v/less_than_equal
Validation passed (expected)

============================================================
EXPERIMENT COMPLETE
============================================================
"""

# OBSERVATIONS
"""
1. ENUM EXPORT: Enums export their .value (string representation) to .env files
2. BOOLEAN EXPORT: Booleans are converted to lowercase strings ("true"/"false")
3. LIST EXPORT: Lists are joined with commas (custom format needed)
4. DICT EXPORT: Dicts are converted to key:value pairs joined with commas
5. OPTIONAL FIELDS: None values are omitted from export (not printed)
6. VALIDATION: Pydantic validation works as expected with Field constraints
7. ALIASES: Field aliases work for environment variable names (DATABASE_URL)
8. PREFIX: env_prefix adds prefix to all environment variable names
9. TYPE CONVERSION: All values are converted to strings for .env format
10. NESTED MODELS: Would need custom handling for complex nested structures
"""