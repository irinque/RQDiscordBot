import discord
from discord.ext import commands
from discord.ui import Button, View, Modal
from discord.utils import get
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import *

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=discord.Intents().all())
client = discord.Client

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.event
async def on_member_join(member: discord.Member):
    channel = get(member.guild.channels, id=int(channel_newmembers_data))
    embed = discord.Embed(title="У нас новенький!", description=f"К нам зашел {member.display_name}!", colour=discord.Colour.from_str(color_main))
    embed.set_author(icon_url=member.avatar.url)
    channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    category_voices = discord.utils.get(member.guild.categories, id=int(category_voices_data))
    if after.channel and after.channel.id == channel_voice_data:
        channel_voice = await member.guild.create_voice_channel(name = f'{member.name}', category = category_voices)
        await channel_voice.set_permissions(member, connect=True, mute_members=False, move_members=False, manage_channels=True)
        await member.move_to(channel_voice)
    if before.channel and len(before.channel.members) == 0 and before.channel.id not in channel_voices_whitelist:
        await before.channel.delete()
    

@bot.tree.command(name="custom_embed", description="Embed to channel")
async def send_all(interaction: discord.Interaction):
    async def select_callback(interaction: discord.Interaction):
        await selection.delete()
        channel_name = dropdown.values[0]
        channel = discord.utils.get(interaction.guild.channels, name=str(channel_name))
        class SendApplication(discord.ui.Modal, title="📝 EMBED"):
            message_title = discord.ui.TextInput(label="🎴 ЗАГОЛОВОК", style=discord.TextStyle.short)
            description = discord.ui.TextInput(label="🀄 ОПИСАНИЕ", style=discord.TextStyle.long, required=True)
            image = discord.ui.TextInput(label="🌄 КАРТИНКА", style=discord.TextStyle.short, required=False)
            async def on_submit(self, interaction: discord.Interaction):
                embed = discord.Embed(title=self.message_title, description=self.description, colour=discord.Colour.from_str(color_main))
                if self.image:
                    embed.set_image(url=self.image)
                await channel.send(embed=embed)
                await interaction.response.send_message(f"сообщение отправлено")
                await interaction.delete_original_response()
        await interaction.response.send_modal(SendApplication())
    view = View()
    dropdown = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text], min_values=1, max_values=1)
    dropdown.callback = select_callback
    view.add_item(dropdown)
    selection = await interaction.channel.send(view=view)
    await interaction.response.send_message(f"Выберите канал для отправки:")
    await interaction.delete_original_response()
    


if __name__ == "__main__":
    bot.run(TOKEN)