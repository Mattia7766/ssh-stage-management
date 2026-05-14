import tornado.escape
from backend.handlers.base import BaseHandler
from backend.db.db import db_interface

STAFF_ROLES = {"ADMIN", "PROFESSORE"}


def _is_staff(ruolo):
    return ruolo in STAFF_ROLES


# ══════════════════════════════════════════════════════════════════════════
#  ENTI
# ══════════════════════════════════════════════════════════════════════════
class EntiHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        enti = await db_interface.get_all_enti()
        for e in enti:
            if e.get("created_at"):
                e["created_at"] = e["created_at"].isoformat()
        self.write_json({"enti": enti})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        body = tornado.escape.json_decode(self.request.body)
        nome = body.get("nome", "").strip()
        if not nome:
            return self.write_json({"error": "Il nome dell'ente è obbligatorio"}, 400)

        posti = body.get("posti_disponibili")
        if posti is not None:
            try:
                posti = int(posti)
                if posti < 0:
                    posti = None
            except (ValueError, TypeError):
                posti = None

        ente_id = await db_interface.create_ente(
            nome=nome,
            descrizione=body.get("descrizione", ""),
            indirizzo=body.get("indirizzo", ""),
            referente=body.get("referente", ""),
            posti_disponibili=posti,
            orari_lavoro=body.get("orari_lavoro"),
        )
        return self.write_json({"message": "Ente creato", "id": ente_id}, 201)


