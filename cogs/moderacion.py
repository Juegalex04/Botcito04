import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

OWNER_ID = 620244589017563136   # TU ID

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ======== CANALES ========
        self.canal_warns = 1436024021769654382
        self.canal_kicks = 1436024201202110605
        self.canal_baneos = 1436024234559279324

        # ======== ROLES AUTORIZADOS ========
        self.rol_admin_principal = 1434976816724054199
        self.rol_admin = 1434976818364023059

        # ======== BASE DE DATOS ========
        self.conn = sqlite3.connect("moderacion.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                user_id INTEGER,
                staff_id INTEGER,
                motivo TEXT,
                fecha TEXT
            )
        """)
        self.conn.commit()

    # =====================================================================
    # ✔ VERIFICAR PERMISOS
    # =====================================================================
    def es_admin(self, interaction: discord.Interaction):
        roles = [r.id for r in interaction.user.roles]
        return (
            self.rol_admin_principal in roles
            or self.rol_admin in roles
        )

    # =====================================================================
    # ✔ ENVIAR MD AL OWNER
    # =====================================================================
    async def log_owner(self, texto: str):
        owner = self.bot.get_user(OWNER_ID)
        if owner:
            try:
                await owner.send(texto)
            except:
                pass

    # =====================================================================
    # ✔ /warn
    # =====================================================================
    @app_commands.command(name="warn", description="Warnea a un usuario.")
    async def warn(self, interaction: discord.Interaction, usuario: discord.User, motivo: str):

        if not self.es_admin(interaction):
            return await interaction.response.send_message(
                "❌ No tienes permisos para usar este comando.",
                ephemeral=True
            )

        # Guardar en base de datos
        self.cursor.execute("""
            INSERT INTO warns (user_id, staff_id, motivo, fecha)
            VALUES (?, ?, ?, ?)
        """, (usuario.id, interaction.user.id, motivo, datetime.now().isoformat()))
        self.conn.commit()

        # Embed al staff
        embed = discord.Embed(
            title="⚠️ Usuario Advertido",
            description=f"**Usuario:** {usuario.mention}\n"
                        f"**Staff:** {interaction.user.mention}\n"
                        f"**Motivo:** {motivo}",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Canal de warns
        canal = interaction.guild.get_channel(self.canal_warns)
        await canal.send(embed=embed)

        # 📩 MD para ti (OWNER)
        await self.log_owner(
            f"⚠️ *WARN aplicado*\n"
            f"Usuario: {usuario} ({usuario.id})\n"
            f"Staff: {interaction.user} ({interaction.user.id})\n"
            f"Motivo: {motivo}"
        )

    # =====================================================================
    # ✔ /kick  (con MD al usuario + MD al owner)
    # =====================================================================
    @app_commands.command(name="kick", description="Expulsa a un usuario del servidor.")
    async def kick(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str):

        if not self.es_admin(interaction):
            return await interaction.response.send_message(
                "❌ No tienes permisos para usar este comando.",
                ephemeral=True
            )

        # 📩 MD al usuario expulsado
        try:
            await usuario.send(
                f"🚪 **Has sido expulsado del servidor `{interaction.guild.name}`.**\n"
                f"**Motivo:** {motivo}"
            )
        except:
            pass

        # Ejecutar kick
        await usuario.kick(reason=motivo)

        embed = discord.Embed(
            title="🚪 Usuario Expulsado",
            description=f"**Usuario:** {usuario.mention}\n"
                        f"**Staff:** {interaction.user.mention}\n"
                        f"**Motivo:** {motivo}",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        canal = interaction.guild.get_channel(self.canal_kicks)
        await canal.send(embed=embed)

        # 📩 MD para ti (OWNER)
        await self.log_owner(
            f"🚪 *KICK aplicado*\n"
            f"Usuario: {usuario} ({usuario.id})\n"
            f"Staff: {interaction.user} ({interaction.user.id})\n"
            f"Motivo: {motivo}"
        )

    # =====================================================================
    # ✔ /ban  (con MD al usuario + MD al owner)
    # =====================================================================
    @app_commands.command(name="ban", description="Banea a un usuario del servidor.")
    async def ban(self, interaction: discord.Interaction, usuario: discord.User, motivo: str):

        if not self.es_admin(interaction):
            return await interaction.response.send_message(
                "❌ No tienes permisos para usar este comando.",
                ephemeral=True
            )

        # 📩 MD al usuario baneado
        try:
            await usuario.send(
                f"⛔ **Has sido baneado permanentemente del servidor `{interaction.guild.name}`.**\n"
                f"**Motivo:** {motivo}"
            )
        except:
            pass

        guild = interaction.guild
        await guild.ban(user=usuario, reason=motivo)

        embed = discord.Embed(
            title="⛔ Usuario Baneado",
            description=f"**Usuario:** {usuario.mention}\n"
                        f"**Staff:** {interaction.user.mention}\n"
                        f"**Motivo:** {motivo}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        canal = interaction.guild.get_channel(self.canal_baneos)
        await canal.send(embed=embed)

        # 📩 MD para ti (OWNER)
        await self.log_owner(
            f"⛔ *BAN aplicado*\n"
            f"Usuario: {usuario} ({usuario.id})\n"
            f"Staff: {interaction.user} ({interaction.user.id})\n"
            f"Motivo: {motivo}"
        )

async def setup(bot):
    await bot.add_cog(Moderacion(bot))