// static/js/app.js

const QUESTIONS = [
    { id: "dati_ets", label: "Dati dell'ETS", type: "text", required: true },
    { id: "dati_alunno", label: "Dati dell'alunn*", type: "text", required: true },
    { id: "percorso", label: "Se sei uno studente specifica il tuo percorso", type: "text", required: true },
    { id: "prima_esperienza", label: "È la prima esperienza di volontariato e cittadinanza?", type: "radio", options: ["Sì", "No"], required: true },
    { id: "fonte_info", label: "Dove o da chi hai ricevuto le informazioni?", type: "checkbox", options: [
        "Progetto Cantieri Giovani", "dalla scuola", "dall'informagiovani", "dai centri giovani",
        "dal CSV Terre Estensi", "materiale promozionale", "servizi sociali", "dalla mia famiglia", "da un amico"
    ], required: true },
    { id: "rispetto_impegni", label: "Credi di essere riuscit* a rispettare orari, appuntamenti, impegni e scadenze?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "motivazioni", label: "Quali sono le motivazioni personali che ti hanno spinto a fare questa esperienza?", type: "checkbox", options: [
        "Il confronto con i miei insegnanti", "gli stimoli degli amici", "gli stimoli della mia famiglia",
        "la curiosità di provare qualcosa di nuovo", "le mie convinzioni personali", "qualche cosa che mi è successo"
    ], required: true },
    { id: "ruolo_stage", label: "Che ruolo hai avuto durante lo stage?", type: "text", required: true },
    { id: "miglioramento_incarichi", label: "Ritieni di essere migliorat* nella tua capacità di portare a termine gli incarichi assegnati?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "lavoro_gruppo", label: "Quanto sei riuscit* a lavorare in gruppo?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "empatia", label: "Quanto sei riuscit* a comprendere gli stati d'animo e le emozioni altrui (empatia)?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "ascolto", label: "Quanto sei riuscit* ad ascoltare ed accettare i punti di vista diversi dai tuoi?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "comunicazione_efficace", label: "Sei riuscit* a comunicare in modo efficace?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "gestione_imprevisti", label: "Sei riuscit* ad affrontare e gestire gli imprevisti?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "chiedere_aiuto", label: "Sei riuscit* a chiedere aiuto quando non sapevi fare qualcosa?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "curiosita_motivazione", label: "Quanto questa esperienza ti ha incuriosit* e motivat*?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "competenze_utili", label: "Le tue competenze (relazionali, informatiche, linguistiche, ecc) ti sono state utili?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "altro_imparato", label: "Ci sono altre cose che hai imparato/sviluppato non elencate sopra che vuoi dirci?", type: "textarea", required: false },
    { id: "crescita_comunicazione", label: "Quanto è cresciuta la tua capacità di comunicare in modo efficace?", type: "likert", options: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "cosa_imparato", label: "Cosa pensi di aver imparato dall'esperienza di stage?", type: "checkbox", options: [
        "Problem solving", "empatia", "adattabilità", "autocontrollo", "lavoro di squadra/networking",
        "sicurezza in sé stessi", "spirito di collaborazione", "volontà di apprendere", "creatività e pensiero critico"
    ], required: true },
    { id: "contesto_spendere", label: "In quale contesto pensi che potresti spendere le competenze che hai sviluppato?", type: "checkbox", options: [
        "Nel mondo della scuola", "nel mondo del lavoro", "nell'attività di volontariato", "nel mio contesto di amici", "in famiglia"
    ], required: true },
    { id: "aspetti_interessanti", label: "Quanto reputi interessanti i seguenti aspetti dell'attività di volontariato?", type: "matrix", subquestions: [
        "Conoscere nuove persone/realtà al di fuori della scuola",
        "Impegnarsi in attività manuali",
        "Scoprire nuovi interessi",
        "Scoprire nuove capacità",
        "Svolgere attività di tuo interesse",
        "Lavorare in gruppo"
    ], scale: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true },
    { id: "soddisfazione_scolastica", label: "Quanto sei soddisfatto/a dei seguenti aspetti della tua vita scolastica e personale?", type: "matrix", subquestions: [
        "Quanto ti senti a tuo agio e felice in classe?",
        "Quanto pensi che le regole della scuola siano importanti e giuste?",
        "Quanto ti senti parte di un gruppo di amici e compagni di classe?",
        "Quanto sei soddisfatto dei tuoi voti?",
        "Quanto riesci a relazionarti con gli altri in classe e a lavorare in gruppo?",
        "Quanto pensi di conoscere i tuoi bisogni e desideri?",
        "Quanto ti senti supportato dalla tua famiglia?"
    ], scale: ["Moltissimo", "Molto", "Abbastanza", "Poco", "Per nulla"], required: true }
];

// ══════════════════════════════════════════════════════════════════════════
//  AUTH
// ══════════════════════════════════════════════════════════════════════════
async function login() {
    const email    = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const res  = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
        if (data.ruolo === "ADMIN") {
            location.href = "dashboard.html";
        } else if (data.ruolo === "PROFESSORE") {
            location.href = "dashboard_prof.html";
        } else {
            location.href = "survey.html";
        }
    } else {
        alert(data.error || "Errore login");
    }
}

async function logout() {
    await fetch("/api/logout", { method: "POST" });
    location.href = "login.html";
}

