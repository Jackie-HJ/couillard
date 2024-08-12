FROM selenium/standalone-chrome
USER root
RUN apt-get update && apt-get install -y python3-full pipx
RUN pipx ensurepath
RUN pipx install mkdocs
COPY requirements.txt .
RUN cat requirements.txt | xargs pipx inject mkdocs
USER seluser
WORKDIR /home/seluser
COPY . .
CMD ["python3", "generate_daily_data.py"]
