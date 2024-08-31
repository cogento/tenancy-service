FROM 913524902957.dkr.ecr.us-west-2.amazonaws.com/cogento/cogento-base:0.0.1

# Install the required packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Install shared libraries
RUN pip install app/shared

COPY . /app
WORKDIR /app

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]