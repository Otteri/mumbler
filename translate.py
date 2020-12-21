import sys
import nlp
import argparse

# A helper script which allows to run nlp network without the bot.
# Uses echo flag, which also produces more info useful for debugging.


def getArgs():
    parser = argparse.ArgumentParser(description='Translation arguments')
    parser.add_argument("--input", default=None, type=str, help="Str to be translated")    
    parser.add_argument("--path", default="data1/", type=str, help="Where to load weights? (include trailin slash)")
    parser.add_argument("--verbose", action="store_true", help="Prints additional info")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = getArgs()

    data_path = args.path

    if args.input is not None:
        user_input = args.input
    else:
        user_input = input("Give input (eng) > ").lower().strip()

    print("Using data path: ", data_path)

    if args.verbose:
        output = nlp.translate(user_input, max_length=50, verbose=True, data_path=data_path)
    else:
        output = nlp.translate(user_input, max_length=50, verbose=False, data_path=data_path)


    if output is 1:
        print("Error!")
    if output is 2:
        nlp.teachSentence(user_input, data_path=data_path)
    else: # normal case
        print(output)
