# Our modules
import human, training, ai
# Other modules
import sys

def main():
    game_type = input("Would you like to run the 'Human', 'Training', or 'AI' file? ")
    if game_type == "Human":
        human.main()
    elif game_type == "AI":
        ai.main()
    elif game_type == "Training":
        training.main()
    else:
        print("INVALID GAME TYPE ENTERED")

if __name__== "__main__":
    main()

