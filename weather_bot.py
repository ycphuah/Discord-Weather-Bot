import discord
import requests
from datetime import datetime

client = discord.Client()

discordToken = 'NzU5MjQzNjU5NTg0NDcxMTAx.X26qwg.T-6uuf5Xz8JQd9LupgLBZF11qS0'
openWeatherToken = '1bef2e158f5cabc0d21fe7fd6efde2e3'

@client.event
async def on_ready():
    print('{0.user}'.format(client) + ' is online.')

@client.event
async def on_message(message):
    channel = message.channel
    m = message.content.lower()

    if m.startswith('!w'):
        messageList = m.split(" ", 1)
        city = messageList[1]

        def getWeather(cityInput):
            extractedData = []
            data = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + cityInput + '&units=metric&appid=' + openWeatherToken + '').json()

            if data['cod'] == '404':
                return []
            else:
                for value in data['main'].values():
                    extractedData.append(int(value))    #temperature, feels like, min temp, max temp, pressure, humidity
                extractedData.append(data['weather'][0]['description'])
                extractedData.append(data['name'])
                extractedData.append(data['sys']['country'])
                extractedData.append(int(data['sys']['sunrise']))
                extractedData.append(int(data['sys']['sunset']))
                extractedData.append(int(data['visibility'] / 1000))

            return extractedData

        currentWeather = getWeather(city)

        if len(currentWeather) == 0:
            await channel.send('Error! Please make sure the city name is correct!')

        else:
            title = str(currentWeather[0]) + '°C\t\t\t\t\t\t\t' + currentWeather[6] + '\t\t\t\t\t' + currentWeather[7] + ', ' + currentWeather[8]
            feelsLike = 'Feels Like ' + str(currentWeather[1]) + '°C'
            embed = discord.Embed(title=title,color=discord.Color.blue(), description=feelsLike)    #Location and description
            embed.add_field(name='Minimum temp: ', value=str(currentWeather[2]) + ' °C')
            embed.add_field(name='Maximum temp: ', value=str(currentWeather[3]) + ' °C')
            embed.add_field(name='Humidity: ', value=str(currentWeather[5]) + ' %')
            embed.add_field(name='Sunrise: ', value=datetime.utcfromtimestamp(currentWeather[9]).strftime('%H:%M'))
            embed.add_field(name='Sunset: ', value=datetime.utcfromtimestamp(currentWeather[10]).strftime('%H:%M'))
            embed.add_field(name='Visibility: ', value=str(currentWeather[11]) + ' km')

            await channel.send(embed=embed)

    if m.startswith('!help'):
        await channel.send('To query weather information, please type !w follow by city name and country code\n''Example: !w dublin,ie')

client.run(discordToken)