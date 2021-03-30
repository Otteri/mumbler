# CONFIG

PIPE_DISCORD2AGENT = "/tmp/discord2agent"
PIPE_AGENT2DISCORD = "/tmp/agent2discord"
MSG_LENGTH = 512 # Pipe buffer size

# Model that shall be used
MODEL = "zoo:blender/blender_90M/model"
        #"zoo:blender/blender_1Bdistill/model"
        #"zoo:blender/blender_400Mdistill/model"
        #"/app/ParlAI/parlai_internal/models/vainamoinen_90M"

# Tokens used when discussing with the bot
TALK_PREFIX = ">>"
COMMAND_PREFIX = "-"
