from get_messages.MessagesParser import MessagesParser


if __name__ == '__main__':
    user_alias = input("[*] Enter the username (in the way it is stored on your smartphone) you want to receive "
                       "messages from (with the emojis too): ")
    personal_alias = input("[*] Enter your WhatsApp name (the name visible to your WhatsApp contacts): ")
    parser = MessagesParser(user_alias, personal_alias)
    parser.get_messages()
    parser.close()
