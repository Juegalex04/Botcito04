import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime, timedelta

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # =============================
        # 📀 BASE DE DATOS
        # =============================
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        # Tabla economía
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS economia (
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 0,
            last_daily TEXT
        )
        """)
        self.conn.commit()

        # Tabla para fecha de entrada al servidor
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresos (
            user_id INTEGER PRIMARY KEY,
            joined_at TEXT
        )
        """)
        self.conn.commit()

        # Guardar la fecha de ingreso si no existe
        @bot.event
        async def on_member_join(member):
            self.cursor.execute("INSERT OR REPLACE INTO ingresos (user_id, joined_at) VALUES (?, ?)",
                                (member.id, datetime.now().isoformat()))
            self.conn.commit()

        # Estado tienda eventos
        self.eventos_activos = True

        # =============================
        # 🛒 TIENDAS
        # =============================

        # IDs que tú pondrás
        self.ROL_MAYORES = 1434976832167477418
        self.ROL_MENORES = 1434976831882395728

        self.ROL_EVENTOS = 1435356129197818006

        # Roles de nivel
        self.roles_nivel = {
            10: 1434976824395567226,
            20: 1434976825116725322,
            30: 1434976826299777128,
            40: 1434976826534527117,
            50: 1434976827281113108,
            60: 1434976827864125460,
            70: 1434976828648456212,
            80: 1434976829285994576,
            90: 1434976829935976488,
            100: 1434976830569582623
        }

        # Roles staff/admin/moderador
        self.roles_casino_requeridos = [
            1434976823091134514,  # Moderador
            1434976822403268639,  # Moderador VIP
            1434976821157433546,  # Staff
            1434976820121305110,  # Staff Principal
            1434976819815252058,  # Staff Privado
            1434976818364023059,  # Administrador
            1434976816724054199   # Administrador Principal
        ]

        # -----------------------------
        # 🟢 TIENDA NORMAL
        # -----------------------------
        self.tienda_normal = {
            "Gamer": {
                "precio": 10,
                "rol_id": 1434976880595046581,  # ← ID AQUÍ
                "requisitos": None
            },
            "Comida": {
                "precio": 10,
                "rol_id": 1434976881974968542,  # ← ID AQUÍ
                "requisitos": None
            },
            "Puto": {
                "precio": 20,
                "rol_id": 1434976883803422851,  # ← ID AQUÍ
                "requisitos": {"edad": "+13"}
            },
            "Amante de los Gatos": {
                "precio": 20,
                "rol_id": 1434976891819004015,  # ← ID AQUÍ
                "requisitos": None
            },
            "Calvo": {
                "precio": 25,
                "rol_id": 1434976882897719358,  # ← ID AQUÍ
                "requisitos": {"calvo": True}
            },
            "Fachero": {
                "precio": 50,
                "rol_id": 1434976885007323347,  # ← ID AQUÍ
                "requisitos": {"nivel": 70}
            },
            "Sad Boy": {
                "precio": 55,
                "rol_id": 1434976876727767242,  # ← ID AQUÍ
                "requisitos": None
            },
            "Sad Girl": {
                "precio": 55,
                "rol_id": 1434976878355152907,  # ← ID AQUÍ
                "requisitos": None
            },
            "Asesino": {
                "precio": 100,
                "rol_id": 1434976890480889916,  # ← ID AQUÍ
                "requisitos": {"nivel": 30}
            },
            "Caza Demonios": {
                "precio": 150,
                "rol_id": 1434976889738498099,  # ← ID AQUÍ
                "requisitos": {"nivel": 90}
            },
        }

        # -----------------------------
        # 🎉 TIENDA EVENTOS
        # -----------------------------
        self.tienda_eventos = {
            "Night Lover": {
                "precio": 30,
                "rol_id": 1434976885653242000,  # ← ID AQUÍ
                "requisitos": "eventos"
            }
        }

        # -----------------------------
        # 💛 TIENDA VIP
        # -----------------------------
        self.tienda_vip = {
            "Fake VIP": {
                "precio": 70,
                "rol_id": 1434976886940762192,  # ← ID AQUÍ
                "requisitos": {"años": 1}
            },
            "e-pink": {
                "precio": 77,
                "rol_id": 1434976888270618736,  # ← ID AQUÍ
                "requisitos": {"nivel": 100}
            },
            "Casino": {
                "precio": 80,
                "rol_id": 1434976892901003465,  # ← ID AQUÍ
                "requisitos": {"rangos": self.roles_casino_requeridos}
            }
        }

    # =======================================================
    # ⚙ FUNCIONES INTERNAS
    # =======================================================

    def get_user(self, user_id):
        self.cursor.execute("SELECT coins, last_daily FROM economia WHERE user_id = ?", (user_id,))
        data = self.cursor.fetchone()

        if data is None:
            self.cursor.execute(
                "INSERT INTO economia (user_id, coins, last_daily) VALUES (?, ?, ?)",
                (user_id, 0, None)
            )
            self.conn.commit()
            return (0, None)

        return data

    def update_coins(self, user_id, amount):
        coins, last_daily = self.get_user(user_id)
        new_amount = coins + amount
        self.cursor.execute("UPDATE economia SET coins = ? WHERE user_id = ?", (new_amount, user_id))
        self.conn.commit()

    # =======================================================
    # 🎁 /diario
    # =======================================================
    @app_commands.command(name="diario", description="Reclama 50 Lekacoins diarios.")
    async def diario(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        coins, last_daily = self.get_user(user_id)

        if last_daily:
            last_time = datetime.fromisoformat(last_daily)
            if datetime.now() - last_time < timedelta(hours=24):
                espera = (last_time + timedelta(hours=24)) - datetime.now()
                horas = espera.seconds // 3600
                minutos = (espera.seconds % 3600) // 60

                return await interaction.response.send_message(
                    f"⏳ Ya reclamaste tu recompensa. Vuelve en **{horas}h {minutos}m**.",
                    ephemeral=True
                )

        self.update_coins(user_id, 50)
        self.cursor.execute("UPDATE economia SET last_daily = ? WHERE user_id = ?",
                            (datetime.now().isoformat(), user_id))
        self.conn.commit()

        await interaction.response.send_message(
            "🎁 **Has recibido 50 Lekacoins!**",
            ephemeral=True
        )

    # =======================================================
    # 💰 /monedas
    # =======================================================
    @app_commands.command(name="monedas", description="Muestra tu saldo de Lekacoins.")
    async def monedas(self, interaction: discord.Interaction):
        coins, _ = self.get_user(interaction.user.id)
        await interaction.response.send_message(
            f"💰 Tienes **{coins} Lekacoins**.",
            ephemeral=True
        )

    # =======================================================
    # 🛒 /tienda
    # =======================================================
    @app_commands.command(name="tienda", description="Muestra las tiendas disponibles.")
    async def tienda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 Tiendas del Servidor",
            description="Usa `/comprar nombre_del_rol` para comprar.",
            color=discord.Color.gold()
        )

        # Normal
        txt = ""
        for nombre, info in self.tienda_normal.items():
            txt += f"**{nombre}** — {info['precio']} 💰\n"
        embed.add_field(name="🟢 Tienda Normal", value=txt, inline=False)

        # Eventos
        if self.eventos_activos:
            txt = ""
            for nombre, info in self.tienda_eventos.items():
                txt += f"**{nombre}** — {info['precio']} 💰\n"
            embed.add_field(name="🎉 Tienda Eventos (ACTIVA)", value=txt, inline=False)
        else:
            embed.add_field(name="🎉 Tienda Eventos",
                            value="🚫 Actualmente desactivada",
                            inline=False)

        # VIP
        txt = ""
        for nombre, info in self.tienda_vip.items():
            txt += f"**{nombre}** — {info['precio']} 💰\n"
        embed.add_field(name="💛 Tienda VIP", value=txt, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # =======================================================
    # 🛒 /comprar
    # =======================================================
    @app_commands.command(name="comprar", description="Compra un rol con Lekacoins.")
    @app_commands.describe(rol="Nombre EXACTO del rol.")
    async def comprar(self, interaction: discord.Interaction, rol: str):

        rol = rol.strip()

        # Buscar en las tiendas
        tiendas = [
            self.tienda_normal,
            self.tienda_eventos if self.eventos_activos else {},
            self.tienda_vip
        ]

        for tienda in tiendas:
            if rol in tienda:
                info = tienda[rol]
                break
        else:
            return await interaction.response.send_message(
                "❌ Ese rol no existe o no está disponible.",
                ephemeral=True
            )

        precio = info["precio"]
        rol_id = info["rol_id"]
        requisitos = info["requisitos"]

        coins, _ = self.get_user(interaction.user.id)

        if coins < precio:
            return await interaction.response.send_message(
                f"❌ Necesitas {precio} Lekacoins, tienes {coins}.",
                ephemeral=True
            )

        # =============================
        # ✔ VERIFICAR REQUISITOS
        # =============================
        member = interaction.user

        # Requisito de edad
        if requisitos and "edad" in requisitos:
            if requisitos["edad"] == "+13":
                if self.ROL_MAYORES not in [r.id for r in member.roles]:
                    return await interaction.response.send_message(
                        "❌ Solo mayores de 13 pueden comprar este rol.",
                        ephemeral=True
                    )

        # Requisito Calvo (especial)
        if requisitos and "calvo" in requisitos:
            if self.ROL_MENEORES in [r.id for r in member.roles]:
                # Si es menor → necesita nivel 50
                if self.roles_nivel[50] not in [r.id for r in member.roles]:
                    return await interaction.response.send_message(
                        "❌ Necesitas nivel 50 para comprar 'Calvo'.",
                        ephemeral=True
                    )

        # Requisito nivel
        if requisitos and "nivel" in requisitos:
            nivel_requerido = requisitos["nivel"]
            if self.roles_nivel[nivel_requerido] not in [r.id for r in member.roles]:
                return await interaction.response.send_message(
                    f"❌ Necesitas nivel {nivel_requerido} para comprar este rol.",
                    ephemeral=True
                )

        # Requisito eventos
        if requisitos == "eventos":
            if self.ROL_EVENTOS not in [r.id for r in member.roles]:
                return await interaction.response.send_message(
                    "❌ Solo disponible durante eventos.",
                    ephemeral=True
                )

        # Requisito años en el servidor
        if requisitos and "años" in requisitos:
            años = requisitos["años"]

            self.cursor.execute("SELECT joined_at FROM ingresos WHERE user_id = ?", (member.id,))
            dato = self.cursor.fetchone()

            if not dato:
                return await interaction.response.send_message(
                    "❌ No puedo verificar tu tiempo en el servidor.",
                    ephemeral=True
                )

            fecha = datetime.fromisoformat(dato[0])
            if (datetime.now() - fecha).days < 365 * años:
                return await interaction.response.send_message(
                    f"❌ Necesitas **{años} año(s)** en el servidor.",
                    ephemeral=True
                )

        # Requisito roles casino
        if requisitos and "rangos" in requisitos:
            roles_usuario = [r.id for r in member.roles]
            if not any(r in roles_usuario for r in requisitos["rangos"]):
                return await interaction.response.send_message(
                    "❌ Solo Moderadores / Staff / Administradores pueden comprar esto.",
                    ephemeral=True
                )

        # Compra válida
        self.update_coins(member.id, -precio)
        await member.add_roles(interaction.guild.get_role(rol_id))

        await interaction.response.send_message(
            f"✔ Has comprado **{rol}** por {precio} Lekacoins.",
            ephemeral=True
        )

    # =======================================================
    # 🎉 ACTIVAR EVENTOS
    # =======================================================
    @app_commands.command(name="activar_eventos", description="Activa la tienda de eventos.")
    @commands.is_owner()
    async def activar_eventos(self, interaction: discord.Interaction):

        self.eventos_activos = True

        # Dar rol Eventos a todos
        rol = interaction.guild.get_role(self.ROL_EVENTOS)
        for member in interaction.guild.members:
            if not member.bot:
                try:
                    await member.add_roles(rol)
                except:
                    pass

        await interaction.response.send_message(
            "🎉 **Tienda de Eventos ACTIVADA**\nEl rol de eventos fue asignado a todos los usuarios.",
            ephemeral=True
        )

    # =======================================================
    # 🚫 DESACTIVAR EVENTOS
    # =======================================================
    @app_commands.command(name="desactivar_eventos", description="Desactiva la tienda de eventos.")
    @commands.is_owner()
    async def desactivar_eventos(self, interaction: discord.Interaction):

        self.eventos_activos = False

        rol = interaction.guild.get_role(self.ROL_EVENTOS)
        for member in interaction.guild.members:
            if not member.bot:
                try:
                    await member.remove_roles(rol)
                except:
                    pass

        await interaction.response.send_message(
            "🚫 **Tienda de Eventos DESACTIVADA**\nEl rol de eventos fue removido de todos los usuarios.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Economia(bot))