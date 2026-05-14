import asyncio
import tornado.web

from backend.db.db import COOKIE_SECRET, PORT, init_pool, db_interface
from backend.handlers.auth import RegisterHandler, LoginHandler, LogoutHandler
from backend.handlers.admin import (
    AdminUsersHandler,
    AdminUserResubmitHandler,
    AdminUserSurveyHandler,
    AdminSurveyResponsesHandler,
    AdminExportHandler,
    AdminImportHandler,
)
from backend.handlers.survey import SurveyHandler
from backend.handlers.enti import (
    EntiHandler,
    EnteDetailHandler,
    DisponibilitaHandler,
    AssignmentsHandler,
    AssignmentDetailHandler,
    StudentStageInfoHandler,
    StudentPreferencesHandler,
    AdminStudentPreferencesHandler,
)


def make_app():
    return tornado.web.Application(
        [
            # ── Auth ──────────────────────────────────────────────────────
            (r"/api/register",  RegisterHandler),
            (r"/api/login",     LoginHandler),
            (r"/api/logout",    LogoutHandler),

            # ── Admin / Prof: utenti ──────────────────────────────────────
            (r"/api/admin/users/(\d+)/allow-resubmit", AdminUserResubmitHandler),
            (r"/api/admin/users/(\d+)/survey",         AdminUserSurveyHandler),
            (r"/api/admin/users/(\d+)",                AdminUsersHandler),
            (r"/api/admin/users",                      AdminUsersHandler),

            # ── Admin / Prof: risposte questionario ───────────────────────
            (r"/api/admin/survey-responses/(\d+)", AdminSurveyResponsesHandler),
            (r"/api/admin/survey-responses",       AdminSurveyResponsesHandler),

            # ── Admin: export / import JSON ───────────────────────────────
            (r"/api/admin/export", AdminExportHandler),
            (r"/api/admin/import", AdminImportHandler),

            # ── Enti ──────────────────────────────────────────────────────
            (r"/api/enti/(\d+)/disponibilita", DisponibilitaHandler),
            (r"/api/enti/(\d+)",               EnteDetailHandler),
            (r"/api/enti",                     EntiHandler),

            # ── Assegnazioni ─────────────────────────────────────────────
            (r"/api/assignments/(\d+)", AssignmentDetailHandler),
            (r"/api/assignments",       AssignmentsHandler),

            # ── Stage info (studente) ─────────────────────────────────────
            (r"/api/my-stage", StudentStageInfoHandler),

            # ── Preferenze enti (studente) ────────────────────────────────
            (r"/api/my-preferences", StudentPreferencesHandler),

            # ── Preferenze studente (admin/prof) ──────────────────────────
            (r"/api/admin/users/(\d+)/preferences", AdminStudentPreferencesHandler),

            # ── Survey utente ─────────────────────────────────────────────
            (r"/api/survey", SurveyHandler),

            # ── File statici ──────────────────────────────────────────────
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
            (r"/",            tornado.web.RedirectHandler,   {"url": "/static/login.html"}),
        ],
        cookie_secret=COOKIE_SECRET,
        autoreload=True,
        debug=True,
    )


async def main():
    await init_pool()
    await db_interface._ensure_tables()
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")
