import discord
from discord.ext import commands
from discord import Embed
import datetime

# ======================
# CONFIGURACIÓN GENERAL
# ======================

CANAL_LOGS = 1436401849459671133        # Canal global de logs
OWNER_ID = 620244589017563136           # Tus MDs


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------
    # Enviar log global + MD
    # ------------

    async def enviar_log(self, embed: discord.Embed, texto_md: str):
        canal = self.bot.get_channel(CANAL_LOGS)

        # Enviar al canal de logs (embed)
        if canal:
            await canal.send(embed=embed)

        # Enviar por MD al OWNER (texto simple)
        owner = self.bot.get_user(OWNER_ID)
        if owner:
            try:
                await owner.send(texto_md)
            except:
                pass

    # =========================
    # 1. MENSAJES ELIMINADOS
    # =========================
    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author.bot:
            return

        embed = Embed(
            title="🗑️ Mensaje eliminado",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Autor", value=f"{message.author} ({message.author.id})", inline=False)
        embed.add_field(name="Canal", value=message.channel.mention, inline=False)
        embed.add_field(name="Contenido", value=message.content or "*<Vacío>*", inline=False)

        texto = (
            "🗑️ Mensaje eliminado\n"
            f"Autor: {message.author} ({message.author.id})\n"
            f"Canal: #{message.channel}\n"
            f"Contenido: {message.content}\n"
        )

        await self.enviar_log(embed, texto)

    # =========================
    # 2. MENSAJES EDITADOS
    # =========================
    @commands.Cog.listener()
    async def on_message_edit(self, antes, despues):

        if antes.author.bot or antes.content == despues.content:
            return

        embed = Embed(
            title="✏️ Mensaje editado",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Autor", value=f"{antes.author} ({antes.author.id})", inline=False)
        embed.add_field(name="Canal", value=antes.channel.mention, inline=False)
        embed.add_field(name="Antes", value=antes.content or "*<Vacío>*", inline=False)
        embed.add_field(name="Después", value=despues.content or "*<Vacío>*", inline=False)

        texto = (
            "✏️ Mensaje editado\n"
            f"Autor: {antes.author} ({antes.author.id})\n"
            f"Canal: #{antes.channel}\n"
            f"Antes: {antes.content}\n"
            f"Después: {despues.content}\n"
        )

        await self.enviar_log(embed, texto)

    # =========================
    # 3. ROLES AÑADIDOS / QUITADOS
    # =========================
    @commands.Cog.listener()
    async def on_member_update(self, antes, despues):

        added = [r for r in despues.roles if r not in antes.roles]
        removed = [r for r in antes.roles if r not in despues.roles]

        for rol in added:
            embed = Embed(
                title="➕ Rol añadido",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Usuario", value=f"{despues} ({despues.id})", inline=False)
            embed.add_field(name="Rol", value=f"{rol.name}", inline=False)

            texto = (
                "➕ Rol añadido\n"
                f"Usuario: {despues} ({despues.id})\n"
                f"Rol añadido: {rol.name}\n"
            )

            await self.enviar_log(embed, texto)

        for rol in removed:
            embed = Embed(
                title="➖ Rol removido",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Usuario", value=f"{antes} ({antes.id})", inline=False)
            embed.add_field(name="Rol", value=f"{rol.name}", inline=False)

            texto = (
                "➖ Rol removido\n"
                f"Usuario: {antes} ({antes.id})\n"
                f"Rol removido: {rol.name}\n"
            )

            await self.enviar_log(embed, texto)

    # =========================
    # 4. CANALES CREADOS / ELIMINADOS
    # =========================
    @commands.Cog.listener()
    async def on_guild_channel_create(self, canal):
        embed = Embed(
            title="📁 Canal creado",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Nombre", value=canal.name)
        embed.add_field(name="ID", value=canal.id)
        embed.add_field(name="Tipo", value=str(canal.type))

        texto = f"📁 Canal creado → {canal.name} (ID {canal.id})"

        await self.enviar_log(embed, texto)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, canal):
        embed = Embed(
            title="🗑️ Canal eliminado",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Nombre", value=canal.name)
        embed.add_field(name="ID", value=canal.id)
        embed.add_field(name="Tipo", value=str(canal.type))

        texto = f"🗑️ Canal eliminado → {canal.name} (ID {canal.id})"

        await self.enviar_log(embed, texto)

    # =========================
    # 5. ROLES CREADOS / ELIMINADOS
    # =========================
    @commands.Cog.listener()
    async def on_guild_role_create(self, rol):
        embed = Embed(
            title="🎨 Rol creado",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Nombre", value=rol.name)
        embed.add_field(name="ID", value=rol.id)

        texto = f"🎨 Rol creado → {rol.name} (ID {rol.id})"

        await self.enviar_log(embed, texto)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, rol):
        embed = Embed(
            title="🔥 Rol eliminado",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Nombre", value=rol.name)
        embed.add_field(name="ID", value=rol.id)

        texto = f"🔥 Rol eliminado → {rol.name} (ID {rol.id})"

        await self.enviar_log(embed, texto)


async def setup(bot):
    await bot.add_cog(Logs(bot))