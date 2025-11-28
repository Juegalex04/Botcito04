import discord
from discord.ext import commands
from discord import app_commands

class Confesiones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canal_confesiones_id = 1435578149491707986  # ID del canal de confesiones

    @app_commands.command(name="confesar", description="Envía una confesión anónima.")
    @app_commands.describe(texto="Escribe aquí tu confesión.")
    async def confesar(self, interaction: discord.Interaction, texto: str):

        canal = interaction.guild.get_channel(self.canal_confesiones_id)

        if canal is None:
            return await interaction.response.send_message(
                "❌ No se encontró el canal de confesiones.", ephemeral=True
            )

        # Enviar mensaje anónimo
        await canal.send(f"📢 **Nueva Confesión Anónima:**\n{texto}")

        await interaction.response.send_message(
            "✔ Tu confesión se envió de forma totalmente anónima.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Confesiones(bot))