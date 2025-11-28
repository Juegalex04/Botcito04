import discord
from discord.ext import commands
import sqlite3
import random
import time

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ========= CONEXIÓN A LA BASE DE DATOS =========
        self.db = sqlite3.connect("levels.db")
        self.cursor = self.db.cursor()

        # Crear tabla si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS niveles (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER,
                nivel INTEGER,
                last_xp_time REAL
            )
        """)
        self.db.commit()

    # ============================================================
    # FUNCIONES DE XP Y NIVELES
    # ============================================================
    def calcular_xp_necesario(self, nivel):
        """Devuelve la XP necesaria según el nivel actual."""
        if nivel < 10:
            return 100
        elif nivel < 30:
            return 150
        elif nivel < 50:
            return 200
        elif nivel < 70:
            return 400
        else:
            return 800  # para niveles 71–100

    def obtener_datos_usuario(self, user_id):
        """Obtiene XP y nivel del usuario."""
        self.cursor.execute("SELECT xp, nivel, last_xp_time FROM niveles WHERE user_id = ?", (user_id,))
        data = self.cursor.fetchone()

        if data is None:
            # Si no existe, crear entrada nueva
            self.cursor.execute(
                "INSERT INTO niveles (user_id, xp, nivel, last_xp_time) VALUES (?, ?, ?, ?)",
                (user_id, 0, 1, 0)
            )
            self.db.commit()
            return (0, 1, 0)

        return data

    def actualizar_usuario(self, user_id, xp, nivel, last_time):
        """Actualiza datos del usuario."""
        self.cursor.execute(
            "UPDATE niveles SET xp = ?, nivel = ?, last_xp_time = ? WHERE user_id = ?",
            (xp, nivel, last_time, user_id)
        )
        self.db.commit()

    # ============================================================
    # EVENTO DE MENSAJE (GANAR XP)
    # ============================================================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_id = message.author.id
        xp_actual, nivel_actual, last_time = self.obtener_datos_usuario(user_id)

        # Antispam — Solo XP cada 60 segundos
        ahora = time.time()
        if ahora - last_time < 60:
            return

        # Dar XP (5–15)
        xp_ganada = random.randint(5, 15)
        xp_nueva = xp_actual + xp_ganada

        xp_necesaria = self.calcular_xp_necesario(nivel_actual)

        # Comprobar si sube de nivel
        if xp_nueva >= xp_necesaria:
            nivel_nuevo = nivel_actual + 1
            xp_restante = xp_nueva - xp_necesaria

            # Guardar avance
            self.actualizar_usuario(user_id, xp_restante, nivel_nuevo, ahora)

            # Enviar mensaje privado
            try:
                await message.author.send(
                    f"🎉 **¡Subiste de nivel!**\n"
                    f"Ahora eres nivel **{nivel_nuevo}** 💜\n"
                    f"¡Sigue chateando para subir más!\n"
                )
            except:
                pass  # Por si el usuario tiene MD cerrados

            # Asignar rol si es múltiplo de 10
            if nivel_nuevo % 10 == 0:
                rol_id = self.obtener_rol_por_nivel(nivel_nuevo)
                if rol_id:
                    rol = message.guild.get_role(rol_id)
                    if rol:
                        await message.author.add_roles(rol)

        else:
            # Actualizar XP sin subir nivel
            self.actualizar_usuario(user_id, xp_nueva, nivel_actual, ahora)

    # ============================================================
    # ASIGNAR ROLES SEGÚN NIVEL
    # ============================================================
    def obtener_rol_por_nivel(self, nivel):
        """Devuelve el ID del rol correspondiente a cada nivel 10–100."""
        roles = {
            10:  1434976824395567226,
            20:  1434976825116725322,
            30:  1434976826299777128,
            40:  1434976826534527117,
            50:  1434976827281113108,
            60:  1434976827864125460,
            70:  1434976828648456212,
            80:  1434976829285994576,
            90:  1434976829935976488,
            100: 1434976830569582623,
        }

        return roles.get(nivel, None)


async def setup(bot):
    await bot.add_cog(LevelSystem(bot))