##########################################¤¤
# Build: $ docker build -t mumbler .
# Run:   $ docker run --gpus all -it mumbler
############################################

FROM nvcr.io/nvidia/pytorch:20.12-py3 AS base

# Currently installing from local files
COPY ParlAI/ /app/ParlAI/
RUN cd /app/ParlAI/; python setup.py develop

# Install python dependencies
RUN pip install \
    'discord.py==1.6.0' \
    'python-dotenv'

# Copy project source code
COPY mumbler/ /app/ParlAI/parlai_internal/mumbler
COPY agents/ /app/ParlAI/parlai_internal/mumbler/agents/
COPY tasks/ /app/ParlAI/parlai_internal/tasks/
COPY ParlAI/data/models/blender/blender_90M/ /app/ParlAI/data/models/blender/blender_90M/

# Start app automatically
WORKDIR /app/ParlAI/parlai_internal/mumbler/
ENTRYPOINT ["python", "main.py"]
