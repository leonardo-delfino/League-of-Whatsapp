from messages_parsers.WhatsAppParser import WhatsAppParser
from league_requests.LeagueOfLegendsClient import LeagueOfLegendsClient

if __name__ == '__main__':
    # TODO: save everything in a file (choose between file or arguments)
    user_alias = input("[*] Enter the username (in the way it is stored on your smartphone) you want to receive "
                       "messages from (with the emojis too): ")
    personal_alias = input("[*] Enter your WhatsApp name (the name visible to your WhatsApp contacts): ")

    league_path = input("[*] Enter the path of Leagues' executable: ")
    bot_name = input("[*] Enter the name of the account that will act as a proxy: ")

    whatsapp_parser = WhatsAppParser(user_alias, personal_alias)
    messages = whatsapp_parser.get_messages()

    league_manager = LeagueOfLegendsClient(league_path, bot_name)
    league_manager.parse_lockfile()

    """
    for message in messages:
        # TODO: every message is a list. Extract the messages from it, and send them
        league_manager.send_message(message)
    """
    league_manager.send_message("test")

    whatsapp_parser.close()
