import os
from parlai_internal.mumbler import config as cfg

# python talk.py -t internal:blended_skill_talk -mf zoo:blender/blender_90M/model
# use izoo:xyz for custom model

if __name__ == "__main__":
    discord2agent = cfg.PIPE_DISCORD2AGENT
    agent2discord = cfg.PIPE_AGENT2DISCORD

    # Make sure that env is clean
    if os.path.exists(discord2agent):
        os.remove(discord2agent)
    if os.path.exists(agent2discord):
        os.remove(agent2discord)

    # Create pipes
    fifo2 = os.mkfifo(agent2discord)
    fifo = os.mkfifo(discord2agent)

    # Open pipes 
    fifo2 = os.open(agent2discord, os.O_RDONLY)
    fifo = os.open(discord2agent, os.O_SYNC | os.O_CREAT | os.O_RDWR)

    while True:
        text = input("Give string input: ")
        if text is "exit":
            break
        content = f"{text}!".encode("utf8")
        os.write(fifo, content)

        # Recieve data (blocking: waits until gets response)
        response = os.read(fifo2, 512).decode('utf-8')
        print(response)

    os.close(fifo)
