import discord
from discord import Embed, File
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class Welcome:
    def __init__(self, client):
        self.client = client
        self.client.event(self.on_member_join)

    async def on_member_join(self, member):
        channel = self.client.get_channel(1233042384787345479)
        if channel is not None:
            background_url = 'https://autumn.revolt.chat/attachments/TCHnUYhrt5xXKUQeaxWX-vqA2Ct9yvH03B_IyF56-H' 

            pfp_url = str(member.avatar.url)

            async with aiohttp.ClientSession() as session:
                async with session.get(background_url) as resp:
                    if resp.status != 200:
                        return await channel.send('Tidak dapat mengunduh gambar latar belakang.')
                    background_data = await resp.read()
                
                async with session.get(pfp_url) as resp:
                    if resp.status != 200:
                        return await channel.send('Tidak dapat mengunduh gambar profil pengguna.')
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
            text = "WELCOME :D"
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

            file = File(buffer, filename='welcome_image.png')

            embed = Embed(
                title="Welcome 😁",
                description=f"**{member.mention} telah bergabung ke server.**",
                color=0x8854d0 
            )
            embed.set_image(url="attachment://welcome_image.png")
            embed.set_footer(text="©secret basement team - 2024", icon_url=self.client.user.avatar.url)

            await channel.send(embed=embed, file=file)

def setup(client):
    Welcome(client)
