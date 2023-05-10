"""
The package for a Discord ChatGPT bot.
"""
from typing import Union
import discord, openai
from colorama import Fore, Style 
class GPTError(Exception): pass
class DiscordGPT:
  """
    Starts a ChatGPT instance for your Discord bot.
    
    Calling this will create a discord.py client, accessible through the class `client` attribute. You can pass the channel id or the name for the bot to know for which messages it should listen, and also customize the prompt and message to be sent. Example:
    ```py
    from discordgpt import DiscordGPT

    DiscordGPT(token="your bot token", api_key="your openai api key", channel_id="a channel id for the chat")
    ```
    Also, `text-davinci-003` is the most advanced completion model for now, but if you want to change it, pass a different one with the `modal` arg.
    You can customize it further by creating a class with DiscordGPT as its superclass:
    ```py
    from discordgpt import DiscordGPT

    class MyDiscordGPT(DiscordGPT):
      def __init__(self): super().__init__(token="bot token", api_key="openai api key", channel_id="a channel id", <more options if you need>)
      async def new_question(self, message):
        # you can really do anything here, a bad word checker is just an example
        if "a bad word" message.content: return await message.channel.send("Don't say bad words to ChatGPT!")
        await super().new_question(message)

    MyDiscordGPT()
    ```
    This will create a bad word blocker for DiscordGPT.
    If you want to customize it _even further_, you can overwrite the whole process:
    ```py
    from discordgpt import DiscordGPT

    class MyDiscordGPT(DiscordGPT):
      def __init__(self): super().__init__(token="bot token", api_key="openai api key", channel_id="a channel id", <more options if you need>)
      async def new_question(self, message):
        response = super().get_response(message) # gets ChatGPT's response
        await message.channel.send(embed=discord.Embed(title="ChatGPT said:", description=response))

    MyDiscordGPT()
    ```
    That makes an embed get sent. But keep in mind, this does not do things like log the new messages or send a typing indicator. You can do that yourself, docs are [here](https://discordpy.readthedocs.io).

    Happy ChatGPTing!
  """
  def __init__(self, token: str, api_key: str, channel_id: Union[int, str]=None, channel_name: str=None, model: str="text-davinci-003", prompt: str="User: {message}\n\nAssistant:\n\n", message_to_send: str="{response}", logger: bool=True):
    if "{message}" not in prompt: raise GPTError("Specify the {message} in the prompt")
    if "{response}" not in message_to_send: raise GPTError("Specify the {response} in the message to send")
    self.client = discord.Client(intents=discord.Intents(33281))
    self.logger = logger
    openai.api_key = api_key
    self.model = model
    self.message = prompt
    self.mts = message_to_send
    @self.client.event
    async def on_error(*args):
      raise GPTError(args[0])
    @self.client.event 
    async def on_ready(): 
      self._log(Fore.YELLOW, f"Logged in as {Style.BRIGHT}{self.client.user}") 
      self._log(Fore.GREEN, "Ready to be ChatGPT!")
    @self.client.event
    async def on_message(message_):
      if message_.author.bot: return
      if channel_id:
        if message_.channel.id == int(channel_id):
          await self.new_question(message_)
      elif channel_name:
        if message_.channel.name == channel_name:
          await self.new_question(message_)
      else: raise GPTError("No channel name or id provided") from None
    self._log(Fore.YELLOW, "Starting Discord client...")
    self.client.run(token, log_handler=None)
  async def new_question(self, message) -> None:
    """
    Runs when a new question is posted (new message in the specified channel).
    """
    await message.channel.typing()
    self._log(Fore.CYAN, f"New question from {message.author}: {message.content}")
    resp = self.get_response(message)
    self._log(Fore.GREEN, f"GPT response: {resp}")
    #print(completion)
    await message.channel.send(f"{self.mts.replace('{response}', resp)}")
  def _log(self, c, t):
    if self.logger: print(f"{c}{t}{Style.RESET_ALL}")
  def get_response(self, message) -> str:
    """
    Gets ChatGPT's response to the message content.
    """
    try: return openai.Completion.create(model=self.model, prompt=self.message.replace("{message}", message.content), max_tokens=2048)["choices"][0]["text"]
    except Exception as e: raise GPTError(e) from None