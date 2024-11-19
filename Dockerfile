FROM rendyprojects/python:latest

WORKDIR /app
WORKDIR /.cache

RUN apt -qq update && \
    apt -qq install -y --no-install-recommends \
    ffmpeg \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libappindicator3-1 \
    libxrender1 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libxss1 \
    fonts-liberation \
    libasound2 \
    libgbm-dev \
    libu2f-udev \
    libvulkan1 \
    libgl1-mesa-dri \
    xdg-utils \
    python3-dev \
    python3-pip \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    chromium \
    chromium-driver \
    neofetch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

COPY . .
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools==59.6.0
RUN pip3 install -r requirements.txt

RUN mkdir -p /app /.cache
RUN chown -R 1000:0 /app /.cache
RUN chmod -R 777 /app /.cache


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]