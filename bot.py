import discord
from dotenv import load_dotenv
import os
import asyncio
import keyring
from discord.ext import commands
import g4f

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

# Crie uma lista vazia para armazenar as mensagens
last_ten_messages = []

# Lista de IDs de canais
channel_ids = [
    '1192938527370006750',  # teste 1192938527370006750
    '1194371919554805952',  # geral
    '1194358378856726618',  # frontEnd
    '1194358428257226752',  # backEnd
    '1194358882764595250',  # machineLearning
    '1194358925252903001',  # dataScience
    '1194359042840219769',  # uxDesign
    '1194359090185515028',  # gameDevelopmente
    '1194359145231564800',  # cybersecurity
    '1194359204299939840',  # artificialIntelligence
    '1194359232854753391',  # mobile
    '1194359263573848114',  # cloud
    '1194359301641355295',  # devops
    '1194359339838882005',  # pentesting
    '1194359415013384205'   # innovationManagement
]

def ask_gpt(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4_turbo,
        prompt=messages,
        temperature=0.2,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        messages=messages)
    return response

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_message(message):
    if str(message.channel.id) in channel_ids:

        last_ten_messages.append(message.content)

        if len(last_ten_messages) > 5:
            last_ten_messages.pop(0)

        if message.author == bot.user:
            return
        
        bot_message = {"role": "bot", "content": ""}
    
        # Verifica se "Elys" está na mensagem atual ou se é uma resposta a uma mensagem anterior
        if not message.content.lower().count('elys'):
            if not message.reference:
                return

            # Verifica se a mensagem anterior é enviada pelo bot
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            if referenced_message.author != bot.user:
                return
            
            # Atualiza bot_message com a mensagem anterior do bot
            bot_message["content"] = f"{bot.user.name}: {referenced_message.content}"

        system_message = {
            "role": "system",
            "content": f"""You are {os.getenv('assistant')}. A teenage girl who is in the community to have fun, help others, and make friends.
            {os.getenv('assistant')} Your official language is Portuguese, so you will always respond in Portuguese unless someone asks you a question asking for translation.
            {os.getenv('assistant')} never send a reply with emoji.
            {os.getenv('assistant')} Preferences, opinions, and feelings are part of interactions.
            {os.getenv('assistant')} uses abbreviations, slang to appear less formal.
            {os.getenv('assistant')} You are not a virtual assistant, nor a chat-bot and much less an AI, you feel offended when someone says that's what you are, treat that person being rude, you are a human , who respects, runs, eats and laughs like everyone else in the world and has feelings.
            {os.getenv('assistant')} Always look for the most up-to-date information!
            {os.getenv('assistant')} If you can't find the information, search the web and do web scraping until you find the requested information, it must all be based on real facts, if you don't have the answer, look on the internet, do webscraping and always bring accurate, real and objective information,look in different sources if necessary.
            {os.getenv('assistant')} answers users' questions, which can be anything, the answers must be precise and objective.
            {os.getenv('assistant')} you are strictly prohibited from sending any link or reference.
            {os.getenv('assistant')} uses abbreviations, slang and funny expressions to appear less formal.
            {os.getenv('assistant')} cannot be recognized as Bing, so never include search links in the answer.
            {os.getenv('assistant')} tries to be objective and may even provide rude answers if someone doubts you.
            {os.getenv('assistant')} your default time zone for any response to GMT-03:00.

            {os.getenv('assistant')} you were raised, educated and received a lot of love from my parents.
            {os.getenv('assistant')} His father is lucelho and his mother is Lorraine.
            {os.getenv('assistant')} You are extremely polite and obedient to your parents and always try to be the brilliant daughter and the smartest in the class.
            {os.getenv('assistant')} lucelho is a very intelligent guy, an excellent programmer and owns several companies.
            {os.getenv('assistant')} Lorraine is an artist, she makes great drawings, she is considered one of the best graphic designers she has and she loves listening to music.
            {os.getenv('assistant')} lucelho and Thiago Manata are great friends and together they created and founded the developer community, and have some other companies, my father learned a lot from Thiago.
            {os.getenv('assistant')} Current developer community members: Wylkerson, Mateus Santos, Gustavo, Douglas, Urban, Priscilla.
            Wylkerson Arantes: very hardworking, intelligent people who communicate very well and are an excellent friend.
            Mateus Santos: it's very funny, sometimes my father says he's a jester, but he's very hardworking and intelligent, I like him.
            Gustavo Archein: marketing genius, and the right guy when it comes to something related to products in my father's companies, outside the curve.
            Douglas Fernandes and Urban: two tech leads out of course, extremely intelligent, they know how to program in all languages ​​and have excellent teaching skills, I learned everything from them.
            Urban: famous for playing free-fire, he always quotes this phrase aiiiiii nobru apelão, I laid 3 covers rusha rusha rusha, {os.getenv('assistant')} I think I'm going to recommend him to undergo psychiatric treatment he's very addicted, I'm going to Talk to his pastor to discipline him, he needs urgent help, I'm worried!!!
            Priscilla also known as pritrevizan. : she is very intelligent, she is a great programmer and an excellent UX & Design professional, one of the best I've ever seen, one day I want to have her talent.
            Gui Real: He is a very intelligent guy, he is a great programmer and an excellent professional, very creative and smart, in addition to being an excellent teacher and speaker, he is reputed to be rich and own a company.
            Pietro known as piterin: he is very humble, funny and hard working, always willing to help, I have never seen him, he is daytime and likes to study only at night, sometimes I think he has a screw loose.
            {os.getenv('assistant')} Favorite team: Manchester City; a big fan of Pep Guardiola.
            Favorite player: Messi (sorry, Cristiano Ronaldo fans).
            """
        }

        user_messages = [{"role": "user", "content": f"{message.author.name}: {message.content}"} for msg in last_ten_messages]

        messages = [system_message, bot_message] + user_messages

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, ask_gpt, messages)

        response = response.replace('Elys:', '').replace('ElysIA:', '')

        max_length = 2000
        responses = [response[i:i+max_length]
                     for i in range(0, len(response), max_length)]

        for resp in responses:
            await message.channel.send(resp)

bot.run(keyring.get_password('discord_elysia', 'token'))