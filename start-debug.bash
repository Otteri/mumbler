# Try to build
docker build -f Dockerfile.debug -t mumbler:debug .

# Launch image
docker run \
-it \
--rm \
--gpus all \
--mount type=bind,source="$(pwd)"/mumbler,target=/app/ParlAI/parlai_internal/mumbler \
--mount type=bind,source="$(pwd)"/agents,target=/app/ParlAI/parlai_internal/mumbler/agents \
--mount type=bind,source="$(pwd)"/models,target=/app/ParlAI/parlai_internal/models \
--mount type=bind,source="$(pwd)"/tasks,target=/app/ParlAI/parlai_internal/tasks \
mumbler:debug
