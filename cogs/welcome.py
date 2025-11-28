import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1435565368969003078
GOODBYE_CHANNEL_ID = 1435565417895563344
ROL_INICIAL_ID = 1435359089793433751


class WelcomeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Rol inicial
        rol = member.guild.get_role(ROL_INICIAL_ID)
        if rol:
            await member.add_roles(rol)

        # Mensaje público de bienvenida
        canal = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if canal:
            await canal.send(f"🎉 ¡Bienvenido/a **{member.name}**! 🎉\nPonte cómodo ❤️")

        # Mensaje privado
        try:
            await member.send(
                "✨ **¡Bienvenido/a al servidor!** ✨\n"
                "Estoy aquí para ayudarte en todo lo necesario 💖\n"
                "• Usa `/tienda` para ver la tienda\n"
                "• Usa `/confesar` para mandar una confesión anónima\n"
                "• Usa `/sugerir` para mejorar el servidor ✨"
            )
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = member.guild.get_channel(GOODBYE_CHANNEL_ID)
        if canal:
            await canal.send(f"👋 {member.name} ha dejado el servidor. ¡Te echaremos de menos!")
        

async def setup(bot):
    await bot.add_cog(WelcomeSystem(bot))