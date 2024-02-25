import discord

from discord.ext import commands, tasks

import http.client as httplib

import json

import datetime

from apikeys import * 

from gtts import gTTS
import asyncio


intents = discord.Intents.default()

intents.members = True



# Defining the prefix which is like the run bot command

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())



# To see when bot running

@client.event

async def on_ready():

    print("Bot is ready")

    print("---------------")



#-----------------------------------------------------------------------------------------#



#Hello command

@client.command()

async def hello(ctx):

    await ctx.send("Hello I am a bot")








#Message when someone joins

@client.event

async def on_member_join(member):

    channel = client.get_channel(-------)

    await channel.send(f"Welcome to the server {member.mention}!")





#Message when someone leaves

@client.event

async def on_member_remove(member):

    channel = client.get_channel(---------)

    await channel.send(f"{member.mention} has left the server!")





@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("User not in channel")


#guild = server
@client.command(pass_context = True)
async def leave(ctx):
    bot_name = ctx.bot.user.name
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send(f"{bot_name} has disconnected")
    else:
        await ctx.send(f"{bot_name} is not connected")




#-----------------------------------------------------------------------------------------#

# def weather

@client.command()

async def weather(ctx):

    LOCATION = 'Belleville Michigan'



    # Construct the API URL with query parameters and URL-encode the location

    encoded_location = LOCATION.replace(' ', '%20')

    url = f"/v1/current.json?key={WEATHER_TOKEN}&q={encoded_location}&aqi=no"



    try:

        # Establish a connection to the API server

        connection = httplib.HTTPSConnection("api.weatherapi.com")



        # Send an HTTP GET request to the API

        connection.request("GET", url)

        response = connection.getresponse()



        # Check if the request was successful (HTTP status code 200)

        if response.status == 200:

            # Parse the JSON response

            weather_data = json.loads(response.read().decode())



            # Extract and send relevant weather information

            current_weather = weather_data.get("current", {})

            temperature = current_weather.get("temp_f", "N/A")  # Use temp_f for Fahrenheit

            weather_description = current_weather.get("condition", {}).get("text", "N/A")



            await ctx.send(f"Weather in {LOCATION}: {weather_description}")

            await ctx.send(f"Temperature: {temperature}°F")  # Display temperature in Fahrenheit



        else:

            await ctx.send(f"Failed to retrieve weather data. Status code: {response.status}")



    except Exception as e:

        await ctx.send(f"An error occurred: {str(e)}")



    finally:

        

        connection.close()



@client.command()

async def weekly_weather(ctx):

    LOCATION = 'Location goes here'



    # Construct the API URL with query parameters and URL-encode the location

    encoded_location = LOCATION.replace(' ', '%20')

    url = f"/v1/forecast.json?key={WEATHER_TOKEN}&q={encoded_location}&days=7&aqi=no"



    try:

        # Establish a connection to the API server

        connection = httplib.HTTPSConnection("api.weatherapi.com")



        # Send an HTTP GET request to the API

        connection.request("GET", url)

        response = connection.getresponse()



        # Check if the request was successful (HTTP status code 200)

        if response.status == 200:

            # Parse the JSON response

            weather_data = json.loads(response.read().decode())



            # Extract and send relevant weather information for each day of the week

            for day in weather_data.get("forecast", {}).get("forecastday", []):

                date = day.get("date", "N/A")

                max_temp = day.get("day", {}).get("maxtemp_f", "N/A")

                min_temp = day.get("day", {}).get("mintemp_f", "N/A")

                condition = day.get("day", {}).get("condition", {}).get("text", "N/A")



                await ctx.send(f"Date: {date}")

                await ctx.send(f"Max Temperature: {max_temp}°F")

                await ctx.send(f"Min Temperature: {min_temp}°F")

                await ctx.send(f"Condition: {condition}")

                await ctx.send("-------------")



        else:

            await ctx.send(f"Failed to retrieve weather data. Status code: {response.status}")



    except Exception as e:

        await ctx.send(f"An error occurred: {str(e)}")



    finally:

        connection.close()



@tasks.loop(hours=168)  

async def send_weather():

    if datetime.datetime.now().weekday() == 6:

        user = await client.fetch_user(293529126298583040)

        channel = client.get_channel(785054196490698762)

        LOCATION = 'Belleville Michigan'

        encoded_location = LOCATION.replace(' ', '%20')

        url = f"/v1/current.json?key={WEATHER_TOKEN}&q={encoded_location}&aqi=no"



        try:

            connection = httplib.HTTPSConnection("api.weatherapi.com")

            connection.request("GET", url)

            response = connection.getresponse()



            if response.status == 200:

                weather_data = json.loads(response.read().decode())

                current_weather = weather_data.get("current", {})

                temperature = current_weather.get("temp_f", "N/A")

                weather_description = current_weather.get("condition", {}).get("text", "N/A")



                await user.send(f"Weather in {LOCATION}: {weather_description}")

                await user.send(f"Temperature: {temperature}°F")



            else:

                await user.send(f"Failed to retrieve weather data. Status code: {response.status}")



        except Exception as e:

            await user.send(f"An error occurred: {str(e)}")



        finally:

            connection.close()



@send_weather.before_loop

async def before_send_weather():

    await client.wait_until_ready()



# Start the bot first

client.run(BOTTOKEN)

# Start the send_weather task

send_weather.start()

