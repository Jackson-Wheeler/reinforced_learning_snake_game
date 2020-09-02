# Other modules
import sys

def main():
    game_type = input("Would you like to run the 'Human', 'Training', or 'AI' file? ")
    if game_type == "Human":
        import human
        human.main()
    elif game_type == "AI":
        import ai
        ai.main()
    elif game_type == "Training":
        import training
        training.main()
    else:
        print("INVALID GAME TYPE ENTERED")

if __name__== "__main__":
    main()

