# DiscordGPT
This is a package to use ChatGPT in Discord.

## Installation
You can download the source here, or use `pip` to install the package: 
```
pip install discordgpt
```

## Usage, examples
You can use the `DiscordGPT` class to make a ChatGPT bot:
```py
from discordgpt import DiscordGPT

DiscordGPT(token="your bot token", api_key="your openai api key", channel_id="a channel id for the chat")
```
This creates a ChatGPT bot that responds when someone sends a message in the specified channel id.

You can customize it further by creating a class with DiscordGPT as its superclass:
```py
from discordgpt import DiscordGPT

class MyDiscordGPT(DiscordGPT):
      def __init__(self): super().__init__(token="bot token", api_key="openai api key", channel_id="a channel id", <more options if you need>)
      async def new_question(self, message):
        # you can really do anything here, a bad word checker is just an example
        if "a bad word" in message.content: return await message.channel.send("Don't say bad words to ChatGPT!")
        await super().new_question(message)

MyDiscordGPT()
```
This will create a bad word blocker for DiscordGPT.
If you want to customize it _even further_, you can overwrite the whole process:
```py
from discordgpt import DiscordGPT
import discord
class MyDiscordGPT(DiscordGPT):
      def __init__(self): super().__init__(token="bot token", api_key="openai api key", channel_id="a channel id", <more options if you need>)
      async def new_question(self, message):
        response = super().get_response(message) # gets ChatGPT's response
        await message.channel.send(embed=discord.Embed(title="ChatGPT said:", description=response))

MyDiscordGPT()
```
That makes an embed get sent. But keep in mind, this does not do things like log the new messages or send a typing indicator. You can do that yourself, docs are [here](https://discordpy.readthedocs.io).

## Documentation

### `discordgpt.DiscordGPT(token: str, api_key: str, channel_id: Union[int, str], channel_name: str, model: str, prompt: str, message_to_send: str, logger: bool)`

This makes a new Discord ChatGPT bot.

### Parameters
- `token` - Your Discord bot token.
- `api_key` - Your OpenAI API key.
- `channel_id` - The channel id for the bot to check for messages. Can be empty if `channel_name` is passed. Default is `None`.
- `channel_name` - The channel name for the bot to check for messages. Can be empty if `channel_id` is passed. Default is `None`.
- `model` - The model to use. Default is `text-davinci-003` which is also the best model for completions, but you can specify yours (fine-tunes also work)
- `prompt` - The prompt to give ChatGPT. Default is `"User: {message}\n\nAssistant:\n\n"`. If you give it a custom prompt, put `{message}` where you want the message content to be.
- `message_to_send` - The message to be sent in the channel. Default is `"{response}"`. If you give it a custom message, put `{response}` where you want ChatGPT's response to be.
- `logger` - Whether DiscordGPT should log events like when the bot goes up, when a new message is sent and the response. Default is `True`, can be turned off (by `False`).

### Raises
- `GPTError`, which is just a class for various exceptions, such as `{message}` or `{response}` missing, or `channel_id` and `channel_name` missing.

### Methods
- `new_question` - runs when a message is sent in the right channel. Accepts `message` (which is a `discord.Message` instance) from which it gets the content and author.
- `get_response` - runs when the code needs ChatGPT's response to the message. It also accepts `message` as an argument, it's also a `discord.Message` instance, and it uses it for the content.

All of those are customizable. There's also `_log` which takes a colorama's Style attribute and the text to log, in case you ever need it.

## That should be it!
If you don't know how to get an API key, get it [here](https://platform.openai.com/account/api-keys).

If you don't know how to make a bot and get its token, you can do that [here](https://discord.com/developers). There's a lot of tutorials online, if anything's not clear.

Keep in mind that OpenAI is not free forever and even if ChatGPT is free on https://chat.openai.com, it's not free forever in the API. You get $5 for free when registering, and you should be good for quite a while. The pricing list is [here](https://openai.com/pricing) (we don't use gpt-4 or gpt-3.5 turbo btw, we use davinci which is the best single reply gpt-3 model). If you don't know what a token is, you can check and test it [here](https://platform.openai.com/tokenizer).

# Happy GPTing!