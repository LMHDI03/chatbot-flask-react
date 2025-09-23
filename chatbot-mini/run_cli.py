from chatbot.bot import ChatBot

if __name__ == "__main__":
    bot = ChatBot()
    print("Bot 🤖: Bonjour ! (tape 'exit' pour quitter)")

    while True:
        msg = input("Vous: ").strip()
        if msg.lower() in ["exit", "quit"]:
            print("Bot 🤖: Au revoir 👋")
            break
        print("Bot 🤖:", bot.handle(msg))