// ══════════════════════════════════════════════════════════════════════════
//  SURVEY  (studente)
// ══════════════════════════════════════════════════════════════════════════
async function loadSurvey() {
    const res = await fetch("/api/survey");
    if (res.status === 401) { location.href = "login.html"; return; }
    const data = await res.json();

    const activeArea  = document.getElementById("surveyActiveArea");
    const blockedArea = document.getElementById("surveyBlockedArea");
    const stageArea   = document.getElementById("surveyStageArea");
    const submitBtn   = document.getElementById("submitSurvey");

    // ── Funzione helper per mostrare solo una area ─────────────────────
    function showOnly(area) {
        [activeArea, blockedArea, stageArea].forEach(a => { if (a) a.style.display = "none"; });
        if (area) area.style.display = "";
    }

    const { assignment, phase } = data;

    // ── Helper: formatta orari lavorativi in HTML leggibile ──────────────
    function formatOrari(orari) {
        if (!orari || typeof orari !== "object") return "";
        const nomi = { lunedi:"Lunedi", martedi:"Martedi", mercoledi:"Mercoledi",
                       giovedi:"Giovedi", venerdi:"Venerdi", sabato:"Sabato", domenica:"Domenica" };
        const righe = Object.entries(nomi)
            .filter(([k]) => orari[k] && orari[k].attivo)
            .map(([k]) => `<tr>
                <td style="padding:0.15rem 0.9rem 0.15rem 0;font-weight:600;color:#374151;">${nomi[k]}</td>
                <td style="color:#1e40af;">${orari[k].inizio} &ndash; ${orari[k].fine}</td>
            </tr>`).join("");
        if (!righe) return "";
        return `<div style="margin-top:0.75rem;background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:0.75rem 1rem;">
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#1d4ed8;margin-bottom:0.5rem;">
                Orari di lavoro
            </div>
            <table style="font-size:0.88rem;border-collapse:collapse;width:100%;">${righe}</table>
        </div>`;
    }

    // 1. Studente con assegnazione — logica fase stage
    if (assignment) {
        const fmt = d => new Date(d).toLocaleDateString("it-IT", {day:"2-digit", month:"long", year:"numeric"});
        // Usa orari personalizzati se presenti, altrimenti quelli dell'ente
        const orariEffettivi = assignment.orari_personalizzati || assignment.ente_orari_lavoro;
        const orariHtml = formatOrari(orariEffettivi);

        if (phase === "pre") {
            showOnly(stageArea);
            document.getElementById("stageStatusTitle").textContent = "Il tuo stage iniziera presto";
            document.getElementById("stageStatusIcon").textContent  = "📅";
            document.getElementById("stageStatusBody").innerHTML = `
                <p>Sei stato assegnato all'ente <strong>${escapeHtml(assignment.ente_nome)}</strong>.</p>
                <p>Il tuo stage iniziera il <strong>${fmt(assignment.data_inizio)}</strong> e terminera il <strong>${fmt(assignment.data_fine)}</strong>.</p>
                ${assignment.ente_indirizzo ? `<p>📍 Indirizzo: <strong>${escapeHtml(assignment.ente_indirizzo)}</strong></p>` : ""}
                ${assignment.ente_referente ? `<p>👤 Referente: <strong>${escapeHtml(assignment.ente_referente)}</strong></p>` : ""}
                ${assignment.note ? `<p>📝 Note: ${escapeHtml(assignment.note)}</p>` : ""}
                ${orariHtml}
                <div class="info-note" style="margin-top:0.75rem;">📋 Il questionario sara disponibile al termine dello stage.</div>`;
            return;
        }

        if (phase === "durante") {
            showOnly(stageArea);
            document.getElementById("stageStatusTitle").textContent = "Stage in corso";
            document.getElementById("stageStatusIcon").textContent  = "🏢";
            document.getElementById("stageStatusBody").innerHTML = `
                <p>Sei attualmente in stage presso <strong>${escapeHtml(assignment.ente_nome)}</strong>.</p>
                <p>Il tuo stage e iniziato il <strong>${fmt(assignment.data_inizio)}</strong> e terminera il <strong>${fmt(assignment.data_fine)}</strong>.</p>
                ${assignment.ente_indirizzo ? `<p>📍 Indirizzo: <strong>${escapeHtml(assignment.ente_indirizzo)}</strong></p>` : ""}
                ${assignment.ente_referente ? `<p>👤 Referente: <strong>${escapeHtml(assignment.ente_referente)}</strong></p>` : ""}
                ${assignment.note ? `<p>📝 Note: ${escapeHtml(assignment.note)}</p>` : ""}
                ${orariHtml}
                <div class="info-note" style="margin-top:0.75rem;">📋 Il questionario sara disponibile al termine dello stage (${fmt(assignment.data_fine)}).</div>`;
            return;
        }
        // phase === "post" → cade nel flusso normale sotto
    }

    // 2. Questionario già compilato senza autorizzazione
    if (data.already_submitted && !data.resubmit_allowed) {
        showOnly(blockedArea);
        const histBox = document.getElementById("submissionHistoryBox");
        if (histBox) histBox.innerHTML = `<p>Hai compilato il questionario <strong>${data.submission_count}</strong> volta/e.</p>`;
        return;
    }

    // 3. Autorizzato a ricompilare
    if (data.already_submitted && data.resubmit_allowed) {
        insertBanner(
            "info-banner info-banner--authorized",
            `✅ L'amministratore ti ha autorizzato a compilare nuovamente il questionario (compilazione #${data.submission_count + 1}). Le risposte precedenti verranno conservate.`
        );
    }

    // 4. Prima compilazione o autorizzato → mostra il form
    showOnly(activeArea);
    renderSurveyForm();
}

function insertBanner(className, html) {
    const banner = document.createElement("div");
    banner.className = className;
    banner.innerHTML = html;
    const form = document.getElementById("surveyForm");
    form.parentNode.insertBefore(banner, form);
}

