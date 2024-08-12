FROM selenium/standalone-chrome
USER root
RUN apt-get update && apt-get install -y python3-full python3 python3-pip pipx
COPY requirements.txt .
RUN sudo pipx ensurepath
RUN sudo pipx ensurepath --global 
RUN sudo pipx install --global --no-cache-dir -r requirements.txt
USER seluser
WORKDIR /home/seluser
COPY . .
CMD ["python3", "generate_daily_data.py"]
