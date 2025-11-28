import discord
from discord.ext import commands
from discord import app_commands

class Anuncios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # IDs de roles
        self.rol_juegalex = 1434976832674861217
        self.rol_admins = 1434976833572700221

    # ============================================================
    # FUNCIONES INTERNAS
    # ============================================================

    def es_admin(self, member: discord.Member):
        """Devuelve True si el usuario es Owner, Admin Principal o Admin."""
        allowed_roles = [
            1434976816724054199,   # Administrador Principal
            1434976818364023059    # Administrador
        ]
        return (
            member.guild.owner_id == member.id
            or any(r.id in allowed_roles for r in member.roles)
        )

    # ============================================================
    # /anuncio_juegalex
    # ============================================================

    @app_commands.command(
        name="anuncio_juegalex",
        description="Publica un anuncio oficial de Juegalex en un canal específico."
    )
    @app_commands.describe(
        canal="Nombre EXACTO del canal donde quieres enviar el anuncio.",
        anuncio="El anuncio que quieres enviar."
    )
    async def anuncio_juegalex(self, interaction: discord.Interaction, canal: str, anuncio: str):

        if not self.es_admin(interaction.user):
            return await interaction.response.send_message("❌ No tienes permiso para usar este comando.", ephemeral=True)

        # Buscar canal por nombre exacto
        canal_obj = discord.utils.get(interaction.guild.text_channels, name=canal)
        if not canal_obj:
            return await interaction.response.send_message(
                "❌ Canal no encontrado. Asegúrate de escribirlo EXACTAMENTE igual.",
                ephemeral=True
            )

        rol_mention = interaction.guild.get_role(self.rol_juegalex)

        # Enviar anuncio
        await canal_obj.send(f"{rol_mention.mention}\n{anuncio}")

        await interaction.response.send_message("✔ Anuncio enviado correctamente.", ephemeral=True)

    # ============================================================
    # /anuncio_admin
    # ============================================================

    @app_commands.command(
        name="anuncio_admin",
        description="Publica un anuncio de los administradores en un canal específico."
    )
    @app_commands.describe(
        canal="Nombre EXACTO del canal donde quieres enviar el anuncio.",
        anuncio="El anuncio que quieres enviar."
    )
    async def anuncio_admin(self, interaction: discord.Interaction, canal: str, anuncio: str):

        if not self.es_admin(interaction.user):
            return await interaction.response.send_message("❌ No tienes permiso para usar este comando.", ephemeral=True)

        # Buscar canal
        canal_obj = discord.utils.get(interaction.guild.text_channels, name=canal)
        if not canal_obj:
            return await interaction.response.send_message(
                "❌ No encontré ese canal. Escribe el nombre EXACTO.",
                ephemeral=True
            )

        rol_mention = interaction.guild.get_role(self.rol_admins)

        # Enviar anuncio
        await canal_obj.send(f"{rol_mention.mention}\n{anuncio}")

        await interaction.response.send_message("✔ Anuncio enviado correctamente.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Anuncios(bot))