function renderSurveyForm() {
    const form = document.getElementById("surveyForm");
    form.innerHTML = "";
    QUESTIONS.forEach((q, index) => {
        const div = document.createElement("div");
        div.className = "question-card";
        div.innerHTML = `<label>${index + 1}. ${q.label} ${q.required ? '<span style="color:red;">*</span>' : ''}</label>`;

        if (q.type === "text") {
            const input = document.createElement("input");
            input.type = "text"; input.name = q.id; input.className = "form-control";
            input.placeholder = "Scrivi qui...";
            if (q.required) input.required = true;
            div.appendChild(input);
        } else if (q.type === "textarea") {
            const ta = document.createElement("textarea");
            ta.name = q.id; ta.className = "form-control"; ta.rows = 3;
            ta.placeholder = "Scrivi qui...";
            if (q.required) ta.required = true;
            div.appendChild(ta);
        } else if (q.type === "radio" || q.type === "likert") {
            const og = document.createElement("div"); og.className = "options-group";
            q.options.forEach(opt => {
                const lbl = document.createElement("label");
                const r = document.createElement("input");
                r.type = "radio"; r.name = q.id; r.value = opt;
                if (q.required) r.required = true;
                lbl.appendChild(r); lbl.appendChild(document.createTextNode(" " + opt));
                og.appendChild(lbl);
            });
            div.appendChild(og);
        } else if (q.type === "checkbox") {
            const og = document.createElement("div"); og.className = "options-group";
            q.options.forEach(opt => {
                const lbl = document.createElement("label");
                const cb = document.createElement("input");
                cb.type = "checkbox"; cb.name = q.id; cb.value = opt;
                if (q.required) cb.classList.add("required-checkbox-group");
                lbl.appendChild(cb); lbl.appendChild(document.createTextNode(" " + opt));
                og.appendChild(lbl);
            });
            div.appendChild(og);
        } else if (q.type === "matrix") {
            const table = document.createElement("table");
            table.className = "matrix-table";
            let header = "<tr><th></th>";
            q.scale.forEach(s => header += `<th>${s}</th>`);
            table.innerHTML = header + "</tr>";
            q.subquestions.forEach((sq, i) => {
                let row = `<tr><td>${sq}</td>`;
                q.scale.forEach(s => row += `<td><input type="radio" name="${q.id}_${i}" value="${s}" ${q.required ? 'required' : ''}></td>`);
                table.innerHTML += row + "</tr>";
            });
            div.appendChild(table);
        }
        form.appendChild(div);
    });
}

async function submitSurvey() {
    let isValid = true, firstError = null;
    QUESTIONS.forEach(q => {
        if (!q.required) return;
        if (q.type === "checkbox") {
            if (!document.querySelector(`input[name="${q.id}"]:checked`)) {
                isValid = false; if (!firstError) firstError = q.label;
            }
        } else if (q.type === "matrix") {
            q.subquestions.forEach((_, i) => {
                if (!document.querySelector(`input[name="${q.id}_${i}"]:checked`)) {
                    isValid = false; if (!firstError) firstError = q.label;
                }
            });
        }
    });

    const form = document.getElementById("surveyForm");
    if (!form.checkValidity() || !isValid) {
        alert(`Compila tutti i campi obbligatori.${firstError ? ' Manca: ' + firstError : ''}`);
        return;
    }

    const formData = new FormData(form);
    const responses = {};
    QUESTIONS.forEach(q => {
        if (q.type === "matrix") {
            q.subquestions.forEach((_, i) => {
                const v = formData.get(`${q.id}_${i}`);
                if (v) responses[`${q.id}_${i}`] = v;
            });
        } else if (q.type === "checkbox") {
            responses[q.id] = formData.getAll(q.id);
        } else {
            responses[q.id] = formData.get(q.id) || "";
        }
    });

    const res = await fetch("/api/survey", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ responses })
    });
    const data = await res.json();
    const msgDiv = document.getElementById("surveyMessage");
    if (res.ok) {
        msgDiv.innerHTML = '<div class="success">✅ Questionario inviato con successo! Grazie per la partecipazione.</div>';
        document.getElementById("submitSurvey").disabled = true;
        setTimeout(() => location.reload(), 2000);
    } else {
        msgDiv.innerHTML = `<div class="error">❌ ${data.error}</div>`;
    }
}

// ══════════════════════════════════════════════════════════════════════════
//  ADMIN DASHBOARD
// ══════════════════════════════════════════════════════════════════════════
let currentSection = 'dashboard';
let allResponses = [];
let allUsers = [];
let allUsersResponseCounts = {};

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId + 'Section').classList.add('active');
    currentSection = sectionId;
    if (sectionId === 'dashboard')       loadDashboardStats();
    else if (sectionId === 'createUser') loadUsersList();
    else if (sectionId === 'responses')  loadSurveyResponses();
    // importExport needs no initial load
}

async function loadDashboardStats() {
    try {
        const [usersRes, responsesRes] = await Promise.all([
            fetch("/api/admin/users"),
            fetch("/api/admin/survey-responses")
        ]);
        if (!usersRes.ok || !responsesRes.ok) { location.href = "login.html"; return; }
        const users     = await usersRes.json();
        const responses = await responsesRes.json();

        document.getElementById("userCount").innerHTML = `
            <div class="stat-icon"><i class="fa fa-users"></i></div>
            <h3>${users.users.length}</h3>
            <p>Utenti registrati</p>`;

        document.getElementById("responseCount").innerHTML = `
            <div class="stat-icon"><i class="fa fa-clipboard-check"></i></div>
            <h3>${responses.responses.length}</h3>
            <p>Questionari inviati</p>`;
    } catch(e) { console.error(e); }
}

async function createUser() {
    const email    = document.getElementById("newEmail").value.trim();
    const password = document.getElementById("newPassword").value;
    const ruolo    = document.getElementById("newRole").value;
    const res  = await fetch("/api/admin/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password, ruolo })
    });
    const data = await res.json();
    const msg  = document.getElementById("createUserMessage");
    if (res.ok) {
        msg.innerHTML = `<div class="success">✅ ${data.message}</div>`;
        loadUsersList();
        document.getElementById("newEmail").value    = "";
        document.getElementById("newPassword").value = "";
        // Se è uno studente, apri il modal PCTO
        if (ruolo === "USER") {
            openPctoModal(data.user_id, data.email);
        }
    } else {
        msg.innerHTML = `<div class="error">❌ ${data.error}</div>`;
    }
}

