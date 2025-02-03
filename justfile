# Lint the code with ruff
lint:
    ruff check -v

# Check for formatting issues with ruff
format-check:
    ruff format --check -v

# Format the code with ruff
format:
    ruff format -v
