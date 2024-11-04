FROM python:3.11-slim

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["python", "src/main.py"]