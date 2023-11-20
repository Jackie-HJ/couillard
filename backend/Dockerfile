FROM selenium/standalone-chrome

USER root

# Install python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python packages from requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Switch back to the selenium user
USER seluser

# Set the working directory
WORKDIR /home/seluser

# Copy the current directory contents into the container at /home/seluser
COPY . .

# Specify the default command to run when the container starts
CMD ["python3", "script.py"]