// ── PCTO MODAL ────────────────────────────────────────────────────────────────
let _pctoUserId    = null;
let _pctoUserEmail = null;
let _pctoEnti      = [];      // enti caricati con posti_disponibili e orari_lavoro
let _pctoForce     = false;   // override disponibilita piena

// Giorni della settimana per orari
const _GIORNI = [
    { key: "lunedi",    label: "Lunedi"    },
    { key: "martedi",   label: "Martedi"   },
    { key: "mercoledi", label: "Mercoledi" },
    { key: "giovedi",   label: "Giovedi"   },
    { key: "venerdi",   label: "Venerdi"   },
    { key: "sabato",    label: "Sabato"    },
    { key: "domenica",  label: "Domenica"  },
];

function _buildOrariGrid(containerId, prefix, defaults) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = "";
    _GIORNI.forEach(g => {
        const def    = defaults && defaults[g.key];
        const attivo = def ? def.attivo : (g.key !== "sabato" && g.key !== "domenica");
        const inizio = def ? (def.inizio || "09:00") : "09:00";
        const fine   = def ? (def.fine   || "17:00") : "17:00";
        const row    = document.createElement("div");
        row.style.cssText = "display:grid;grid-template-columns:auto 90px 1fr auto auto;gap:0.4rem;align-items:center;margin-bottom:0.35rem;";
        row.innerHTML = `
            <input type="checkbox" id="${prefix}_${g.key}_attivo" ${attivo ? "checked" : ""}
                   onchange="_toggleGiorno('${prefix}','${g.key}')" style="width:15px;height:15px;cursor:pointer;">
            <label for="${prefix}_${g.key}_attivo" style="font-size:0.83rem;font-weight:600;">${g.label}</label>
            <input type="time" id="${prefix}_${g.key}_inizio" value="${inizio}" ${!attivo ? "disabled" : ""}
                   style="padding:0.3rem 0.5rem;border:1px solid #cbd5e1;border-radius:6px;font-size:0.83rem;margin-bottom:0;width:auto;background:${!attivo ? '#f1f5f9' : 'white'};">
            <span style="font-size:0.75rem;color:#94a3b8;">&#8594;</span>
            <input type="time" id="${prefix}_${g.key}_fine" value="${fine}" ${!attivo ? "disabled" : ""}
                   style="padding:0.3rem 0.5rem;border:1px solid #cbd5e1;border-radius:6px;font-size:0.83rem;margin-bottom:0;width:auto;background:${!attivo ? '#f1f5f9' : 'white'};">`;
        container.appendChild(row);
    });
}

function _toggleGiorno(prefix, key) {
    const cb     = document.getElementById(`${prefix}_${key}_attivo`);
    const inizio = document.getElementById(`${prefix}_${key}_inizio`);
    const fine   = document.getElementById(`${prefix}_${key}_fine`);
    if (!cb) return;
    [inizio, fine].forEach(el => {
        if (!el) return;
        el.disabled = !cb.checked;
        el.style.background = cb.checked ? "white" : "#f1f5f9";
    });
}

function _readOrariGrid(prefix) {
    const result = {};
    _GIORNI.forEach(g => {
        const cb = document.getElementById(`${prefix}_${g.key}_attivo`);
        if (!cb) return;
        result[g.key] = {
            attivo: cb.checked,
            inizio: (document.getElementById(`${prefix}_${g.key}_inizio`) || {}).value || "09:00",
            fine:   (document.getElementById(`${prefix}_${g.key}_fine`)   || {}).value || "17:00",
        };
    });
    return Object.values(result).some(v => v.attivo) ? result : null;
}

async function pctoCheckDisponibilita() {
    const enteId = parseInt(document.getElementById("pctoEnteSelect").value);
    const inizio = document.getElementById("pctoDataInizio").value;
    const fine   = document.getElementById("pctoDataFine").value;
    const box    = document.getElementById("pctoDispBox");
    if (!box) return;

    if (!enteId || !inizio || !fine) { box.innerHTML = ""; return; }
    if (inizio > fine) {
        box.innerHTML = `<div style="padding:0.5rem 0.9rem;border-radius:8px;font-size:0.84rem;background:#fef3c7;color:#92400e;border:1px solid #fcd34d;">
            La data di fine deve essere successiva alla data di inizio.</div>`;
        return;
    }

    const ente = _pctoEnti.find(e => e.id === enteId);
    if (!ente || ente.posti_disponibili == null) {
        box.innerHTML = `<div style="padding:0.5rem 0.9rem;border-radius:8px;font-size:0.84rem;background:#f1f5f9;color:#64748b;border:1px solid #e2e8f0;">
            Nessun limite di posti configurato per questa azienda.</div>`;
        return;
    }

    box.innerHTML = `<div style="padding:0.5rem 0.9rem;border-radius:8px;font-size:0.84rem;background:#f1f5f9;color:#64748b;">Verifica disponibilita...</div>`;

    const res  = await fetch(`/api/enti/${enteId}/disponibilita?data_inizio=${inizio}&data_fine=${fine}`);
    const data = await res.json();
    if (!res.ok) { box.innerHTML = ""; return; }

    const { posti_totali, posti_occupati, posti_liberi, disponibile, occupato_fino_a } = data;
    _pctoForce = false;

    if (disponibile) {
        const warn = posti_liberi <= Math.max(1, Math.floor(posti_totali * 0.2));
        box.innerHTML = `<div style="padding:0.6rem 0.9rem;border-radius:8px;font-size:0.85rem;font-weight:600;
            background:${warn ? '#fef3c7' : '#d1fae5'};color:${warn ? '#92400e' : '#065f46'};
            border:1px solid ${warn ? '#fcd34d' : '#6ee7b7'};">
            ${warn ? 'Attenzione:' : ''} <strong>${posti_liberi}</strong> posto/i libero/i su ${posti_totali}
            nel periodo selezionato.
        </div>`;
    } else {
        const finoA = occupato_fino_a
            ? ` L'ente torna disponibile dal <strong>${new Date(occupato_fino_a).toLocaleDateString("it-IT",{day:"2-digit",month:"long",year:"numeric"})}</strong>.`
            : "";
        box.innerHTML = `<div style="padding:0.6rem 0.9rem;border-radius:8px;font-size:0.85rem;font-weight:600;
            background:#fee2e2;color:#991b1b;border:1px solid #fca5a5;">
            Tutti i ${posti_totali} posti sono occupati nel periodo selezionato.${finoA}
            <div style="margin-top:0.5rem;">
                <button onclick="pctoForceProceed()" style="width:auto;padding:0.4rem 1rem;
                    background:#dc2626;color:white;border:none;border-radius:6px;cursor:pointer;font-weight:600;font-size:0.82rem;">
                    Continua comunque
                </button>
            </div>
        </div>`;
    }
}

