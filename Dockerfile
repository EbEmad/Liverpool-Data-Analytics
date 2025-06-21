FROM python:3.9-slim

# Set environment variables
 # to prevent .py files from being written to disk
ENV PYTHONDONTWRITEBYTECODE=1
# to ensure that the output of Python is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app/
CMD [ "python","./src/scrap.py" ]

