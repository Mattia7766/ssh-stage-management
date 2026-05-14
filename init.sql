-- Assicura che lo user 'student' abbia i permessi completi sul database
-- (il docker entrypoint crea già il DB e lo user, ma solo per 'student'@'%')
GRANT ALL PRIVILEGES ON `DB_SSH_todo_app2`.* TO 'student'@'%';
FLUSH PRIVILEGES;