function pctoForceProceed() {
    _pctoForce = true;
    const box = document.getElementById("pctoDispBox");
    if (box) box.innerHTML = `<div style="padding:0.6rem 0.9rem;border-radius:8px;font-size:0.85rem;font-weight:600;
        background:#fef3c7;color:#92400e;border:1px solid #fcd34d;">
        Procederai anche se l'ente e al completo.
    </div>`;
}

function pctoToggleOrari() {
    const cb  = document.getElementById("pctoOrariToggle");
    const sec = document.getElementById("pctoOrariSection");
    if (!sec) return;
    sec.style.display = cb.checked ? "" : "none";
    if (cb.checked) {
        const enteId = parseInt(document.getElementById("pctoEnteSelect").value);
        const ente   = _pctoEnti.find(e => e.id === enteId);
        _buildOrariGrid("pctoOrariGrid", "pctoOr", ente?.orari_lavoro || null);
    }
}

async function openPctoModal(userId, email) {
    _pctoUserId    = userId;
    _pctoUserEmail = email;
    _pctoForce     = false;

    const overlay = document.getElementById("pctoModalOverlay");
    if (!overlay) return;

    document.getElementById("pctoModalSubtitle").textContent =
        `Studente: ${email}  —  Assegna ora il PCTO oppure fallo in seguito dalla sezione Enti & Stage.`;
    document.getElementById("pctoModalMessage").innerHTML = "";
    document.getElementById("pctoDataInizio").value = "";
    document.getElementById("pctoDataFine").value   = "";
    const dispBox = document.getElementById("pctoDispBox");
    if (dispBox) dispBox.innerHTML = "";
    const tog = document.getElementById("pctoOrariToggle");
    if (tog) { tog.checked = false; }
    const sec = document.getElementById("pctoOrariSection");
    if (sec) sec.style.display = "none";

    // Carica enti e preferenze in parallelo
    const sel      = document.getElementById("pctoEnteSelect");
    const prefsBox = document.getElementById("pctoPrefsBox");
    sel.innerHTML = '<option value="">Caricamento...</option>';
    if (prefsBox) { prefsBox.innerHTML = ""; prefsBox.style.display = "none"; }

    try {
        const [entiRes, prefRes] = await Promise.all([
            fetch("/api/enti"),
            fetch(`/api/admin/users/${userId}/preferences`)
        ]);
        const d = await entiRes.json();
        _pctoEnti = d.enti || [];
        if (_pctoEnti.length === 0) {
            sel.innerHTML = '<option value="">Nessun ente disponibile — aggiungine uno prima</option>';
        } else {
            sel.innerHTML = '<option value="">Seleziona azienda / ente...</option>' +
                _pctoEnti.map(e => `<option value="${e.id}">${escapeHtml(e.nome)}</option>`).join("");
        }

        // Mostra preferenze studente
        if (prefsBox && prefRes.ok) {
            const pd    = await prefRes.json();
            const prefs = pd.preferences || [];
            if (prefs.length > 0) {
                const ordLabels = ["1ª", "2ª", "3ª"];
                prefsBox.innerHTML =
                    '<p style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#166534;margin-bottom:0.5rem;">Preferenze espresse dallo studente</p>' +
                    prefs.map(p => `
                        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">
                            <span style="background:#16a34a;color:white;border-radius:50%;width:20px;height:20px;min-width:20px;display:inline-flex;align-items:center;justify-content:center;font-size:0.68rem;font-weight:800;">${p.ordine}</span>
                            <span style="font-size:0.85rem;font-weight:600;color:#14532d;flex:1;">${escapeHtml(p.ente_nome)}</span>
                            <button onclick="document.getElementById('pctoEnteSelect').value='${p.ente_id}';pctoCheckDisponibilita();"
                                style="font-size:0.72rem;padding:0.18rem 0.6rem;background:transparent;border:1px solid #16a34a;color:#16a34a;border-radius:5px;cursor:pointer;width:auto;box-shadow:none;font-weight:700;font-family:inherit;">
                                Usa
                            </button>
                        </div>`).join("");
                prefsBox.style.display = "block";
            }
        }
    } catch {
        sel.innerHTML = '<option value="">Errore caricamento enti</option>';
    }

    overlay.style.display = "flex";
}

function closePctoModal() {
    const overlay = document.getElementById("pctoModalOverlay");
    if (overlay) overlay.style.display = "none";
    const prefsBox = document.getElementById("pctoPrefsBox");
    if (prefsBox) { prefsBox.innerHTML = ""; prefsBox.style.display = "none"; }
    _pctoUserId    = null;
    _pctoUserEmail = null;
    _pctoForce     = false;
}

