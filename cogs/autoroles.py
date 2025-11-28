import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select


class AutoRolesMenus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ====== CANALES ======
        self.canal_edad_id = 1435564630016790600
        self.canal_anuncios_id = 1435571835495252048
        self.canal_juegos_id = 1435572086658564117

        # ====== ROLES ======
        self.roles_edad = {
            "🌙 13 años o más": 1434976832167477418,
            "🍼 Menores de 13 años": 1434976831882395728
        }

        self.roles_anuncios = {
            "👑 Anuncios de Juegalex 04": 1434976832674861217,
            "👸 Anuncios de Administradores": 1434976833572700221
        }

        self.roles_juegos = {
            "🧩 Among Us": 1434976834176548925,
            "🔫 Fortnite": 1434976834692321320,
            "🏙️ GTA V Legacy": 1434976835481108620,
            "🧱 Minecraft": 1434976857228316764,
            "⚔️ Valorant": 1434976858453184543,
            "🌌 Genshin Impact": 1434976859568996484,
            "👻 Five Nights at Freddy's": 1434976860575633429,
            "🏃 Stumble Guys": 1434976861909291098,
            "💎 Geometry Dash": 1434976862617993328,
            "🏰 Sims 4": 1434976864140656680,
            "🤡 Poppy Playtime": 1434976872592310282,
            "🎮 Roblox": 1434976874270031964,
            "🤹 Fall Guys": 1434976875230265487,
            "🌋 League of Legends": 1436019002135547945
        }

    # ================================================================
    # 📌 FUNCIÓN PARA CREAR MENÚS
    # ================================================================
    def crear_menu(self, opciones_dic):
        opciones = [
            discord.SelectOption(
                label=nombre,
                value=str(rol_id),
                description=f"Rol: {nombre}"
            )
            for nombre, rol_id in opciones_dic.items()
        ]

        select = Select(
            placeholder="Selecciona tus roles aquí...",
            min_values=0,
            max_values=len(opciones),
            options=opciones
        )

        async def callback(interaction: discord.Interaction):
            usuario = interaction.user
            guild = interaction.guild

            # Quitar roles previos del grupo
            for rol_id in opciones_dic.values():
                rol = guild.get_role(rol_id)
                if rol in usuario.roles:
                    await usuario.remove_roles(rol)

            # Asignar nuevos roles seleccionados
            for rol_id in interaction.data["values"]:
                rol = guild.get_role(int(rol_id))
                await usuario.add_roles(rol)

            await interaction.response.send_message(
                "¡Roles actualizados correctamente! 💜",
                ephemeral=True
            )

        select.callback = callback

        view = View()
        view.add_item(select)
        return view

    # ================================================================
    # 📌 SLASH COMMAND: crear autoroles
    # ================================================================
    @app_commands.command(name="crear_autoroles", description="Crea los menús de autoroles en sus canales.")
    @app_commands.checks.has_permissions(administrator=True)
    async def crear_autoroles(self, interaction: discord.Interaction):

        # ===== MENÚ EDAD =====
        canal_edad = interaction.guild.get_channel(self.canal_edad_id)
        await canal_edad.send(
            "**🧿 Selecciona tu categoría de edad:**",
            view=self.crear_menu(self.roles_edad)
        )

        # ===== MENÚ ANUNCIOS =====
        canal_anuncios = interaction.guild.get_channel(self.canal_anuncios_id)
        await canal_anuncios.send(
            "**📢 Elige qué anuncios quieres recibir:**",
            view=self.crear_menu(self.roles_anuncios)
        )

        # ===== MENÚ JUEGOS =====
        canal_juegos = interaction.guild.get_channel(self.canal_juegos_id)
        await canal_juegos.send(
            "**🎮 Selecciona los juegos que te gustan:**",
            view=self.crear_menu(self.roles_juegos)
        )

        await interaction.response.send_message("✔ Menús creados correctamente.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(AutoRolesMenus(bot))
