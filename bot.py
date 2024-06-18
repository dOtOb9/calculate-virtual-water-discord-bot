import discord
from os import getenv

from main import send_image_to_ai

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    
    if message.channel.type == 'private': return  # DM以外のチャンネルでのメッセージは無視


    if message.attachments != []:
        for attachment in message.attachments:
            virtual_water_text, items_text = send_image_to_ai(attachment.url)

            embed = discord.Embed(
                title='仮想水算出結果', 
                colour=discord.Colour.green(),
                fields=[
                    discord.EmbedField(
                        name='品名', 
                        value=items_text
                    ),
                    discord.EmbedField(
                        name='仮想水量💧', 
                        value=virtual_water_text
                    )
                ]
            )

            embed.set_footer(text='gpt-4o-2024-05-13', icon_url='https://github.com/dOtOb9/calculate-virtual-water-dsicord-bot/blob/main/chatgpt-logo.png?raw=true')

    await message.channel.send(embed=embed)


bot.run(getenv('DISCORD_BOT_TOKEN'))