async function assignPcto() {
    const enteId     = document.getElementById("pctoEnteSelect").value;
    const dataInizio = document.getElementById("pctoDataInizio").value;
    const dataFine   = document.getElementById("pctoDataFine").value;
    const msg        = document.getElementById("pctoModalMessage");

    if (!enteId || !dataInizio || !dataFine) {
        msg.innerHTML = '<div class="error">Seleziona l\'ente e inserisci entrambe le date.</div>';
        return;
    }
    if (dataFine < dataInizio) {
        msg.innerHTML = '<div class="error">La data di fine non puo essere precedente all\'inizio.</div>';
        return;
    }

    // Blocca se posti esauriti (a meno di forceCreate)
    const ente = _pctoEnti.find(e => e.id === parseInt(enteId));
    if (ente && ente.posti_disponibili != null && !_pctoForce) {
        const dr   = await fetch(`/api/enti/${enteId}/disponibilita?data_inizio=${dataInizio}&data_fine=${dataFine}`);
        const dd   = await dr.json();
        if (!dd.disponibile) {
            msg.innerHTML = '<div class="error">Ente al completo. Clicca "Continua comunque" per procedere ugualmente.</div>';
            return;
        }
    }

    const orariCb   = document.getElementById("pctoOrariToggle");
    const orariPers = orariCb && orariCb.checked ? _readOrariGrid("pctoOr") : null;

    msg.innerHTML = '<em style="color:var(--gray-400);">Salvataggio...</em>';
    const res  = await fetch("/api/assignments", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id:              _pctoUserId,
            ente_id:              parseInt(enteId),
            data_inizio:          dataInizio,
            data_fine:            dataFine,
            note:                 "",
            orari_personalizzati: orariPers,
        }),
    });
    const data = await res.json();
    if (res.ok) {
        msg.innerHTML = '<div class="success">PCTO assegnato con successo!</div>';
        setTimeout(closePctoModal, 1200);
    } else {
        msg.innerHTML = `<div class="error">${data.error || "Errore durante l'assegnazione"}</div>`;
    }
}

async function deleteUser(userId) {
    if (!confirm("Sei sicuro di voler eliminare questo utente? Le sue risposte verranno cancellate.")) return;
    const res  = await fetch(`/api/admin/users/${userId}`, { method: "DELETE" });
    const data = await res.json();
    if (res.ok) loadUsersList();
    else alert(data.error);
}

async function loadUsersList() {
    const [usersRes, responsesRes] = await Promise.all([
        fetch("/api/admin/users"),
        fetch("/api/admin/survey-responses")
    ]);
    const usersData     = await usersRes.json();
    const responsesData = await responsesRes.json();

    allUsersResponseCounts = {};
    responsesData.responses.forEach(r => {
        allUsersResponseCounts[r.user_id] = (allUsersResponseCounts[r.user_id] || 0) + 1;
    });

    allUsers = usersData.users;
    renderUsersList(allUsers);
}

function filterUsers() {
    const emailF = (document.getElementById("searchEmail").value || "").toLowerCase();
    const roleF  = document.getElementById("searchRole").value;
    renderUsersList(allUsers.filter(u =>
        u.email.toLowerCase().includes(emailF) && (!roleF || u.ruolo === roleF)
    ));
}

function clearUserSearch() {
    document.getElementById("searchEmail").value = "";
    document.getElementById("searchRole").value  = "";
    renderUsersList(allUsers);
}

