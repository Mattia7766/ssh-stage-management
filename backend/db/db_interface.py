from datetime import datetime, date
import aiomysql
import json


class DatabaseInterface:
    def __init__(self, get_pool_func):
        self._get_pool = get_pool_func

    async def _ensure_tables(self):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # ── users ──────────────────────────────────────────────────
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARBINARY(255) NOT NULL,
                        ruolo ENUM('ADMIN', 'PROFESSORE', 'USER') DEFAULT 'USER',
                        resubmit_allowed TINYINT(1) NOT NULL DEFAULT 0
                    )
                """)
                # Migrazione: aggiungi resubmit_allowed se mancante
                try:
                    await cursor.execute("""
                        ALTER TABLE users
                        ADD COLUMN resubmit_allowed TINYINT(1) NOT NULL DEFAULT 0
                    """)
                except Exception:
                    pass
                # Migrazione: aggiorna ENUM per includere PROFESSORE
                try:
                    await cursor.execute("""
                        ALTER TABLE users
                        MODIFY COLUMN ruolo ENUM('ADMIN', 'PROFESSORE', 'USER') DEFAULT 'USER'
                    """)
                except Exception:
                    pass

                # ── survey_responses ───────────────────────────────────────
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS survey_responses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        responses JSON NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)

                # ── enti ───────────────────────────────────────────────────
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS enti (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        descrizione TEXT,
                        indirizzo VARCHAR(255),
                        referente VARCHAR(255),
                        posti_disponibili INT DEFAULT NULL,
                        orari_lavoro JSON DEFAULT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Migrazioni enti
                for col, defn in [
                    ("posti_disponibili", "INT DEFAULT NULL"),
                    ("orari_lavoro",      "JSON DEFAULT NULL"),
                ]:
                    try:
                        await cursor.execute(
                            f"ALTER TABLE enti ADD COLUMN {col} {defn}"
                        )
                    except Exception:
                        pass

                # ── student_assignments ────────────────────────────────────
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_assignments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        ente_id INT NOT NULL,
                        data_inizio DATE NOT NULL,
                        data_fine DATE NOT NULL,
                        note TEXT,
                        orari_personalizzati JSON DEFAULT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (ente_id) REFERENCES enti(id) ON DELETE CASCADE
                    )
                """)
                # Migrazione assignments
                try:
                    await cursor.execute(
                        "ALTER TABLE student_assignments ADD COLUMN orari_personalizzati JSON DEFAULT NULL"
                    )
                except Exception:
                    pass

                # ── student_preferences ────────────────────────────────────
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_preferences (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        ente_id INT NOT NULL,
                        ordine TINYINT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (ente_id) REFERENCES enti(id) ON DELETE CASCADE,
                        UNIQUE KEY uniq_user_ordine (user_id, ordine)
                    )
                """)

    # ══════════════════════════════════════════════════════════════════════
    #  USERS
    # ══════════════════════════════════════════════════════════════════════
    async def check_user(self, email: str):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT ruolo FROM users WHERE email = %s", (email,)
                )
                utente = await cursor.fetchone()
                return utente["ruolo"] if utente else None

    async def get_user_by_email(self, email: str):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT id, email, password, ruolo, resubmit_allowed FROM users WHERE email = %s",
                    (email,)
                )
                user = await cursor.fetchone()
                if user:
                    user["_id"] = user["id"]
                return user

    async def create_user(self, email: str, hashed_password: bytes, ruolo: str = "USER"):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO users (email, password, ruolo) VALUES (%s, %s, %s)",
                    (email, hashed_password, ruolo)
                )
                return type('obj', (object,), {'inserted_id': cursor.lastrowid})()

    async def get_all_users(self):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT id, email, ruolo, resubmit_allowed FROM users ORDER BY email"
                )
                return await cursor.fetchall()

    async def get_users_by_role(self, ruolo: str):
        """Restituisce tutti gli utenti con un certo ruolo."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT id, email, ruolo, resubmit_allowed FROM users WHERE ruolo = %s ORDER BY email",
                    (ruolo,)
                )
                return await cursor.fetchall()

    async def delete_user(self, user_id: int):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                return cursor.rowcount > 0

    async def set_resubmit_allowed(self, user_id: int, allowed: bool) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE users SET resubmit_allowed = %s WHERE id = %s",
                    (1 if allowed else 0, user_id)
                )
                return cursor.rowcount > 0

    async def get_resubmit_allowed(self, user_id: int) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT resubmit_allowed FROM users WHERE id = %s", (user_id,)
                )
                row = await cursor.fetchone()
                return bool(row[0]) if row else False

    # ══════════════════════════════════════════════════════════════════════
    #  SURVEY
    # ══════════════════════════════════════════════════════════════════════
    async def save_survey_response(self, user_id: int, email: str, responses: dict):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO survey_responses (user_id, email, responses) VALUES (%s, %s, %s)",
                    (user_id, email, json.dumps(responses))
                )
                return cursor.lastrowid

    async def get_all_survey_responses(self):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT sr.id, sr.user_id, sr.email, sr.submitted_at, sr.responses, u.ruolo
                    FROM survey_responses sr
                    JOIN users u ON sr.user_id = u.id
                    ORDER BY sr.submitted_at DESC
                """)
                rows = await cursor.fetchall()
                for r in rows:
                    if r.get("submitted_at"):
                        r["submitted_at"] = r["submitted_at"].isoformat()
                    try:
                        r["responses"] = json.loads(r["responses"]) if r.get("responses") else {}
                    except Exception:
                        r["responses"] = {}
                return rows

    async def get_survey_responses_by_user(self, user_id: int):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT id, user_id, email, submitted_at, responses
                    FROM survey_responses
                    WHERE user_id = %s
                    ORDER BY submitted_at DESC
                """, (user_id,))
                rows = await cursor.fetchall()
                for r in rows:
                    if r.get("submitted_at"):
                        r["submitted_at"] = r["submitted_at"].isoformat()
                    try:
                        r["responses"] = json.loads(r["responses"]) if r.get("responses") else {}
                    except Exception:
                        r["responses"] = {}
                return rows

    async def get_survey_submission_count(self, user_id: int) -> int:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT COUNT(*) FROM survey_responses WHERE user_id = %s", (user_id,)
                )
                result = await cursor.fetchone()
                return result[0]

    async def user_has_submitted_survey(self, user_id: int) -> bool:
        return (await self.get_survey_submission_count(user_id)) > 0

    async def delete_survey_response(self, response_id: int) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM survey_responses WHERE id = %s", (response_id,)
                )
                return cursor.rowcount > 0

    # ══════════════════════════════════════════════════════════════════════
    #  EXPORT / IMPORT
    # ══════════════════════════════════════════════════════════════════════
    async def get_all_users_with_passwords(self):
        """Restituisce tutti gli utenti inclusi gli hash della password (per export)."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT id, email, password, ruolo, resubmit_allowed FROM users ORDER BY id"
                )
                return await cursor.fetchall()

    async def import_user(self, email: str, password_bytes: bytes, ruolo: str, resubmit_allowed: int) -> int:
        """Inserisce un utente se non esiste ancora (per email). Restituisce l'id."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                row = await cursor.fetchone()
                if row:
                    return row["id"]
                await cursor.execute(
                    "INSERT INTO users (email, password, ruolo, resubmit_allowed) VALUES (%s, %s, %s, %s)",
                    (email, password_bytes, ruolo, resubmit_allowed)
                )
                return cursor.lastrowid

    async def import_survey_response(self, user_id: int, email: str, responses: dict, submitted_at: str):
        """Inserisce una risposta al questionario con timestamp specifico (per import)."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO survey_responses (user_id, email, responses, submitted_at) VALUES (%s, %s, %s, %s)",
                    (user_id, email, json.dumps(responses), submitted_at)
                )
                return cursor.lastrowid

    async def import_ente(self, nome: str, descrizione: str, indirizzo: str, referente: str,
                          posti_disponibili=None, orari_lavoro=None) -> int:
        """Crea un ente se non esiste (per nome). Restituisce l'id."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id FROM enti WHERE nome = %s", (nome,))
                row = await cursor.fetchone()
                if row:
                    return row["id"]
                await cursor.execute(
                    "INSERT INTO enti (nome, descrizione, indirizzo, referente, posti_disponibili, orari_lavoro) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nome, descrizione or "", indirizzo or "", referente or "",
                     posti_disponibili,
                     json.dumps(orari_lavoro) if orari_lavoro is not None else None)
                )
                return cursor.lastrowid

    async def import_assignment(self, user_id: int, ente_id: int, data_inizio: str, data_fine: str, note: str) -> int:
        """Inserisce un'assegnazione (per import)."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO student_assignments (user_id, ente_id, data_inizio, data_fine, note) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, ente_id, data_inizio, data_fine, note or "")
                )
                return cursor.lastrowid

    # ══════════════════════════════════════════════════════════════════════
    #  ENTI
    # ══════════════════════════════════════════════════════════════════════
    async def create_ente(self, nome: str, descrizione: str = "", indirizzo: str = "",
                          referente: str = "", posti_disponibili=None, orari_lavoro=None) -> int:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO enti (nome, descrizione, indirizzo, referente, posti_disponibili, orari_lavoro) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nome, descrizione, indirizzo, referente, posti_disponibili,
                     json.dumps(orari_lavoro) if orari_lavoro is not None else None)
                )
                return cursor.lastrowid

    async def get_all_enti(self):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM enti ORDER BY nome")
                rows = await cursor.fetchall()
                for r in rows:
                    if isinstance(r.get("orari_lavoro"), str):
                        try:
                            r["orari_lavoro"] = json.loads(r["orari_lavoro"])
                        except Exception:
                            r["orari_lavoro"] = None
                return rows

    async def get_ente_by_id(self, ente_id: int):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM enti WHERE id = %s", (ente_id,))
                r = await cursor.fetchone()
                if r and isinstance(r.get("orari_lavoro"), str):
                    try:
                        r["orari_lavoro"] = json.loads(r["orari_lavoro"])
                    except Exception:
                        r["orari_lavoro"] = None
                return r

    async def update_ente(self, ente_id: int, nome: str, descrizione: str, indirizzo: str,
                          referente: str, posti_disponibili=None, orari_lavoro=None) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE enti SET nome=%s, descrizione=%s, indirizzo=%s, referente=%s, posti_disponibili=%s, orari_lavoro=%s WHERE id=%s",
                    (nome, descrizione, indirizzo, referente, posti_disponibili,
                     json.dumps(orari_lavoro) if orari_lavoro is not None else None, ente_id)
                )
                return cursor.rowcount > 0

    async def check_disponibilita(self, ente_id: int, data_inizio: str, data_fine: str, exclude_assignment_id: int = None):
        """Controlla i posti disponibili per un ente nel periodo dato.
        Ritorna: {posti_totali, posti_occupati, posti_liberi, disponibile, occupato_fino_a}
        """
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "SELECT posti_disponibili FROM enti WHERE id = %s", (ente_id,)
                )
                ente = await cursor.fetchone()
                if not ente or ente["posti_disponibili"] is None:
                    return {"posti_totali": None, "posti_occupati": 0,
                            "posti_liberi": None, "disponibile": True, "occupato_fino_a": None}

                posti_totali = ente["posti_disponibili"]

                # Conta assegnazioni che si sovrappongono al periodo richiesto
                excl = f" AND sa.id != {int(exclude_assignment_id)}" if exclude_assignment_id else ""
                await cursor.execute(f"""
                    SELECT COUNT(*) AS cnt
                    FROM student_assignments sa
                    WHERE sa.ente_id = %s
                      AND sa.data_inizio <= %s
                      AND sa.data_fine >= %s
                      {excl}
                """, (ente_id, data_fine, data_inizio))
                row = await cursor.fetchone()
                posti_occupati = row["cnt"] if row else 0
                posti_liberi = posti_totali - posti_occupati
                disponibile = posti_liberi > 0

                # Se non disponibile, calcola la prima data in cui si libera un posto:
                # = il MIN(data_fine) tra le assegnazioni che si sovrappongono al periodo richiesto.
                # Dal giorno successivo a quella data l'ente avrà almeno un posto libero.
                occupato_fino_a = None
                if not disponibile:
                    await cursor.execute(f"""
                        SELECT MIN(sa.data_fine) AS fine
                        FROM student_assignments sa
                        WHERE sa.ente_id = %s
                          AND sa.data_inizio <= %s
                          AND sa.data_fine   >= %s
                          {excl}
                    """, (ente_id, data_fine, data_inizio))
                    r2 = await cursor.fetchone()
                    if r2 and r2.get("fine"):
                        fine = r2["fine"]
                        occupato_fino_a = fine.isoformat() if hasattr(fine, "isoformat") else str(fine)

                return {
                    "posti_totali": posti_totali,
                    "posti_occupati": posti_occupati,
                    "posti_liberi": max(0, posti_liberi),
                    "disponibile": disponibile,
                    "occupato_fino_a": occupato_fino_a,
                }

    async def delete_ente(self, ente_id: int) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM enti WHERE id = %s", (ente_id,))
                return cursor.rowcount > 0

    # ══════════════════════════════════════════════════════════════════════
    #  STUDENT ASSIGNMENTS
    # ══════════════════════════════════════════════════════════════════════
    async def assign_student(self, user_id: int, ente_id: int, data_inizio: str, data_fine: str,
                             note: str = "", orari_personalizzati=None) -> int:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """INSERT INTO student_assignments (user_id, ente_id, data_inizio, data_fine, note, orari_personalizzati)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (user_id, ente_id, data_inizio, data_fine, note,
                     json.dumps(orari_personalizzati) if orari_personalizzati is not None else None)
                )
                return cursor.lastrowid

    async def update_assignment(self, assignment_id: int, ente_id: int, data_inizio: str, data_fine: str,
                                note: str = "", orari_personalizzati=None) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """UPDATE student_assignments
                       SET ente_id=%s, data_inizio=%s, data_fine=%s, note=%s, orari_personalizzati=%s
                       WHERE id=%s""",
                    (ente_id, data_inizio, data_fine, note,
                     json.dumps(orari_personalizzati) if orari_personalizzati is not None else None,
                     assignment_id)
                )
                return cursor.rowcount > 0

    async def delete_assignment(self, assignment_id: int) -> bool:
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM student_assignments WHERE id = %s", (assignment_id,)
                )
                return cursor.rowcount > 0

    async def get_assignment_by_user(self, user_id: int):
        """Restituisce l'assegnazione attiva (o più recente) di uno studente."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT sa.id, sa.user_id, sa.ente_id, sa.data_inizio, sa.data_fine, sa.note,
                           sa.orari_personalizzati,
                           e.nome AS ente_nome, e.indirizzo AS ente_indirizzo,
                           e.referente AS ente_referente, e.descrizione AS ente_descrizione,
                           e.orari_lavoro AS ente_orari_lavoro
                    FROM student_assignments sa
                    JOIN enti e ON sa.ente_id = e.id
                    WHERE sa.user_id = %s
                    ORDER BY sa.data_inizio DESC
                    LIMIT 1
                """, (user_id,))
                row = await cursor.fetchone()
                if row:
                    for field in ("data_inizio", "data_fine"):
                        if isinstance(row[field], (datetime, date)):
                            row[field] = row[field].isoformat()
                    # Decode JSON orari fields so handlers always receive dicts
                    for field in ("orari_personalizzati", "ente_orari_lavoro"):
                        if isinstance(row.get(field), str):
                            try:
                                row[field] = json.loads(row[field])
                            except Exception:
                                row[field] = None
                return row

    async def get_all_assignments(self):
        """Restituisce tutte le assegnazioni con dati utente ed ente."""
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT sa.id, sa.user_id, sa.ente_id, sa.data_inizio, sa.data_fine, sa.note,
                           u.email AS student_email,
                           e.nome AS ente_nome
                    FROM student_assignments sa
                    JOIN users u ON sa.user_id = u.id
                    JOIN enti e ON sa.ente_id = e.id
                    ORDER BY sa.data_inizio DESC
                """)
                rows = await cursor.fetchall()
                for r in rows:
                    for field in ("data_inizio", "data_fine"):
                        if isinstance(r[field], (datetime, date)):
                            r[field] = r[field].isoformat()
                return rows

    async def get_assignments_by_ente(self, ente_id: int):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT sa.id, sa.user_id, sa.data_inizio, sa.data_fine, sa.note,
                           u.email AS student_email
                    FROM student_assignments sa
                    JOIN users u ON sa.user_id = u.id
                    WHERE sa.ente_id = %s
                    ORDER BY sa.data_inizio DESC
                """, (ente_id,))
                rows = await cursor.fetchall()
                for r in rows:
                    for field in ("data_inizio", "data_fine"):
                        if isinstance(r.get(field), (datetime, date)):
                            r[field] = r[field].isoformat()
                return rows

    # ══════════════════════════════════════════════════════════════════════
    #  STUDENT PREFERENCES
    # ══════════════════════════════════════════════════════════════════════
    async def save_preferences(self, user_id: int, ente_ids: list):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM student_preferences WHERE user_id = %s", (user_id,)
                )
                for i, ente_id in enumerate(ente_ids, 1):
                    await cursor.execute(
                        "INSERT INTO student_preferences (user_id, ente_id, ordine) VALUES (%s, %s, %s)",
                        (user_id, ente_id, i)
                    )

    async def get_preferences_by_user(self, user_id: int):
        pool = self._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("""
                    SELECT sp.ordine, sp.ente_id, e.nome AS ente_nome, e.indirizzo AS ente_indirizzo
                    FROM student_preferences sp
                    JOIN enti e ON sp.ente_id = e.id
                    WHERE sp.user_id = %s
                    ORDER BY sp.ordine
                """, (user_id,))
                return await cursor.fetchall()
