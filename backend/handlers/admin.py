import base64
import json as _json
import tornado.escape
import bcrypt

from backend.handlers.base import BaseHandler
from backend.db.db import db_interface

STAFF_ROLES = {"ADMIN", "PROFESSORE"}


def _is_staff(ruolo):
    return ruolo in STAFF_ROLES


class AdminUsersHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        users = await db_interface.get_all_users()
        self.write_json({"users": users})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo_caller = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo_caller):
            return self.write_json({"error": "Accesso negato"}, 403)
        body = tornado.escape.json_decode(self.request.body)
        email = body.get("email", "").strip()
        password = body.get("password", "")
        ruolo_nuovo = body.get("ruolo", "USER").upper()
        if not email or not password:
            return self.write_json({"error": "Email e password obbligatorie"}, 400)
        if ruolo_caller == "PROFESSORE" and ruolo_nuovo != "USER":
            return self.write_json({"error": "Il professore puo creare solo studenti"}, 403)
        if ruolo_nuovo not in ("ADMIN", "PROFESSORE", "USER"):
            return self.write_json({"error": "Ruolo non valido"}, 400)
        existing = await db_interface.get_user_by_email(email)
        if existing:
            return self.write_json({"error": "Utente gia esistente"}, 400)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        result = await db_interface.create_user(email, hashed, ruolo_nuovo)
        return self.write_json({
            "message": f"Utente {email} creato con ruolo {ruolo_nuovo}",
            "user_id": result.inserted_id,
            "email": email,
            "ruolo": ruolo_nuovo,
        }, 201)

    async def delete(self, user_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo_caller = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo_caller):
            return self.write_json({"error": "Accesso negato"}, 403)
        if str(user["id"]) == str(user_id):
            return self.write_json({"error": "Non puoi cancellare te stesso"}, 400)
        if ruolo_caller == "PROFESSORE":
            all_users = await db_interface.get_all_users()
            target_user = next((u for u in all_users if str(u["id"]) == str(user_id)), None)
            if not target_user:
                return self.write_json({"error": "Utente non trovato"}, 404)
            if target_user["ruolo"] != "USER":
                return self.write_json({"error": "Il professore puo eliminare solo studenti"}, 403)
        success = await db_interface.delete_user(int(user_id))
        if success:
            return self.write_json({"message": "Utente eliminato"})
        else:
            return self.write_json({"error": "Utente non trovato"}, 404)