function renderUsersList(users) {
    const tbody = document.querySelector("#usersTable tbody");
    if (users.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--gray-600);padding:2rem;">Nessun utente trovato.</td></tr>`;
        return;
    }
    tbody.innerHTML = "";
    users.forEach(u => {
        const count        = allUsersResponseCounts[u.id] || 0;
        const hasSubmitted = count > 0;
        const isAuthorized = Boolean(u.resubmit_allowed);

        let surveyCell = "";
        if (!hasSubmitted) {
            surveyCell = `<span class="badge badge--gray">📭 Nessuna</span>`;
        } else if (isAuthorized) {
            surveyCell = `
                <span class="badge badge--authorized">✅ Autorizzato a ricompilare</span>
                <button class="btn-icon" onclick="viewUserSurveys(${u.id},'${escapeHtml(u.email)}')" title="Vedi risposte" style="margin-left:0.4rem;">📄</button>
                <button class="btn-revoke" onclick="revokeResubmit(${u.id})" title="Revoca autorizzazione" style="margin-left:0.4rem;">🔒</button>`;
        } else {
            surveyCell = `
                <span class="badge badge--submitted">✅ ${count} risposta/e</span>
                <button class="btn-icon" onclick="viewUserSurveys(${u.id},'${escapeHtml(u.email)}')" title="Vedi risposte" style="margin-left:0.4rem;">📄</button>
                <button class="btn-authorize" onclick="authorizeResubmit(${u.id})" title="Autorizza nuova compilazione" style="margin-left:0.4rem;">🔓 Autorizza</button>`;
        }

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.id}</td>
            <td>${escapeHtml(u.email)}</td>
            <td><span class="response-badge" style="background:${u.ruolo === 'ADMIN' ? 'var(--accent)' : u.ruolo === 'PROFESSORE' ? 'var(--warning)' : 'var(--primary)'};">${u.ruolo}</span></td>
            <td>${surveyCell}</td>
            <td><button class="btn-delete" onclick="deleteUser(${u.id})" style="width:auto;padding:0.4rem 0.8rem;">🗑️ Elimina</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function authorizeResubmit(userId) {
    if (!confirm("Autorizzare questo utente a compilare nuovamente il questionario?")) return;
    const res  = await fetch(`/api/admin/users/${userId}/allow-resubmit`, { method: "POST" });
    const data = await res.json();
    if (res.ok) loadUsersList();
    else alert(data.error);
}

async function revokeResubmit(userId) {
    if (!confirm("Revocare l'autorizzazione alla ri-compilazione?")) return;
    const res  = await fetch(`/api/admin/users/${userId}/allow-resubmit`, { method: "DELETE" });
    const data = await res.json();
    if (res.ok) loadUsersList();
    else alert(data.error);
}

async function viewUserSurveys(userId, email) {
    const res = await fetch(`/api/admin/users/${userId}/survey`);
    if (!res.ok) { alert("Errore nel caricamento delle risposte."); return; }
    const data = await res.json();

    let responsesHtml = "";
    data.responses.forEach((r, i) => {
        const date_fmt = new Date(r.submitted_at).toLocaleString('it-IT', {
            day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
        });
        responsesHtml += `
            <div class="user-survey-entry">
                <div class="user-survey-entry-header">
                    <strong>Risposta #${i + 1} — ${date_fmt}</strong>
                    <button class="btn-delete" style="width:auto;padding:0.3rem 0.75rem;font-size:0.85rem;"
                            onclick="deleteSurveyResponseFromModal(${r.id},this)">🗑️ Elimina</button>
                </div>
                <div class="response-detail-grid">${formatResponseDetails(r.responses)}</div>
            </div>`;
    });

    if (!data.responses.length) { alert("Nessuna risposta trovata per questo utente."); return; }

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal" onclick="this.closest('.modal').remove()">&times;</span>
            <h3>Risposte di ${escapeHtml(email)}</h3>
            ${responsesHtml}
        </div>`;
    document.body.appendChild(modal);
    modal.addEventListener('click', e => { if (e.target === modal) modal.remove(); });
}

function filterResponses() {
    const fs = (document.getElementById("filterStudente").value || "").toLowerCase();
    const fe = (document.getElementById("filterETS").value || "").toLowerCase();
    renderResponsesTable(allResponses.filter(r => {
        const stud   = r.responses?.__studente__;
        const nomeV  = stud
            ? (`${stud.nome || ''} ${stud.cognome || ''}`.trim() || r.responses?.dati_alunno || r.email || "")
            : (r.responses?.dati_alunno || r.email || "");
        const etsV   = r.responses?.dati_ets || stud?.azienda || "";
        return nomeV.toLowerCase().includes(fs) && etsV.toLowerCase().includes(fe);
    }));
}

function clearFilters() {
    document.getElementById("filterStudente").value = "";
    document.getElementById("filterETS").value      = "";
    renderResponsesTable(allResponses);
}

// UTILITY
function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
        .replace(/&/g,"&amp;").replace(/</g,"&lt;")
        .replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function setupDropdown() {
    const btn  = document.getElementById('menuToggle');
    const menu = document.getElementById('dropdownMenu');
    if (!btn || !menu) return;
    btn.addEventListener('click', e => { e.stopPropagation(); menu.classList.toggle('show'); });
    document.addEventListener('click', e => {
        if (!btn.contains(e.target) && !menu.contains(e.target)) menu.classList.remove('show');
    });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('show')));
}


// ═══════════════════════════════════════════════════════
//  ADMIN: SURVEY RESPONSES
// ═══════════════════════════════════════════════════════
async function loadSurveyResponses() {
    const res = await fetch("/api/admin/survey-responses");
    if (!res.ok) { location.href = "login.html"; return; }
    const data = await res.json();
    allResponses = data.responses || [];
    renderResponsesTable(allResponses);
}

function renderResponsesTable(responses) {
    const table   = document.getElementById("responsesTable");
    const tbody   = document.getElementById("responsesTableBody");
    const noMsg   = document.getElementById("noResultsMessage");
    if (!table || !tbody) return;
    if (responses.length === 0) {
        table.style.display = "none";
        if (noMsg) noMsg.style.display = "block";
        return;
    }
    if (noMsg) noMsg.style.display = "none";
    table.style.display = "";
    tbody.innerHTML = "";
    responses.forEach(r => {
        const stud  = r.responses?.__studente__;
        const nome  = escapeHtml(
            stud ? (`${stud.nome || ''} ${stud.cognome || ''}`.trim() || r.responses?.dati_alunno || r.email || "—")
                 : (r.responses?.dati_alunno || r.email || "—")
        );
        const ets   = escapeHtml(r.responses?.dati_ets || stud?.azienda || "—");
        const data  = new Date(r.submitted_at).toLocaleString("it-IT", {
            day:"2-digit", month:"2-digit", year:"numeric", hour:"2-digit", minute:"2-digit"
        });
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td style="text-align:center;">
                <button onclick="toggleResponseDetail(this)" style="width:30px;height:30px;border-radius:50%;border:none;background:#475569;color:white;cursor:pointer;font-size:0.65rem;padding:0;box-shadow:none;font-weight:700;">&#9658;</button>
            </td>
            <td>${nome}</td>
            <td>${ets}</td>
            <td>${data}</td>
            <td>
                <button onclick="deleteSurveyResponse(${r.id}, this)" style="width:auto;padding:0.35rem 0.75rem;font-size:0.82rem;" class="btn-delete"><i class="fa fa-trash"></i> Elimina</button>
            </td>`;
        const detailTr = document.createElement("tr");
        detailTr.className = "response-detail-row";
        detailTr.style.display = "none";
        detailTr.innerHTML = `
            <td colspan="5" style="padding:0;">
                <div style="padding:1rem 1.5rem; background:var(--gray-50); border-top:1px solid var(--border);">
                    <div class="response-detail-grid">${formatResponseDetails(r.responses)}</div>
                </div>
            </td>`;
        tbody.appendChild(tr);
        tbody.appendChild(detailTr);
    });
}

function toggleResponseDetail(btn) {
    const tr       = btn.closest("tr");
    const detailTr = tr.nextElementSibling;
    if (!detailTr) return;
    const open = detailTr.style.display !== "none";
    detailTr.style.display = open ? "none" : "";
    btn.textContent = open ? "▶" : "▼";
}

