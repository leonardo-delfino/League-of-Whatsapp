# League of WhatsApp
A League of Legends match can last a different amount of time. You can finish in 20 minutes, 
or it can take up to an hour. <br>
While playing is really hard to get distracted by your smartphone. As a result, you won't be
able to check the messages on messaging services like WhatsApp. <br>
However, you can still receive a message from a friend inside the League's client (from a 
RiotGames account), and it will be shown in game. You can also reply to that message directly
from the match (by typing in the chat /msg "name of the account" your message). <br>
The purpose of this script is to allow the reception (real-time) and response of the messages
from a WhatsApp contact during a League of Legends match.

## How to install
Still developing.

## How does it work
Before executing the script, you have to create another RiotGames account (in the same region
of the one you want to use for the reception / response of the messages). After creating it, 
just send a friend request to your real account. After that, you can run the script.

You have to insert two usernames: the one to receive messages from (in the way it is stored 
on the smartphone), and your personal Whatsapp name. <br>
You can check your WhatsApp name from Menu (the three dots) -> Settings.

You will be now able to receive (it is assumed that every message before your last one have 
already been read) all the text messages (you will also able to reply to them) from the user
you have inserted directly into your match.

To let the script work correctly, you have to open two instances of League of Legends. <br>
To do so you have to add the string "--allow-multiple-clients" (without the double quotation
marks) in the "Target" field that you can find in the "Shortcut" tab of your link to the League
of Legends executable. <br>
You can see from the image below where you have to add the line of code 
(sorry for the italian):
<p align="center">
  <img src="img/properties.png" />
</p>

## Supported messaging services
By now, only WhatsApp is supported. I plan to also add Telegram once the development for 
Whatsapp is finished.

## TODO
 * ~~Get the input and convert it to ASCII;~~
 * ~~Get the text messages from the user until your last one;~~
 * ~~Get also the images and the vocal messages;~~
 * ~~Send the messages to a RiotGames account;~~
 * ~~Send the messages from the RiotGames account to your personal account;~~
 * Reply to the messages directly from the match;
 * Send the messages from the RiotGames account back to the WhatsApp contact.

## License
The software has the [MIT license](https://choosealicense.com/licenses/mit/). Feel free to use it or to contribute to it.
