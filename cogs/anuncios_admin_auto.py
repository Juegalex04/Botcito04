import discord
from discord.ext import commands

class AnuncioAdminAuto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # IDs proporcionados
        self.rol_admin_id = 1434976818364023059
        self.canal_anuncio_admins_id = 1435575775553261711
        self.rol_ping_admins_id = 1434976833572700221

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Detecta cuando un usuario obtiene el rol de ADMINISTRADOR.
        No se activa si el rol ya lo tenía antes.
        """

        rol_admin = after.guild.get_role(self.rol_admin_id)

        # Si el usuario NO tenía el rol antes, pero ahora sí → ES NUEVO ADMIN
        if rol_admin not in before.roles and rol_admin in after.roles:

            canal = after.guild.get_channel(self.canal_anuncio_admins_id)
            rol_ping = after.guild.get_role(self.rol_ping_admins_id)

            # Mensaje público en el canal de anuncios de administradores
            await canal.send(
                f"🎉 ¡Atención {rol_ping.mention}! 🎉\n"
                f"El usuario **{after.mention}** ha sido ascendido al rol de **Administrador**.\n"
                f"✨ ¡Felicítalo! Muy pronto recibirá su canal privado asignado por el Owner."
            )

            # Mensaje privado al nuevo admin
            try:
                await after.send(
                    "🎉 **¡FELICIDADES!** 🎉\n"
                    "Has sido ascendido al rol de **Administrador** en el servidor.\n\n"
                    "A partir de ahora podrás:\n"
                    "• Hablar en el chat de administradores.\n"
                    "• Participar en reuniones con el dueño del servidor.\n"
                    "• Tener tu propio canal personal como administrador.\n"
                    "• Hacer anuncios en tu canal exclusivo.\n"
                    "• Ayudar a moderar y organizar eventos.\n\n"
                    "El OWNER te creará tu canal correspondiente en breves momentos.\n"
                    "✨ ¡Disfruta tu nueva responsabilidad!"
                )
            except:
                print(f"No pude enviar DM a {after}.")

async def setup(bot):
    await bot.add_cog(AnuncioAdminAuto(bot))