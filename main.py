# Our modules
import human_play
# Other modules
import sys


def main():
    game_type = str(sys.argv[1])
    if game_type == "Human":
        human_play.main()
    elif game_type == "AI":
        pass
    elif game_type == "Training":
        pass
    else:
        print("INVALID GAME TYPE ENTERED")

if __name__== "__main__":
    main()

