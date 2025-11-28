import discord
from discord.ext import commands
from discord import app_commands

class Sugerencias(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canal_sugerencias_id = 1435578117878976512  # ID del canal de sugerencias

    @app_commands.command(name="sugerencia", description="Envía una sugerencia al servidor.")
    @app_commands.describe(texto="Escribe tu sugerencia.")
    async def sugerencia(self, interaction: discord.Interaction, texto: str):

        canal = interaction.guild.get_channel(self.canal_sugerencias_id)

        if canal is None:
            return await interaction.response.send_message(
                "❌ No se encontró el canal de sugerencias.", ephemeral=True
            )

        mensaje = await canal.send(f"💡 **Nueva sugerencia:**\n{texto}")

        # Reacciones de votación
        await mensaje.add_reaction("✅")
        await mensaje.add_reaction("❌")

        await interaction.response.send_message(
            "✔ Tu sugerencia fue enviada correctamente.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Sugerencias(bot))