class AdminUserResubmitHandler(BaseHandler):
    async def post(self, user_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        success = await db_interface.set_resubmit_allowed(int(user_id), True)
        if success:
            return self.write_json({"message": "Autorizzazione concessa."})
        else:
            return self.write_json({"error": "Utente non trovato"}, 404)

    async def delete(self, user_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        success = await db_interface.set_resubmit_allowed(int(user_id), False)
        if success:
            return self.write_json({"message": "Autorizzazione revocata."})
        else:
            return self.write_json({"error": "Utente non trovato"}, 404)


class AdminUserSurveyHandler(BaseHandler):
    async def get(self, user_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        responses = await db_interface.get_survey_responses_by_user(int(user_id))
        self.write_json({"responses": responses, "count": len(responses)})


class AdminSurveyResponsesHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        responses = await db_interface.get_all_survey_responses()
        self.write_json({"responses": responses})

    async def delete(self, response_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        success = await db_interface.delete_survey_response(int(response_id))
        if success:
            return self.write_json({"message": "Risposta eliminata con successo"})
        else:
            return self.write_json({"error": "Risposta non trovata"}, 404)


class AdminExportHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if ruolo != "ADMIN":
            return self.write_json({"error": "Accesso riservato agli admin"}, 403)
        raw_users = await db_interface.get_all_users_with_passwords()
        users_export = []
        for u in raw_users:
            pw = u["password"]
            pw_b64 = base64.b64encode(pw if isinstance(pw, (bytes, bytearray)) else pw.encode()).decode("ascii")
            users_export.append({"id": u["id"], "email": u["email"], "ruolo": u["ruolo"],
                                  "resubmit_allowed": int(u["resubmit_allowed"]), "password_hash_b64": pw_b64})
        survey_responses = await db_interface.get_all_survey_responses()
        enti = await db_interface.get_all_enti()
        for e in enti:
            if hasattr(e.get("created_at"), "isoformat"):
                e["created_at"] = e["created_at"].isoformat()
        assignments = await db_interface.get_all_assignments()
        payload = {"export_version": 1, "users": users_export,
                   "survey_responses": survey_responses, "enti": enti, "assignments": assignments}
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_header("Content-Disposition", 'attachment; filename="stage_review_export.json"')
        self.write(_json.dumps(payload, ensure_ascii=False, indent=2, default=str))


class AdminImportHandler(BaseHandler):
    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if ruolo != "ADMIN":
            return self.write_json({"error": "Accesso riservato agli admin"}, 403)
        try:
            # Il frontend invia il file come multipart/form-data con campo "file"
            if self.request.files and "file" in self.request.files:
                raw = self.request.files["file"][0]["body"]
                data = _json.loads(raw.decode("utf-8"))
            else:
                # Fallback: body JSON grezzo (es. chiamate API dirette)
                data = tornado.escape.json_decode(self.request.body)
        except Exception:
            return self.write_json({"error": "JSON non valido"}, 400)
        stats = {"users_created": 0, "users_skipped": 0, "survey_responses_imported": 0,
                 "enti_created": 0, "enti_skipped": 0, "assignments_imported": 0, "errors": []}
        email_to_id = {}
        for u in data.get("users", []):
            try:
                email = u["email"]
                pw_bytes = base64.b64decode(u["password_hash_b64"])
                new_id = await db_interface.import_user(email, pw_bytes, u.get("ruolo", "USER"), int(u.get("resubmit_allowed", 0)))
                email_to_id[email] = new_id
                existing = await db_interface.get_user_by_email(email)
                if existing and existing["id"] != u.get("id"):
                    stats["users_skipped"] += 1
                else:
                    stats["users_created"] += 1
            except Exception as exc:
                stats["errors"].append(f"Utente {u.get('email', '?')}: {exc}")
        for u in data.get("users", []):
            email = u.get("email", "")
            if email and email not in email_to_id:
                ex = await db_interface.get_user_by_email(email)
                if ex:
                    email_to_id[email] = ex["id"]
        for resp in data.get("survey_responses", []):
            try:
                email = resp["email"]
                uid = email_to_id.get(email)
                if not uid:
                    ex = await db_interface.get_user_by_email(email)
                    uid = ex["id"] if ex else None
                if not uid:
                    stats["errors"].append(f"Risposta: utente {email} non trovato")
                    continue
                await db_interface.import_survey_response(uid, email, resp.get("responses", {}), resp.get("submitted_at", ""))
                stats["survey_responses_imported"] += 1
            except Exception as exc:
                stats["errors"].append(f"Risposta: {exc}")
        nome_to_ente_id = {}
        for e in data.get("enti", []):
            try:
                nome = e["nome"]
                new_eid = await db_interface.import_ente(
                    nome, e.get("descrizione", ""), e.get("indirizzo", ""), e.get("referente", ""),
                    e.get("posti_disponibili"), e.get("orari_lavoro")
                )
                nome_to_ente_id[nome] = new_eid
                ex_enti = await db_interface.get_all_enti()
                if any(x["nome"] == nome and x["id"] != e.get("id") for x in ex_enti):
                    stats["enti_skipped"] += 1
                else:
                    stats["enti_created"] += 1
            except Exception as exc:
                stats["errors"].append(f"Ente {e.get('nome', '?')}: {exc}")
        for asgn in data.get("assignments", []):
            try:
                sem = asgn.get("student_email", "")
                enm = asgn.get("ente_nome", "")
                uid = email_to_id.get(sem)
                if not uid:
                    ex = await db_interface.get_user_by_email(sem)
                    uid = ex["id"] if ex else None
                eid = nome_to_ente_id.get(enm)
                if not uid or not eid:
                    stats["errors"].append(f"Assegnazione: utente o ente non trovati")
                    continue
                await db_interface.import_assignment(uid, eid, asgn.get("data_inizio", ""), asgn.get("data_fine", ""), asgn.get("note", ""))
                stats["assignments_imported"] += 1
            except Exception as exc:
                stats["errors"].append(f"Assegnazione: {exc}")
        self.write_json({"message": "Import completato", "stats": stats})
