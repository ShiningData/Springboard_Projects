# Core dependencies
fastapi==0.104.1
uvicorn==0.23.2
pydantic==2.4.2

# Type hints and validation
typing-extensions==4.8.0

# Logging and monitoring
python-json-logger==2.0.7

# Performance optimization
orjson==3.9.10  # For faster JSON serialization
cachetools==5.3.1  # For caching frequently used functions

# Optional performance dependencies (Unix-like systems only)
# uvloop==0.17.0  # For faster event loop implementation
# httptools==0.5.0  # For faster HTTP protocol implementation

# Development dependencies
pytest==7.4.3
pytest-asyncio==0.21.1  # For testing FastAPI applications
httpx==0.25.1
black==23.10.1  # For code formatting
isort==5.12.0  # For import sorting
mypy==1.6.1  # For static type checking 
