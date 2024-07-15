import discord
from discord import Embed, File
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class Goodbye:
    def __init__(self, client):
        self.client = client
        self.client.event(self.on_member_remove)

    async def on_member_remove(self, member):
        channel = self.client.get_channel(YOUR_CHANNEL_ID)
        if channel is not None:
            background_url = 'YOUR_CUSTOM_URL' 

            pfp_url = str(member.avatar.url)

            async with aiohttp.ClientSession() as session:
                async with session.get(background_url) as resp:
                    if resp.status != 200:
                        return await channel.send('Unable to download background images.')
                    background_data = await resp.read()
                
                async with session.get(pfp_url) as resp:
                    if resp.status != 200:
                        return await channel.send('Cant download user profile picture.')
                    pfp_data = await resp.read()

            background = Image.open(BytesIO(background_data)).convert("RGBA")
            pfp = Image.open(BytesIO(pfp_data)).resize((700, 700)).convert("RGBA")

            mask = Image.new("L", pfp.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 700, 700), fill=255)
            pfp.putalpha(mask)

            background.paste(pfp, (background.width // 2 - 350, background.height // 2 - 450), pfp)

            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype("arial.ttf", 150) 
            text = "GOODBYE :("
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            draw.text(
                ((background.width - text_width) // 2, (background.height // 2) + 250),
                text,
                font=font,
                fill=(255, 255, 255, 255)
            )

            buffer = BytesIO()
            background.save(buffer, format='PNG')
            buffer.seek(0)

            file = File(buffer, filename='goodbye_image.png')

            embed = Embed(
                title="Goodbye 😭",
                description=f"**{member.mention} has logged out of the server.**",
                color=0x8854d0
            )
            embed.set_image(url="attachment://goodbye_image.png")
            await channel.send(embed=embed, file=file)

def setup(client):
    Goodbye(client)
