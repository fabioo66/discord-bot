import discord
import requests
import wikipedia
import os
import random
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")

intents = discord.Intents.all()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def info(ctx):
    await ctx.send("Bot desarrollado por fabito")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "hola" in message.content.lower():
        await message.channel.send(f"¡Hola {message.author.name}!")

    await bot.process_commands(message)


@bot.command()
async def crypto(ctx, coin: str):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd")
        data = response.json()
        if coin in data:
            price = data[coin]["usd"]
            await ctx.send(f"El precio de {coin} es ${price} USD")
        else:
            await ctx.send("No se encontró la criptomoneda especificada")
    except Exception as e:
        await ctx.send("Hubo un error al consultar el precio de la criptomoneda")
        print(e)


def buscar_wikipedia(consulta):
    try:
        wikipedia.set_lang("es")
        resultado = wikipedia.summary(consulta, sentences=4)
        return resultado
    except wikipedia.exceptions.DisambiguationError as e:
        return f"La busqueda '{consulta}' es ambigua. Por favor, se mas especifico"
    except wikipedia.exceptions.PageError as e:
        return f"No se encontro ningun articulo relacionado con '{consulta}' en wikipedia"



@bot.command()
async def wiki(ctx, *, consulta):
    try:
        resultado = buscar_wikipedia(consulta)
        await ctx.send(resultado)
    except  Exception as e:
        await ctx.send(f"Error al realizar la busqueda en Wikipedia: {e}")


@bot.command()
async def memide(ctx):
    random_number = random.randint(1,30)
    await ctx.send(f"A {ctx.author.name} le mide {random_number} cm")


@bot.command()
async def coinflip(ctx):
    coin = ["CARA", "SECA"]
    await ctx.send("Tirando una moneda...")
    await ctx.send(f"Resultado = {random.choice(coin)}")


bot.run(token)