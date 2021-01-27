import os

# A helper script that can be used for debugging

if __name__ == "__main__":
    IPC_FIFO_NAME =  "/tmp/discord2agent"
    IPC_FIFO_NAME2 = "/tmp/agent2discord"

    # Make sure that env is clean
    if os.path.exists(IPC_FIFO_NAME):
        os.remove(IPC_FIFO_NAME)
    if os.path.exists(IPC_FIFO_NAME2):
        os.remove(IPC_FIFO_NAME2)

    # Create pipes
    fifo2 = os.mkfifo(IPC_FIFO_NAME2)
    fifo = os.mkfifo(IPC_FIFO_NAME)

    # Open pipes 
    fifo2 = os.open(IPC_FIFO_NAME2, os.O_RDONLY)
    fifo = os.open(IPC_FIFO_NAME, os.O_SYNC | os.O_CREAT | os.O_RDWR)

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
