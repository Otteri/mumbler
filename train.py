import argparse
import nlp

# A helper script for user

def getArgs():
    parser = argparse.ArgumentParser(description='Training arguments')
    parser.add_argument("--useGpu", action="store_true", help="Uses GPU instead of CPU (supports one GPU)")
    parser.add_argument("--load", action="store_true", default=None, help="Load weights")
    parser.add_argument("--save_every", default=5000, type=int, help="save weight and print statistics every N")
    parser.add_argument("--epochs", default=10000, type=int, help="Number of training iterations")
    parser.add_argument("--path", type=str, required=True, help="Where weights are stored?") # Tip: store into same folder as data
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = getArgs()

    device = "cpu"
    if args.useGpu:
        device = "cuda"

    if args.load is None:
        ans = input("Are you sure you want to start training over again? Ctrl+C to cancel and use '--load' next time!")
        training_settings = nlp.TrainingSettings(
                                data_path=args.path,
                                load_model=False,
                                device=device,
                                epochs=args.epochs,
                                save_every=args.save_every
                            )
    else:
        # map args to settings-class
        training_settings = nlp.TrainingSettings(
                                data_path=args.path,
                                load_model=args.load,
                                device=device,
                                epochs=args.epochs,
                                save_every=args.save_every
                            )

    nlp.runTraining(training_settings)
