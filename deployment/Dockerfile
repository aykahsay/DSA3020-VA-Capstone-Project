# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# copy project files
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# default command runs streamlit app (app/main.py)
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