const QUESTION_LABELS = {
    // Dati anagrafici (old format)
    dati_alunno:              "Studente",
    dati_ets:                 "Ente / Azienda",
    classe:                   "Classe",
    anno:                     "Anno scolastico",
    tutor_scolastico:         "Tutor scolastico",
    tutor_aziendale:          "Tutor aziendale",
    data_inizio:              "Data inizio",
    data_fine:                "Data fine",
    ore_svolte:               "Ore svolte",
    // Valutazioni generali
    valutazione_generale:     "Valutazione generale",
    consigliare:              "Consiglieresti questo stage?",
    proseguire:               "Vorresti proseguire?",
    punti_forza:              "Punti di forza",
    punti_debolezza:          "Punti di debolezza",
    commenti:                 "Commenti liberi",
    note:                     "Note",
    // Competenze (new format)
    competenze_tecniche:      "Competenze tecniche",
    competenze_relazionali:   "Competenze relazionali",
    autonomia:                "Autonomia",
    puntualita:               "Puntualità",
    rispetto_regole:          "Rispetto delle regole",
    motivazione:              "Motivazione",
    problem_solving:          "Problem solving",
    comunicazione:            "Comunicazione",
    lavoro_squadra:           "Lavoro di squadra",
    // Ambiente
    ambiente_lavoro:          "Ambiente di lavoro",
    accoglienza:              "Accoglienza",
    supporto_tutor:           "Supporto del tutor",
    strumenti:                "Strumenti e risorse",
    // Attività
    attivita_svolte:          "Attività svolte",
    compiti_assegnati:        "Compiti assegnati",
    obiettivi_raggiunti:      "Obiettivi raggiunti",
    difficolta_incontrate:    "Difficoltà incontrate",
    // New format __studente__ sub-fields
    nome:    "Nome",
    cognome: "Cognome",
    corso:   "Corso di studi",
    azienda: "Azienda",
    durata:  "Durata (settimane)",
};

function formatResponseDetails(resp) {
    if (!resp || typeof resp !== "object") return "<em>Nessun dettaglio</em>";

    const items = [];

    // Expand __studente__ object into individual readable fields
    if (resp.__studente__ && typeof resp.__studente__ === "object") {
        const s = resp.__studente__;
        const studentFields = ["nome","cognome","corso","anno","azienda","durata"];
        studentFields.forEach(f => {
            if (s[f] != null && s[f] !== "") {
                items.push({ label: QUESTION_LABELS[f] || f, value: String(s[f]) });
            }
        });
    }

    Object.entries(resp).forEach(([k, v]) => {
        // Skip keys rendered separately or that produce raw objects
        if (k === "__studente__" || k === "soft_skills") return;
        // Skip any remaining object or array-of-objects values
        if (v !== null && typeof v === "object") {
            if (Array.isArray(v)) {
                if (v.length > 0 && typeof v[0] === "object") return;
                // array of primitives — join them
                v = v.join(", ");
            } else {
                return;
            }
        }
        const label = QUESTION_LABELS[k] || k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
        items.push({ label, value: String(v ?? "") });
    });

    if (items.length === 0) return "<em>Nessun dettaglio disponibile</em>";

    return items.map(({ label, value }) => `
        <div class="response-detail-item">
            <span class="response-detail-label">${escapeHtml(label)}</span>
            <span class="response-detail-value">${escapeHtml(value)}</span>
        </div>`).join("");
}

async function deleteSurveyResponse(id, btn) {
    if (!confirm("Eliminare questa risposta? L'operazione non e' reversibile.")) return;
    const res = await fetch(`/api/admin/survey-responses/${id}`, { method: "DELETE" });
    if (res.ok) {
        allResponses = allResponses.filter(r => r.id !== id);
        renderResponsesTable(allResponses);
    } else {
        const d = await res.json();
        alert(d.error || "Errore durante l'eliminazione.");
    }
}

async function deleteSurveyResponseFromModal(id, btn) {
    await deleteSurveyResponse(id, btn);
    const modal = btn.closest(".modal");
    if (modal) modal.remove();
}

// ═══════════════════════════════════════════════════════
//  ADMIN: EXPORT / IMPORT
// ═══════════════════════════════════════════════════════
async function exportData() {
    const msgEl = document.getElementById("exportMessage");
    if (msgEl) msgEl.innerHTML = "<em>Esportazione in corso...</em>";
    try {
        const res  = await fetch("/api/admin/export");
        if (!res.ok) throw new Error("Errore server");
        const blob = await res.blob();
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement("a");
        a.href     = url;
        a.download = "stage_review_export.json";
        a.click();
        URL.revokeObjectURL(url);
        if (msgEl) msgEl.innerHTML = `<div class="success">✅ Esportazione completata.</div>`;
    } catch(e) {
        if (msgEl) msgEl.innerHTML = `<div class="error">❌ Errore: ${e.message}</div>`;
    }
}

async function importData() {
    const fileInput = document.getElementById("importFile");
    const msgEl     = document.getElementById("importMessage");
    if (!fileInput.files.length) {
        if (msgEl) msgEl.innerHTML = `<div class="error">❌ Seleziona un file JSON da importare.</div>`;
        return;
    }
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    if (msgEl) msgEl.innerHTML = "<em>Importazione in corso...</em>";
    try {
        const res  = await fetch("/api/admin/import", { method: "POST", body: formData });
        const data = await res.json();
        if (res.ok) {
            if (msgEl) msgEl.innerHTML = `<div class="success">✅ ${escapeHtml(data.message || "Importazione completata.")}</div>`;
            loadDashboardStats();
        } else {
            if (msgEl) msgEl.innerHTML = `<div class="error">❌ ${escapeHtml(data.error || "Errore importazione.")}</div>`;
        }
    } catch(e) {
        if (msgEl) msgEl.innerHTML = `<div class="error">❌ Errore: ${e.message}</div>`;
    }
}

// INIT
const _page = location.pathname.split("/").pop() || "";
if (_page === "login.html" || _page === "register.html" || _page === "") {
    // Pagine pubbliche: nessun init, nessun redirect automatico
} else if (_page === "survey.html") {
    window.onload = loadSurvey;
} else {
    window.onload = () => {
        setupDropdown();
        if (typeof loadDashboardStats === 'function') loadDashboardStats();
        if (typeof loadUsersList     === 'function') loadUsersList();
        if (typeof loadSurveyResponses === 'function') loadSurveyResponses();
    };
}