class EnteDetailHandler(BaseHandler):
    async def get(self, ente_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        ente = await db_interface.get_ente_by_id(int(ente_id))
        if not ente:
            return self.write_json({"error": "Ente non trovato"}, 404)
        if ente.get("created_at"):
            ente["created_at"] = ente["created_at"].isoformat()

        assignments = await db_interface.get_assignments_by_ente(int(ente_id))
        self.write_json({"ente": ente, "assignments": assignments})

    async def put(self, ente_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        body = tornado.escape.json_decode(self.request.body)
        nome = body.get("nome", "").strip()
        if not nome:
            return self.write_json({"error": "Il nome è obbligatorio"}, 400)

        posti = body.get("posti_disponibili")
        if posti is not None:
            try:
                posti = int(posti)
                if posti < 0:
                    posti = None
            except (ValueError, TypeError):
                posti = None

        success = await db_interface.update_ente(
            int(ente_id), nome,
            body.get("descrizione", ""),
            body.get("indirizzo", ""),
            body.get("referente", ""),
            posti_disponibili=posti,
            orari_lavoro=body.get("orari_lavoro"),
        )
        if success:
            return self.write_json({"message": "Ente aggiornato"})
        return self.write_json({"error": "Ente non trovato"}, 404)

    async def delete(self, ente_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        success = await db_interface.delete_ente(int(ente_id))
        if success:
            return self.write_json({"message": "Ente eliminato"})
        return self.write_json({"error": "Ente non trovato"}, 404)


# ══════════════════════════════════════════════════════════════════════════
#  DISPONIBILITA
# ══════════════════════════════════════════════════════════════════════════
class DisponibilitaHandler(BaseHandler):
    """GET /api/enti/<id>/disponibilita?data_inizio=YYYY-MM-DD&data_fine=YYYY-MM-DD
       Ritorna: {posti_totali, posti_occupati, posti_liberi, disponibile, occupato_fino_a}
    """
    async def get(self, ente_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        data_inizio = self.get_argument("data_inizio", None)
        data_fine   = self.get_argument("data_fine", None)
        exclude_id  = self.get_argument("exclude", None)

        if not data_inizio or not data_fine:
            return self.write_json({"error": "data_inizio e data_fine sono obbligatorie"}, 400)

        result = await db_interface.check_disponibilita(
            int(ente_id), data_inizio, data_fine,
            exclude_assignment_id=int(exclude_id) if exclude_id else None
        )
        self.write_json(result)


# ══════════════════════════════════════════════════════════════════════════
#  ASSIGNMENTS
# ══════════════════════════════════════════════════════════════════════════
class AssignmentsHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        assignments = await db_interface.get_all_assignments()
        self.write_json({"assignments": assignments})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        body        = tornado.escape.json_decode(self.request.body)
        user_id     = body.get("user_id")
        ente_id     = body.get("ente_id")
        data_inizio = body.get("data_inizio", "").strip()
        data_fine   = body.get("data_fine", "").strip()
        note        = body.get("note", "")
        orari_pers  = body.get("orari_personalizzati")

        if not all([user_id, ente_id, data_inizio, data_fine]):
            return self.write_json({"error": "user_id, ente_id, data_inizio e data_fine sono obbligatori"}, 400)
        if data_inizio > data_fine:
            return self.write_json({"error": "La data di inizio deve essere precedente alla data di fine"}, 400)

        assignment_id = await db_interface.assign_student(
            int(user_id), int(ente_id), data_inizio, data_fine, note,
            orari_personalizzati=orari_pers
        )
        return self.write_json({"message": "Studente assegnato all'ente", "id": assignment_id}, 201)


class AssignmentDetailHandler(BaseHandler):
    async def put(self, assignment_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        body        = tornado.escape.json_decode(self.request.body)
        ente_id     = body.get("ente_id")
        data_inizio = body.get("data_inizio", "").strip()
        data_fine   = body.get("data_fine", "").strip()
        note        = body.get("note", "")
        orari_pers  = body.get("orari_personalizzati")

        if not all([ente_id, data_inizio, data_fine]):
            return self.write_json({"error": "ente_id, data_inizio e data_fine sono obbligatori"}, 400)
        if data_inizio > data_fine:
            return self.write_json({"error": "La data di inizio deve essere precedente alla data di fine"}, 400)

        success = await db_interface.update_assignment(
            int(assignment_id), int(ente_id), data_inizio, data_fine, note,
            orari_personalizzati=orari_pers
        )
        if success:
            return self.write_json({"message": "Assegnazione aggiornata"})
        return self.write_json({"error": "Assegnazione non trovata"}, 404)

    async def delete(self, assignment_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)

        success = await db_interface.delete_assignment(int(assignment_id))
        if success:
            return self.write_json({"message": "Assegnazione eliminata"})
        return self.write_json({"error": "Assegnazione non trovata"}, 404)


class StudentStageInfoHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        assignment = await db_interface.get_assignment_by_user(int(user["id"]))
        if not assignment:
            return self.write_json({"assignment": None})

        from datetime import date
        today  = date.today().isoformat()
        inizio = assignment["data_inizio"]
        fine   = assignment["data_fine"]

        if today < inizio:
            phase = "pre"
        elif today > fine:
            phase = "post"
        else:
            phase = "durante"

        # Decodifica orari JSON se stringhe
        for field in ("orari_personalizzati", "ente_orari_lavoro"):
            if isinstance(assignment.get(field), str):
                import json as _json
                try:
                    assignment[field] = _json.loads(assignment[field])
                except Exception:
                    assignment[field] = None

        self.write_json({"assignment": assignment, "phase": phase, "today": today})


# ══════════════════════════════════════════════════════════════════════════
#  STUDENT PREFERENCES
# ══════════════════════════════════════════════════════════════════════════
class StudentPreferencesHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        prefs = await db_interface.get_preferences_by_user(int(user["id"]))
        self.write_json({"preferences": prefs})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if _is_staff(ruolo):
            return self.write_json({"error": "Solo gli studenti possono salvare preferenze"}, 403)
        assignment = await db_interface.get_assignment_by_user(int(user["id"]))
        if assignment:
            return self.write_json({"error": "Hai già un'assegnazione, non puoi modificare le preferenze"}, 400)
        body = tornado.escape.json_decode(self.request.body)
        ente_ids = [int(x) for x in body.get("ente_ids", []) if x][:3]
        if len(ente_ids) != len(set(ente_ids)):
            return self.write_json({"error": "Non puoi selezionare lo stesso ente più volte"}, 400)
        await db_interface.save_preferences(int(user["id"]), ente_ids)
        return self.write_json({"message": "Preferenze salvate"})


class AdminStudentPreferencesHandler(BaseHandler):
    async def get(self, user_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)
        ruolo = await db_interface.check_user(user["email"])
        if not _is_staff(ruolo):
            return self.write_json({"error": "Accesso negato"}, 403)
        prefs = await db_interface.get_preferences_by_user(int(user_id))
        self.write_json({"preferences": prefs})
