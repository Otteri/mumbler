FROM nvcr.io/nvidia/pytorch:20.11-py3

# Update system and install deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/

# Install discord related stuff
RUN pip install -U pip && \
    pip install discord.py -q --retries 5 && \
    pip install python-dotenv -q --retries 5 && \
    rm -rf /root/.cache/pip/*

# copy project sources from repo or mount dir

WORKDIR /workspace/nlp

#CMD ["python3 bot.py"]
