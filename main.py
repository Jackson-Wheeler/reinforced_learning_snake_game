

def main():
    game_type = input("Enter what you want to run: 'Human', 'Ai', or 'Training': ")
    if game_type == "Human":
        import human
        human.main()
    elif game_type == "Ai":
        import ai
        ai.main()
    elif game_type == "Training":
        import training
        training.main()
    else:
        print("INVALID GAME TYPE ENTERED")

if __name__== "__main__":
    main()

