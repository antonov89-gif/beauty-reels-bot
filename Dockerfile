# The bot itself is Python (aiogram), but real Reels rendering runs through
# the HyperFrames CLI, which needs Node.js, FFmpeg, and a headless Chrome --
# none of which a plain Python buildpack provides. This image installs both
# runtimes so VideoRenderAgent (reels_mvp.py) actually works in production.
FROM node:22-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ffmpeg \
        unzip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pin the same HyperFrames version used in reels-video/ so renders stay
# reproducible; bump both together if you upgrade.
RUN npm install -g hyperframes@0.8.68 \
    && hyperframes browser ensure

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "reels_mvp.py"]
