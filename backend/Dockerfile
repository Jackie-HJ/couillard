FROM selenium/standalone-chrome
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
USER seluser
WORKDIR /home/seluser
COPY . .
CMD ["--selenium-manager", "true"]
# CMD ["python3", "generate_daily_data.py"]