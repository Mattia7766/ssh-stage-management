# 🎓 Sistema di Gestione Stage Studenteschi

Applicazione web per la gestione di stage/tirocini studenteschi sviluppata con Python/Tornado e MySQL.

## 🚀 Quick Start con Docker

### Prerequisiti
- Docker
- Docker Compose

### Installazione e Avvio

```bash
# 1. Clona il repository
git clone https://github.com/Mattia7766/ssh-stage-management.git
cd ssh-stage-management

# 2. Avvia i container Docker
docker-compose up -d --build

# 3. Accedi all'applicazione
# Apri il browser su: http://localhost:8888
```

## 📁 Struttura del Progetto

```
PyCharmMiscProject/
├── backend/
│   ├── db/              # Interfaccia database
│   │   ├── db.py        # Configurazione pool connessioni
│   │   └── db_interface.py
│   └── handlers/        # Request handlers
│       ├── auth.py      # Autenticazione
│       ├── admin.py     # Pannello admin
│       ├── enti.py      # Gestione enti
│       └── survey.py    # Questionari
├── static/              # Frontend
│   ├── js/              # JavaScript
│   ├── *.html           # Pagine HTML
│   └── style.css        # Stili
├── entrypoint.sh        # Script di avvio container
├── Dockerfile           # Immagine Docker app
├── docker-compose.yml   # Orchestrazione container
├── requirements.txt     # Dipendenze Python
├── Task_server.py       # Server principale
└── init.sql            # Inizializzazione database
```

## 🛠 Comandi Docker Utili

```bash
# Avviare i container
docker-compose up -d --build

# Fermare i container
docker-compose down

# Vedere i log in tempo reale
docker-compose logs -f app

# Vedere lo stato dei container
docker-compose ps

# Accedere al container dell'app
docker-compose exec app bash

# Accedere al database MySQL
docker-compose exec db mysql -u student -pPass DB_SSH_todo_app2

# Ricostruire dopo modifiche al codice
docker-compose up -d --build
```

## 📊 Funzionalità

- 👤 **Autenticazione utenti**: Admin, Professore, Studente
- 🏢 **Gestione enti/aziende** per stage
- 📋 **Assegnazione studenti** agli enti
- 📝 **Questionario di valutazione** stage
- 📊 **Dashboard e statistiche**
- 🔍 **Analisi ETS** (Educational Training System)

## 💻 Tecnologie

- **Backend**: Python 3.12, Tornado Web Framework
- **Database**: MySQL 8.0
- **ORM**: aiomysql (async)
- **Sicurezza**: bcrypt per hash password
- **Frontend**: JavaScript vanilla, HTML5, CSS3
- **Containerizzazione**: Docker, Docker Compose

## 🔧 Configurazione

### Database
Il database MySQL è accessibile su:
- **Dall'host**: `localhost:3307`
- **Dentro Docker**: `db:3306`

### Credenziali di default
- **Database**: `DB_SSH_todo_app2`
- **Username**: `student`
- **Password**: `Pass`

⚠️ **IMPORTANTE**: Cambia le password prima di usare in produzione!

## 🐛 Troubleshooting

### Porta 3306 già in uso
Il progetto usa la porta 3307 per evitare conflitti con MySQL locale.

### Errore "localhost" connection
Il container app usa uno script `entrypoint.sh` che mappa automaticamente `localhost` al container `db`.

### Container non si avvia
```bash
# Controlla i log
docker-compose logs app
docker-compose logs db

# Ricostruisci da zero
docker-compose down -v
docker-compose up -d --build
```

## 👨‍💻 Sviluppo Locale (senza Docker)

```bash
# Crea virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oppure
.venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Avvia il server (assicurati che MySQL sia in esecuzione)
python Task_server.py
```

## 📝 Variabili d'Ambiente

Il progetto supporta le seguenti variabili d'ambiente:

```bash
DB_HOST=db              # Host database
DB_PORT=3306            # Porta database
DB_USER=student         # Username database
DB_PASSWORD=Pass        # Password database
DB_NAME=DB_SSH_todo_app2  # Nome database
COOKIE_SECRET=your_secret  # Chiave per cookie sicuri
PORT=8888               # Porta applicazione
```

## 📧 Contatti

Progetto sviluppato da **Mattia Bottari** per l'Istituto Fermi - Modena

## 📄 Licenza

Progetto didattico - Istituto Fermi
