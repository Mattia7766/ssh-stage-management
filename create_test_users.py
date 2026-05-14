#!/usr/bin/env python3
"""Crea utenti di test ADMIN e USER"""

import asyncio
import aiomysql
import bcrypt


async def create_test_users():
    """Inserisce un utente ADMIN e un utente USER"""

    conn = await aiomysql.connect(
        host="localhost",
        port=3306,
        user="student",
        password="Pass",
        db="DB_SSH_todo_app2"
    )

    async with conn.cursor() as cursor:

        # Crea utente ADMIN
        admin_email = "admin@todo.com"
        admin_password = "admin123"
        admin_hashed = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt())

        try:
            await cursor.execute("""
                                 INSERT INTO users (email, password, ruolo)
                                 VALUES (%s, %s, %s) ON DUPLICATE KEY
                                 UPDATE
                                     password =
                                 VALUES (password), ruolo =
                                 VALUES (ruolo)
                                 """, (admin_email, admin_hashed, "ADMIN"))
            print(f"✅ Utente ADMIN creato: {admin_email} (password: {admin_password})")
        except Exception as e:
            print(f"❌ Errore creazione ADMIN: {e}")

        # Crea utente USER
        user_email = "user@todo.com"
        user_password = "user123"
        user_hashed = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())

        try:
            await cursor.execute("""
                                 INSERT INTO users (email, password, ruolo)
                                 VALUES (%s, %s, %s) ON DUPLICATE KEY
                                 UPDATE
                                     password =
                                 VALUES (password), ruolo =
                                 VALUES (ruolo)
                                 """, (user_email, user_hashed, "USER"))
            print(f"✅ Utente USER creato: {user_email} (password: {user_password})")
        except Exception as e:
            print(f"❌ Errore creazione USER: {e}")

    await conn.commit()
    conn.close()
    print("\n🎉 Operazione completata!")


if __name__ == "__main__":
    asyncio.run(create_test_users())