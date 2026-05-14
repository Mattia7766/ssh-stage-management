import tornado.escape
from datetime import date
from backend.handlers.base import BaseHandler
from backend.db.db import db_interface


class SurveyHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        uid = int(user["id"])
        count = await db_interface.get_survey_submission_count(uid)
        resubmit_allowed = await db_interface.get_resubmit_allowed(uid)

        # Controlla la fase dello stage
        assignment = await db_interface.get_assignment_by_user(uid)
        phase = None
        if assignment:
            today = date.today().isoformat()
            if today < assignment["data_inizio"]:
                phase = "pre"
            elif today > assignment["data_fine"]:
                phase = "post"
            else:
                phase = "durante"

        self.write_json({
            "already_submitted": count > 0,
            "submission_count": count,
            "resubmit_allowed": resubmit_allowed,
            "assignment": assignment,
            "phase": phase,
        })

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        uid = int(user["id"])

        assignment = await db_interface.get_assignment_by_user(uid)
        if not assignment:
            return self.write_json({
                "error": "Non hai ancora un'assegnazione. Il questionario sarà disponibile al termine del tuo stage."
            }, 403)
        if assignment:
            today = date.today().isoformat()
            if today < assignment["data_inizio"]:
                return self.write_json({
                    "error": "Il questionario sarà disponibile dopo la fine dello stage."
                }, 403)
            if assignment["data_inizio"] <= today <= assignment["data_fine"]:
                return self.write_json({
                    "error": "Il questionario sarà disponibile al termine dello stage."
                }, 403)

        count = await db_interface.get_survey_submission_count(uid)
        if count > 0:
            resubmit_allowed = await db_interface.get_resubmit_allowed(uid)
            if not resubmit_allowed:
                return self.write_json({
                    "error": "Hai già compilato il questionario. "
                             "Contatta l'amministratore per richiedere una nuova compilazione."
                }, 403)
            await db_interface.set_resubmit_allowed(uid, False)

        body = tornado.escape.json_decode(self.request.body)
        responses = body.get("responses", {})

        if not isinstance(responses, dict):
            return self.write_json({"error": "Formato risposte non valido"}, 400)

        await db_interface.save_survey_response(
            user_id=uid,
            email=user["email"],
            responses=responses
        )
        return self.write_json({"message": "Questionario inviato con successo"}, 201)
