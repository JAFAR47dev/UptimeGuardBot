"""
Translation strings for handlers/settings.py and handlers/help.py.

Usage:
    from locales.help_strings import ht
    ht("fr", "settings_menu", current_tz="Europe/Paris")
    ht("es", "help_full", plan_text="Pro", ...)
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # ── settings.py ───────────────────────────────────────────────────
        "settings_menu":
            "⚙️ <b>Settings</b>\n\n"
            "🌍 Timezone: <b>{current_tz}</b>\n\n"
            "What would you like to update?",
        "btn_change_tz":        "🌍 Change Timezone",
        "btn_my_plan":          "📦 My Plan",
        "btn_language":         "🌐 Language",
        "language_picker_prompt":
            "🌐 <b>Choose your language</b>\n\n"
            "Tap a language below:",
        "language_set_confirm": "✅ Language set to <b>English</b> 🇬🇧",
        "tz_change_prompt":
            "🌍 <b>Set Your Timezone</b>\n\n"
            "Type the name of your city and I'll detect your timezone.\n\n"
            "Examples:\n"
            "• <code>London</code>\n"
            "• <code>New York</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>Mumbai</code>\n"
            "• <code>Tokyo</code>\n\n"
            "Send /cancel to go back.",
        "tz_onboarding_prompt":
            "🌍 <b>One quick thing — what city do you live in?</b>\n\n"
            "This lets me send your weekly reports and alerts "
            "at the right time for your timezone.\n\n"
            "Just type your city name:\n"
            "<code>Lagos</code> · <code>London</code> · "
            "<code>New York</code> · <code>Dubai</code>\n\n"
            "Send /skip to use UTC for now.",
        "tz_not_found":
            "❌ <b>Couldn't find \"{city}\".</b>\n\n"
            "Try a larger nearby city, or spell it in English.\n\n"
            "Examples: <code>New York</code>, <code>Moscow</code>, "
            "<code>London</code>, <code>Dubai</code>",
        "tz_found":
            "📍 <b>Found it!</b>\n\n"
            "City: <b>{city}</b>\n"
            "Country: <b>{country}</b>\n"
            "Timezone: <b>{timezone}</b>\n"
            "UTC offset: <b>{utc_offset}</b>\n\n"
            "Is this correct?",
        "btn_tz_yes":           "✅ Yes, save it",
        "btn_tz_no":            "❌ No, try again",
        "tz_saved":
            "✅ <b>Timezone saved!</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "Your weekly reports and scheduled alerts will now "
            "arrive at the right local time for you.",
        "tz_save_error":        "Something went wrong. Use /settings to try again.",
        "tz_retry_prompt":      "No problem. Type your city name again:",
        "tz_skip_confirmed":
            "OK, using UTC for now.\n\n"
            "You can update this anytime via /settings.",
        "settings_cancelled":   "❌ Cancelled.",

        # ── help.py ───────────────────────────────────────────────────────
        "plan_trial":           "✅ Pro (Trial)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 Free",
        "help_full":
            "📖 <b>UptimeGuard Help</b>\n"
            "Your plan: <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>Commands</b>\n"
            "─────────────────────\n\n"

            "/start — Home screen with live snapshot\n\n"
            "/add — Add a new URL to monitor\n"
            "<i>Example: https://mystore.com</i>\n\n"
            "/list — All your monitors with actions\n"
            "<i>Pause, resume, delete, notes, thresholds,\n"
            "webhooks, keyword checks, confirm count</i>\n\n"
            "/status — Quick one-line status per monitor\n"
            "<i>Fastest way to check everything at a glance</i>\n\n"
            "/report — 7-day uptime report\n"
            "<i>Uptime %, avg response time per monitor</i>\n\n"
            "/incidents — Incident history per monitor\n"
            "<i>Timeline of past down events and durations</i>\n\n"
            "/testalert — Send a test down/up alert pair\n"
            "<i>Verify your notifications are working</i>\n\n"
            "/maintenance — Manage maintenance windows\n"
            "<i>Pause alerts during planned downtime</i>\n\n"
            "/team — Manage team notification members\n"
            "<i>Add teammates to receive your alerts (Pro)</i>\n\n"
            "/statuspage — Your public status page\n"
            "<i>Share live uptime with clients</i>\n\n"
            "/referral — Your referral link and stats\n"
            "<i>Earn bonus monitor slots by referring users</i>\n\n"
            "/upgrade — Upgrade to Pro\n\n"
            "/help — This message\n\n"

            "─────────────────────\n"
            "📦 <b>Free Plan</b>\n"
            "─────────────────────\n\n"

            "• Up to {free_limit} monitors\n"
            "• 5-minute check interval\n"
            "• Down + recovery alerts\n"
            "• 7-day uptime history\n"
            "• Monitor notes\n"
            "• Alert snooze\n"
            "• Public status page\n"
            "• Maintenance windows (1 window)\n"
            "• Referral bonus monitor slots\n\n"

            "─────────────────────\n"
            "⭐ <b>Pro Plan</b>\n"
            "─────────────────────\n\n"

            "• Unlimited monitors\n"
            "• 1-minute check interval\n"
            "• SSL certificate expiry warnings\n"
            "• Slow response threshold alerts\n"
            "• HTTP keyword monitoring\n"
            "• Confirm count (reduce false alerts)\n"
            "• Webhook integrations (Slack, PagerDuty)\n"
            "• Team notifications (up to 5 members)\n"
            "• Unlimited maintenance windows\n"
            "• Custom status page title + no branding\n"
            "• Full weekly summary reports\n"
            "• Avg response time tracking\n\n"

            "─────────────────────\n"
            "💰 <b>Pricing</b>\n"
            "─────────────────────\n\n"

            "📅 Monthly       <b>{monthly} Stars</b>\n"
            "📆 3 Months    <b>{three_month} Stars</b>  "
            "<i>save {save_3m} Stars</i>\n"
            "📆 Yearly        <b>{yearly} Stars</b>  "
            "<i>save {save_yr} Stars</i>\n\n"
            "💬 <i>Not happy? Message us within 7 days for a full refund.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>Tips</b>\n"
            "─────────────────────\n\n"

            "• Use ⏸ <b>Pause</b> during planned maintenance "
            "instead of deleting — your history is preserved.\n\n"
            "• Got a down alert while fixing? Tap "
            "🔕 <b>Snooze</b> to silence repeats. "
            "Recovery alerts always fire regardless.\n\n"
            "• Add a 📝 <b>Note</b> to each monitor via /list — "
            "it appears in every down alert so you always know "
            "who to call without checking elsewhere.\n\n"
            "• 🐢 <b>Slow response threshold</b> — get alerted "
            "when a site is slow before it fully goes down "
            "(Pro).\n\n"
            "• 🔑 <b>Keyword monitor</b> — confirm a word or phrase "
            "appears in the page body on every check. "
            "Catches silent failures where the site returns 200 "
            "but shows an error page (Pro).\n\n"
            "• 🔢 <b>Confirm count</b> — require N consecutive "
            "failures before alerting. Eliminates false alarms "
            "from brief network blips (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — connect to Slack or PagerDuty "
            "via /list → Webhook on any monitor (Pro).\n\n"
            "• 🔐 SSL warnings fire at 30, 7, and 1 day before "
            "expiry so you're never caught off guard.\n\n"
            "• 👥 <b>Team alerts</b> — add teammates via /team "
            "so the whole team knows when something goes down (Pro).",

        "btn_add_monitor":      "➕ Add Monitor",
        "btn_test_alert":       "🧪 Test Alert",
        "btn_referral":         "👥 Referral Link",
        "btn_upgrade":          "⭐ Upgrade to Pro",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "settings_menu":
            "⚙️ <b>Paramètres</b>\n\n"
            "🌍 Fuseau horaire : <b>{current_tz}</b>\n\n"
            "Que veux-tu mettre à jour ?",
        "btn_change_tz":        "🌍 Changer le fuseau horaire",
        "btn_my_plan":          "📦 Mon plan",
        "btn_language":         "🌐 Langue",
        "language_picker_prompt":
            "🌐 <b>Choisis ta langue</b>\n\n"
            "Appuie sur une langue ci-dessous :",
        "language_set_confirm": "✅ Langue définie sur <b>Français</b> 🇫🇷",
        "tz_change_prompt":
            "🌍 <b>Définir ton fuseau horaire</b>\n\n"
            "Tape le nom de ta ville et je détecterai ton fuseau horaire.\n\n"
            "Exemples :\n"
            "• <code>London</code>\n"
            "• <code>New York</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>Mumbai</code>\n"
            "• <code>Tokyo</code>\n\n"
            "Envoie /cancel pour revenir.",
        "tz_onboarding_prompt":
            "🌍 <b>Une chose rapide — dans quelle ville vis-tu ?</b>\n\n"
            "Cela me permet d'envoyer tes rapports et alertes "
            "au bon moment local.\n\n"
            "Tape simplement le nom de ta ville :\n"
            "<code>Paris</code> · <code>London</code> · "
            "<code>New York</code> · <code>Dubai</code>\n\n"
            "Envoie /skip pour utiliser UTC pour l'instant.",
        "tz_not_found":
            "❌ <b>Impossible de trouver \"{city}\".</b>\n\n"
            "Essaie une grande ville voisine ou écris-la en anglais.\n\n"
            "Exemples : <code>Paris</code>, <code>Moscow</code>, "
            "<code>London</code>, <code>Dubai</code>",
        "tz_found":
            "📍 <b>Trouvé !</b>\n\n"
            "Ville : <b>{city}</b>\n"
            "Pays : <b>{country}</b>\n"
            "Fuseau : <b>{timezone}</b>\n"
            "Décalage UTC : <b>{utc_offset}</b>\n\n"
            "Est-ce correct ?",
        "btn_tz_yes":           "✅ Oui, enregistrer",
        "btn_tz_no":            "❌ Non, réessayer",
        "tz_saved":
            "✅ <b>Fuseau horaire enregistré !</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "Tes rapports et alertes arriveront désormais "
            "au bon moment local.",
        "tz_save_error":        "Une erreur s'est produite. Utilise /settings pour réessayer.",
        "tz_retry_prompt":      "Pas de problème. Tape à nouveau le nom de ta ville :",
        "tz_skip_confirmed":
            "OK, UTC sera utilisé pour l'instant.\n\n"
            "Tu peux le modifier à tout moment via /settings.",
        "settings_cancelled":   "❌ Annulé.",
        "plan_trial":           "✅ Pro (Essai)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 Gratuit",
        "help_full":
            "📖 <b>Aide UptimeGuard</b>\n"
            "Ton plan : <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>Commandes</b>\n"
            "─────────────────────\n\n"

            "/start — Écran d'accueil avec snapshot en direct\n\n"
            "/add — Ajouter une URL à surveiller\n"
            "<i>Exemple : https://monsite.com</i>\n\n"
            "/list — Tous tes moniteurs avec actions\n"
            "<i>Pause, reprise, suppression, notes, seuils,\n"
            "webhooks, mots-clés, confirmations</i>\n\n"
            "/status — Statut rapide par moniteur\n"
            "<i>La façon la plus rapide de tout vérifier</i>\n\n"
            "/report — Rapport de disponibilité 7 jours\n"
            "<i>Disponibilité % et temps de réponse moyen</i>\n\n"
            "/incidents — Historique des incidents\n"
            "<i>Chronologie des pannes et durées</i>\n\n"
            "/testalert — Envoyer une paire d'alertes test\n"
            "<i>Vérifier que les notifications fonctionnent</i>\n\n"
            "/maintenance — Gérer les fenêtres de maintenance\n"
            "<i>Suspendre les alertes lors de pannes planifiées</i>\n\n"
            "/team — Gérer les membres de l'équipe\n"
            "<i>Ajouter des coéquipiers pour recevoir les alertes (Pro)</i>\n\n"
            "/statuspage — Ta page de statut publique\n"
            "<i>Partager la disponibilité avec tes clients</i>\n\n"
            "/referral — Ton lien de parrainage et statistiques\n"
            "<i>Gagne des emplacements bonus en parrainant des utilisateurs</i>\n\n"
            "/upgrade — Passer à Pro\n\n"
            "/help — Ce message\n\n"

            "─────────────────────\n"
            "📦 <b>Plan gratuit</b>\n"
            "─────────────────────\n\n"

            "• Jusqu'à {free_limit} moniteurs\n"
            "• Vérification toutes les 5 minutes\n"
            "• Alertes de panne et de récupération\n"
            "• Historique de 7 jours\n"
            "• Notes de moniteur\n"
            "• Mise en veille des alertes\n"
            "• Page de statut publique\n"
            "• Fenêtres de maintenance (1 fenêtre)\n"
            "• Emplacements bonus par parrainage\n\n"

            "─────────────────────\n"
            "⭐ <b>Plan Pro</b>\n"
            "─────────────────────\n\n"

            "• Moniteurs illimités\n"
            "• Vérification toutes les minutes\n"
            "• Alertes d'expiration SSL\n"
            "• Alertes de réponse lente\n"
            "• Surveillance par mot-clé HTTP\n"
            "• Comptage de confirmations\n"
            "• Intégrations webhook (Slack, PagerDuty)\n"
            "• Notifications d'équipe (jusqu'à 5 membres)\n"
            "• Fenêtres de maintenance illimitées\n"
            "• Titre personnalisé + sans branding\n"
            "• Rapports hebdomadaires complets\n"
            "• Suivi du temps de réponse moyen\n\n"

            "─────────────────────\n"
            "💰 <b>Tarifs</b>\n"
            "─────────────────────\n\n"

            "📅 Mensuel       <b>{monthly} Stars</b>\n"
            "📆 3 Mois        <b>{three_month} Stars</b>  "
            "<i>économise {save_3m} Stars</i>\n"
            "📆 Annuel         <b>{yearly} Stars</b>  "
            "<i>économise {save_yr} Stars</i>\n\n"
            "💬 <i>Pas satisfait ? Contacte-nous sous 7 jours pour un remboursement complet.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>Conseils</b>\n"
            "─────────────────────\n\n"

            "• Utilise ⏸ <b>Pause</b> pendant la maintenance planifiée "
            "au lieu de supprimer — l'historique est conservé.\n\n"
            "• Alerte reçue pendant une correction ? Appuie sur "
            "🔕 <b>Répéter</b> pour suspendre les répétitions. "
            "Les alertes de récupération sont toujours envoyées.\n\n"
            "• Ajoute une 📝 <b>Note</b> à chaque moniteur via /list — "
            "elle apparaît dans chaque alerte de panne.\n\n"
            "• 🐢 <b>Seuil de réponse lente</b> — sois alerté "
            "quand un site est lent avant qu'il tombe (Pro).\n\n"
            "• 🔑 <b>Surveillance par mot-clé</b> — confirme qu'un mot "
            "apparaît dans la page à chaque vérification (Pro).\n\n"
            "• 🔢 <b>Comptage de confirmations</b> — exige N échecs "
            "consécutifs avant d'alerter (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — connecte Slack ou PagerDuty "
            "via /list → Webhook (Pro).\n\n"
            "• 🔐 Alertes SSL à 30, 7 et 1 jour avant l'expiration.\n\n"
            "• 👥 <b>Alertes équipe</b> — ajoute des coéquipiers via /team (Pro).",

        "btn_add_monitor":      "➕ Ajouter un moniteur",
        "btn_test_alert":       "🧪 Alerte test",
        "btn_referral":         "👥 Lien de parrainage",
        "btn_upgrade":          "⭐ Passer à Pro",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "settings_menu":
            "⚙️ <b>Configuración</b>\n\n"
            "🌍 Zona horaria: <b>{current_tz}</b>\n\n"
            "¿Qué quieres actualizar?",
        "btn_change_tz":        "🌍 Cambiar zona horaria",
        "btn_my_plan":          "📦 Mi plan",
        "btn_language":         "🌐 Idioma",
        "language_picker_prompt":
            "🌐 <b>Elige tu idioma</b>\n\n"
            "Toca un idioma a continuación:",
        "language_set_confirm": "✅ Idioma establecido en <b>Español</b> 🇪🇸",
        "tz_change_prompt":
            "🌍 <b>Establecer tu zona horaria</b>\n\n"
            "Escribe el nombre de tu ciudad y detectaré tu zona horaria.\n\n"
            "Ejemplos:\n"
            "• <code>Madrid</code>\n"
            "• <code>New York</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>Buenos Aires</code>\n"
            "• <code>Tokyo</code>\n\n"
            "Envía /cancel para volver.",
        "tz_onboarding_prompt":
            "🌍 <b>Una cosa rápida — ¿en qué ciudad vives?</b>\n\n"
            "Esto me permite enviarte informes y alertas "
            "a la hora local correcta.\n\n"
            "Escribe el nombre de tu ciudad:\n"
            "<code>Madrid</code> · <code>London</code> · "
            "<code>New York</code> · <code>Dubai</code>\n\n"
            "Envía /skip para usar UTC por ahora.",
        "tz_not_found":
            "❌ <b>No pude encontrar \"{city}\".</b>\n\n"
            "Prueba con una ciudad cercana más grande o escríbela en inglés.\n\n"
            "Ejemplos: <code>New York</code>, <code>Moscow</code>, "
            "<code>London</code>, <code>Dubai</code>",
        "tz_found":
            "📍 <b>¡Encontrado!</b>\n\n"
            "Ciudad: <b>{city}</b>\n"
            "País: <b>{country}</b>\n"
            "Zona horaria: <b>{timezone}</b>\n"
            "Offset UTC: <b>{utc_offset}</b>\n\n"
            "¿Es correcto?",
        "btn_tz_yes":           "✅ Sí, guardar",
        "btn_tz_no":            "❌ No, intentar de nuevo",
        "tz_saved":
            "✅ <b>¡Zona horaria guardada!</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "Tus informes y alertas ahora llegarán "
            "a la hora local correcta.",
        "tz_save_error":        "Algo salió mal. Usa /settings para intentarlo de nuevo.",
        "tz_retry_prompt":      "No hay problema. Escribe el nombre de tu ciudad de nuevo:",
        "tz_skip_confirmed":
            "OK, usando UTC por ahora.\n\n"
            "Puedes actualizarlo en cualquier momento via /settings.",
        "settings_cancelled":   "❌ Cancelado.",
        "plan_trial":           "✅ Pro (Prueba)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 Gratis",
        "help_full":
            "📖 <b>Ayuda de UptimeGuard</b>\n"
            "Tu plan: <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>Comandos</b>\n"
            "─────────────────────\n\n"

            "/start — Pantalla de inicio con snapshot en vivo\n\n"
            "/add — Añadir una URL a monitorear\n"
            "<i>Ejemplo: https://mitienda.com</i>\n\n"
            "/list — Todos tus monitores con acciones\n"
            "<i>Pausar, reanudar, eliminar, notas, umbrales,\n"
            "webhooks, palabras clave, confirmaciones</i>\n\n"
            "/status — Estado rápido por monitor\n"
            "<i>La forma más rápida de verificar todo</i>\n\n"
            "/report — Informe de disponibilidad de 7 días\n"
            "<i>% disponibilidad y tiempo de respuesta promedio</i>\n\n"
            "/incidents — Historial de incidentes\n"
            "<i>Cronología de caídas y duraciones</i>\n\n"
            "/testalert — Enviar un par de alertas de prueba\n"
            "<i>Verificar que las notificaciones funcionan</i>\n\n"
            "/maintenance — Gestionar ventanas de mantenimiento\n"
            "<i>Pausar alertas durante caídas planificadas</i>\n\n"
            "/team — Gestionar miembros del equipo\n"
            "<i>Añadir compañeros para recibir tus alertas (Pro)</i>\n\n"
            "/statuspage — Tu página de estado pública\n"
            "<i>Compartir disponibilidad con clientes</i>\n\n"
            "/referral — Tu enlace de referido y estadísticas\n"
            "<i>Gana espacios extra refiriendo usuarios</i>\n\n"
            "/upgrade — Actualizar a Pro\n\n"
            "/help — Este mensaje\n\n"

            "─────────────────────\n"
            "📦 <b>Plan Gratuito</b>\n"
            "─────────────────────\n\n"

            "• Hasta {free_limit} monitores\n"
            "• Verificación cada 5 minutos\n"
            "• Alertas de caída y recuperación\n"
            "• Historial de 7 días\n"
            "• Notas de monitor\n"
            "• Posponer alertas\n"
            "• Página de estado pública\n"
            "• Ventanas de mantenimiento (1 ventana)\n"
            "• Espacios bonus por referidos\n\n"

            "─────────────────────\n"
            "⭐ <b>Plan Pro</b>\n"
            "─────────────────────\n\n"

            "• Monitores ilimitados\n"
            "• Verificación cada minuto\n"
            "• Alertas de expiración SSL\n"
            "• Alertas de respuesta lenta\n"
            "• Monitoreo por palabra clave HTTP\n"
            "• Conteo de confirmaciones\n"
            "• Integraciones webhook (Slack, PagerDuty)\n"
            "• Notificaciones de equipo (hasta 5 miembros)\n"
            "• Ventanas de mantenimiento ilimitadas\n"
            "• Título personalizado + sin branding\n"
            "• Informes semanales completos\n"
            "• Seguimiento del tiempo de respuesta promedio\n\n"

            "─────────────────────\n"
            "💰 <b>Precios</b>\n"
            "─────────────────────\n\n"

            "📅 Mensual       <b>{monthly} Stars</b>\n"
            "📆 3 Meses     <b>{three_month} Stars</b>  "
            "<i>ahorra {save_3m} Stars</i>\n"
            "📆 Anual          <b>{yearly} Stars</b>  "
            "<i>ahorra {save_yr} Stars</i>\n\n"
            "💬 <i>¿No estás satisfecho? Escríbenos en 7 días para un reembolso completo.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>Consejos</b>\n"
            "─────────────────────\n\n"

            "• Usa ⏸ <b>Pausar</b> durante mantenimiento planificado "
            "en vez de eliminar — tu historial se conserva.\n\n"
            "• ¿Recibiste una alerta mientras arreglas algo? Toca "
            "🔕 <b>Posponer</b> para silenciar repeticiones.\n\n"
            "• Añade una 📝 <b>Nota</b> a cada monitor via /list — "
            "aparece en cada alerta de caída.\n\n"
            "• 🐢 <b>Umbral de respuesta lenta</b> — recibe alertas "
            "antes de que el sitio caiga completamente (Pro).\n\n"
            "• 🔑 <b>Monitor por palabra clave</b> — confirma que una "
            "palabra aparece en la página en cada verificación (Pro).\n\n"
            "• 🔢 <b>Conteo de confirmaciones</b> — requiere N fallos "
            "consecutivos antes de alertar (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — conecta Slack o PagerDuty "
            "via /list → Webhook (Pro).\n\n"
            "• 🔐 Alertas SSL a 30, 7 y 1 día antes de la expiración.\n\n"
            "• 👥 <b>Alertas de equipo</b> — añade compañeros via /team (Pro).",

        "btn_add_monitor":      "➕ Añadir monitor",
        "btn_test_alert":       "🧪 Alerta de prueba",
        "btn_referral":         "👥 Enlace de referido",
        "btn_upgrade":          "⭐ Actualizar a Pro",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "settings_menu":
            "⚙️ <b>الإعدادات</b>\n\n"
            "🌍 المنطقة الزمنية: <b>{current_tz}</b>\n\n"
            "ماذا تريد تحديثه؟",
        "btn_change_tz":        "🌍 تغيير المنطقة الزمنية",
        "btn_my_plan":          "📦 خطتي",
        "btn_language":         "🌐 اللغة",
        "language_picker_prompt":
            "🌐 <b>اختر لغتك</b>\n\n"
            "اضغط على لغة أدناه:",
        "language_set_confirm": "✅ تم تعيين اللغة إلى <b>العربية</b> 🇸🇦",
        "tz_change_prompt":
            "🌍 <b>تعيين منطقتك الزمنية</b>\n\n"
            "اكتب اسم مدينتك وسأكتشف منطقتك الزمنية.\n\n"
            "أمثلة:\n"
            "• <code>Riyadh</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>Cairo</code>\n"
            "• <code>London</code>\n"
            "• <code>New York</code>\n\n"
            "أرسل /cancel للرجوع.",
        "tz_onboarding_prompt":
            "🌍 <b>سؤال سريع — في أي مدينة تعيش؟</b>\n\n"
            "يساعدني هذا في إرسال تقاريرك وتنبيهاتك "
            "في الوقت المحلي الصحيح.\n\n"
            "اكتب اسم مدينتك:\n"
            "<code>Riyadh</code> · <code>Dubai</code> · "
            "<code>Cairo</code> · <code>London</code>\n\n"
            "أرسل /skip لاستخدام UTC الآن.",
        "tz_not_found":
            "❌ <b>تعذّر إيجاد \"{city}\".</b>\n\n"
            "جرّب مدينة أكبر قريبة، أو اكتبها بالإنجليزية.\n\n"
            "أمثلة: <code>Dubai</code>, <code>Cairo</code>, "
            "<code>London</code>, <code>New York</code>",
        "tz_found":
            "📍 <b>تم إيجادها!</b>\n\n"
            "المدينة: <b>{city}</b>\n"
            "البلد: <b>{country}</b>\n"
            "المنطقة الزمنية: <b>{timezone}</b>\n"
            "الفارق عن UTC: <b>{utc_offset}</b>\n\n"
            "هل هذا صحيح؟",
        "btn_tz_yes":           "✅ نعم، حفظ",
        "btn_tz_no":            "❌ لا، حاول مجدداً",
        "tz_saved":
            "✅ <b>تم حفظ المنطقة الزمنية!</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "ستصلك الآن تقاريرك وتنبيهاتك في الوقت المحلي الصحيح.",
        "tz_save_error":        "حدث خطأ ما. استخدم /settings للمحاولة مجدداً.",
        "tz_retry_prompt":      "لا بأس. اكتب اسم مدينتك مجدداً:",
        "tz_skip_confirmed":
            "حسناً، سيتم استخدام UTC الآن.\n\n"
            "يمكنك التغيير في أي وقت عبر /settings.",
        "settings_cancelled":   "❌ تم الإلغاء.",
        "plan_trial":           "✅ Pro (تجربة)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 مجاني",
        "help_full":
            "📖 <b>مساعدة UptimeGuard</b>\n"
            "خطتك: <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>الأوامر</b>\n"
            "─────────────────────\n\n"

            "/start — الشاشة الرئيسية مع لقطة مباشرة\n\n"
            "/add — إضافة رابط للمراقبة\n"
            "<i>مثال: https://متجري.com</i>\n\n"
            "/list — جميع مراقبيك مع الإجراءات\n"
            "<i>إيقاف مؤقت، استئناف، حذف، ملاحظات، حدود،\n"
            "webhooks، كلمات مفتاحية، تأكيدات</i>\n\n"
            "/status — حالة سريعة لكل مراقب\n"
            "<i>أسرع طريقة للتحقق من كل شيء</i>\n\n"
            "/report — تقرير التوفر لـ 7 أيام\n"
            "<i>نسبة التوفر ومتوسط وقت الاستجابة</i>\n\n"
            "/incidents — سجل الحوادث\n"
            "<i>جدول زمني للتوقفات والمدد</i>\n\n"
            "/testalert — إرسال زوج من التنبيهات التجريبية\n"
            "<i>التحقق من عمل الإشعارات</i>\n\n"
            "/maintenance — إدارة نوافذ الصيانة\n"
            "<i>إيقاف التنبيهات أثناء التوقف المخطط</i>\n\n"
            "/team — إدارة أعضاء الفريق\n"
            "<i>إضافة زملاء لتلقي تنبيهاتك (Pro)</i>\n\n"
            "/statuspage — صفحة الحالة العامة\n"
            "<i>مشاركة التوفر مع العملاء</i>\n\n"
            "/referral — رابط إحالتك وإحصائياتك\n"
            "<i>اكسب فتحات مراقبة إضافية بإحالة المستخدمين</i>\n\n"
            "/upgrade — الترقية إلى Pro\n\n"
            "/help — هذه الرسالة\n\n"

            "─────────────────────\n"
            "📦 <b>الخطة المجانية</b>\n"
            "─────────────────────\n\n"

            "• حتى {free_limit} مراقبين\n"
            "• فحص كل 5 دقائق\n"
            "• تنبيهات التوقف والاستعادة\n"
            "• سجل 7 أيام\n"
            "• ملاحظات المراقب\n"
            "• تأجيل التنبيهات\n"
            "• صفحة حالة عامة\n"
            "• نوافذ الصيانة (نافذة واحدة)\n"
            "• فتحات مكافأة للإحالات\n\n"

            "─────────────────────\n"
            "⭐ <b>خطة Pro</b>\n"
            "─────────────────────\n\n"

            "• مراقبون غير محدودون\n"
            "• فحص كل دقيقة\n"
            "• تحذيرات انتهاء SSL\n"
            "• تنبيهات الاستجابة البطيئة\n"
            "• مراقبة بالكلمة المفتاحية HTTP\n"
            "• عدد التأكيدات\n"
            "• تكاملات Webhook (Slack, PagerDuty)\n"
            "• إشعارات الفريق (حتى 5 أعضاء)\n"
            "• نوافذ صيانة غير محدودة\n"
            "• عنوان مخصص + بدون علامة تجارية\n"
            "• تقارير أسبوعية كاملة\n"
            "• تتبع متوسط وقت الاستجابة\n\n"

            "─────────────────────\n"
            "💰 <b>الأسعار</b>\n"
            "─────────────────────\n\n"

            "📅 شهري          <b>{monthly} نجمة</b>\n"
            "📆 3 أشهر       <b>{three_month} نجمة</b>  "
            "<i>وفّر {save_3m} نجمة</i>\n"
            "📆 سنوي           <b>{yearly} نجمة</b>  "
            "<i>وفّر {save_yr} نجمة</i>\n\n"
            "💬 <i>غير راضٍ؟ راسلنا خلال 7 أيام لاسترداد كامل.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>نصائح</b>\n"
            "─────────────────────\n\n"

            "• استخدم ⏸ <b>إيقاف مؤقت</b> أثناء الصيانة المخططة "
            "بدلاً من الحذف — يُحفظ سجلك.\n\n"
            "• تلقيت تنبيهاً أثناء الإصلاح؟ اضغط "
            "🔕 <b>تأجيل</b> لإسكات التكرار.\n\n"
            "• أضف 📝 <b>ملاحظة</b> لكل مراقب عبر /list — "
            "تظهر في كل تنبيه توقف.\n\n"
            "• 🐢 <b>حد الاستجابة البطيئة</b> — احصل على تنبيه "
            "قبل أن يتوقف الموقع كلياً (Pro).\n\n"
            "• 🔑 <b>مراقبة الكلمة المفتاحية</b> — تأكد من ظهور "
            "كلمة في الصفحة عند كل فحص (Pro).\n\n"
            "• 🔢 <b>عدد التأكيدات</b> — اشترط N فشل متتالٍ "
            "قبل التنبيه (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — اربط Slack أو PagerDuty "
            "عبر /list → Webhook (Pro).\n\n"
            "• 🔐 تنبيهات SSL قبل 30 و7 و1 يوم من الانتهاء.\n\n"
            "• 👥 <b>تنبيهات الفريق</b> — أضف زملاء عبر /team (Pro).",

        "btn_add_monitor":      "➕ إضافة مراقب",
        "btn_test_alert":       "🧪 تنبيه تجريبي",
        "btn_referral":         "👥 رابط الإحالة",
        "btn_upgrade":          "⭐ الترقية إلى Pro",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "settings_menu":
            "⚙️ <b>Configurações</b>\n\n"
            "🌍 Fuso horário: <b>{current_tz}</b>\n\n"
            "O que você gostaria de atualizar?",
        "btn_change_tz":        "🌍 Alterar fuso horário",
        "btn_my_plan":          "📦 Meu plano",
        "btn_language":         "🌐 Idioma",
        "language_picker_prompt":
            "🌐 <b>Escolha seu idioma</b>\n\n"
            "Toque em um idioma abaixo:",
        "language_set_confirm": "✅ Idioma definido para <b>Português</b> 🇧🇷",
        "tz_change_prompt":
            "🌍 <b>Definir seu fuso horário</b>\n\n"
            "Digite o nome da sua cidade e eu detectarei seu fuso horário.\n\n"
            "Exemplos:\n"
            "• <code>São Paulo</code>\n"
            "• <code>Lisbon</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>London</code>\n"
            "• <code>New York</code>\n\n"
            "Envie /cancel para voltar.",
        "tz_onboarding_prompt":
            "🌍 <b>Uma coisa rápida — em qual cidade você mora?</b>\n\n"
            "Isso me permite enviar seus relatórios e alertas "
            "no horário local correto.\n\n"
            "Digite o nome da sua cidade:\n"
            "<code>São Paulo</code> · <code>Lisbon</code> · "
            "<code>London</code> · <code>Dubai</code>\n\n"
            "Envie /skip para usar UTC por ora.",
        "tz_not_found":
            "❌ <b>Não encontrei \"{city}\".</b>\n\n"
            "Tente uma cidade maior próxima ou escreva em inglês.\n\n"
            "Exemplos: <code>Sao Paulo</code>, <code>Lisbon</code>, "
            "<code>London</code>, <code>Dubai</code>",
        "tz_found":
            "📍 <b>Encontrado!</b>\n\n"
            "Cidade: <b>{city}</b>\n"
            "País: <b>{country}</b>\n"
            "Fuso horário: <b>{timezone}</b>\n"
            "Offset UTC: <b>{utc_offset}</b>\n\n"
            "Está correto?",
        "btn_tz_yes":           "✅ Sim, salvar",
        "btn_tz_no":            "❌ Não, tentar novamente",
        "tz_saved":
            "✅ <b>Fuso horário salvo!</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "Seus relatórios e alertas agora "
            "chegarão no horário local correto.",
        "tz_save_error":        "Algo deu errado. Use /settings para tentar novamente.",
        "tz_retry_prompt":      "Sem problema. Digite o nome da sua cidade novamente:",
        "tz_skip_confirmed":
            "OK, usando UTC por ora.\n\n"
            "Você pode alterar a qualquer momento via /settings.",
        "settings_cancelled":   "❌ Cancelado.",
        "plan_trial":           "✅ Pro (Teste)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 Gratuito",
        "help_full":
            "📖 <b>Ajuda do UptimeGuard</b>\n"
            "Seu plano: <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>Comandos</b>\n"
            "─────────────────────\n\n"

            "/start — Tela inicial com snapshot ao vivo\n\n"
            "/add — Adicionar uma URL para monitorar\n"
            "<i>Exemplo: https://meusite.com</i>\n\n"
            "/list — Todos os seus monitores com ações\n"
            "<i>Pausar, retomar, excluir, notas, limites,\n"
            "webhooks, palavras-chave, confirmações</i>\n\n"
            "/status — Status rápido por monitor\n"
            "<i>A forma mais rápida de verificar tudo</i>\n\n"
            "/report — Relatório de disponibilidade de 7 dias\n"
            "<i>% de disponibilidade e tempo de resposta médio</i>\n\n"
            "/incidents — Histórico de incidentes\n"
            "<i>Linha do tempo de quedas e durações</i>\n\n"
            "/testalert — Enviar um par de alertas de teste\n"
            "<i>Verificar que as notificações funcionam</i>\n\n"
            "/maintenance — Gerenciar janelas de manutenção\n"
            "<i>Pausar alertas durante quedas planejadas</i>\n\n"
            "/team — Gerenciar membros da equipe\n"
            "<i>Adicionar membros para receber seus alertas (Pro)</i>\n\n"
            "/statuspage — Sua página de status pública\n"
            "<i>Compartilhar disponibilidade com clientes</i>\n\n"
            "/referral — Seu link de indicação e estatísticas\n"
            "<i>Ganhe slots extras indicando usuários</i>\n\n"
            "/upgrade — Atualizar para Pro\n\n"
            "/help — Esta mensagem\n\n"

            "─────────────────────\n"
            "📦 <b>Plano Gratuito</b>\n"
            "─────────────────────\n\n"

            "• Até {free_limit} monitores\n"
            "• Verificação a cada 5 minutos\n"
            "• Alertas de queda e recuperação\n"
            "• Histórico de 7 dias\n"
            "• Notas de monitor\n"
            "• Adiar alertas\n"
            "• Página de status pública\n"
            "• Janelas de manutenção (1 janela)\n"
            "• Slots bônus por indicação\n\n"

            "─────────────────────\n"
            "⭐ <b>Plano Pro</b>\n"
            "─────────────────────\n\n"

            "• Monitores ilimitados\n"
            "• Verificação a cada minuto\n"
            "• Alertas de expiração SSL\n"
            "• Alertas de resposta lenta\n"
            "• Monitoramento por palavra-chave HTTP\n"
            "• Contagem de confirmações\n"
            "• Integrações webhook (Slack, PagerDuty)\n"
            "• Notificações de equipe (até 5 membros)\n"
            "• Janelas de manutenção ilimitadas\n"
            "• Título personalizado + sem branding\n"
            "• Relatórios semanais completos\n"
            "• Rastreamento do tempo de resposta médio\n\n"

            "─────────────────────\n"
            "💰 <b>Preços</b>\n"
            "─────────────────────\n\n"

            "📅 Mensal        <b>{monthly} Stars</b>\n"
            "📆 3 Meses     <b>{three_month} Stars</b>  "
            "<i>economize {save_3m} Stars</i>\n"
            "📆 Anual           <b>{yearly} Stars</b>  "
            "<i>economize {save_yr} Stars</i>\n\n"
            "💬 <i>Não satisfeito? Fale conosco em 7 dias para reembolso completo.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>Dicas</b>\n"
            "─────────────────────\n\n"

            "• Use ⏸ <b>Pausar</b> durante manutenção planejada "
            "em vez de excluir — seu histórico é preservado.\n\n"
            "• Recebeu um alerta enquanto corrige algo? Toque em "
            "🔕 <b>Adiar</b> para silenciar repetições.\n\n"
            "• Adicione uma 📝 <b>Nota</b> a cada monitor via /list — "
            "ela aparece em cada alerta de queda.\n\n"
            "• 🐢 <b>Limite de resposta lenta</b> — receba alertas "
            "antes que o site caia completamente (Pro).\n\n"
            "• 🔑 <b>Monitor por palavra-chave</b> — confirme que uma "
            "palavra aparece na página em cada verificação (Pro).\n\n"
            "• 🔢 <b>Contagem de confirmações</b> — exija N falhas "
            "consecutivas antes de alertar (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — conecte Slack ou PagerDuty "
            "via /list → Webhook (Pro).\n\n"
            "• 🔐 Alertas SSL a 30, 7 e 1 dia antes da expiração.\n\n"
            "• 👥 <b>Alertas de equipe</b> — adicione membros via /team (Pro).",

        "btn_add_monitor":      "➕ Adicionar monitor",
        "btn_test_alert":       "🧪 Alerta de teste",
        "btn_referral":         "👥 Link de indicação",
        "btn_upgrade":          "⭐ Atualizar para Pro",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "settings_menu":
            "⚙️ <b>Настройки</b>\n\n"
            "🌍 Часовой пояс: <b>{current_tz}</b>\n\n"
            "Что хочешь обновить?",
        "btn_change_tz":        "🌍 Изменить часовой пояс",
        "btn_my_plan":          "📦 Мой тариф",
        "btn_language":         "🌐 Язык",
        "language_picker_prompt":
            "🌐 <b>Выбери язык</b>\n\n"
            "Нажми на язык ниже:",
        "language_set_confirm": "✅ Язык установлен на <b>Русский</b> 🇷🇺",
        "tz_change_prompt":
            "🌍 <b>Установить часовой пояс</b>\n\n"
            "Напиши название своего города, и я определю часовой пояс.\n\n"
            "Примеры:\n"
            "• <code>Moscow</code>\n"
            "• <code>London</code>\n"
            "• <code>Dubai</code>\n"
            "• <code>New York</code>\n"
            "• <code>Tokyo</code>\n\n"
            "Отправь /cancel для возврата.",
        "tz_onboarding_prompt":
            "🌍 <b>Один быстрый вопрос — в каком городе ты живёшь?</b>\n\n"
            "Это позволит мне отправлять отчёты и уведомления "
            "в правильное местное время.\n\n"
            "Просто напиши название города:\n"
            "<code>Moscow</code> · <code>London</code> · "
            "<code>New York</code> · <code>Dubai</code>\n\n"
            "Отправь /skip, чтобы использовать UTC пока.",
        "tz_not_found":
            "❌ <b>Не удалось найти \"{city}\".</b>\n\n"
            "Попробуй большой соседний город или напиши название по-английски.\n\n"
            "Примеры: <code>Moscow</code>, <code>London</code>, "
            "<code>New York</code>, <code>Dubai</code>",
        "tz_found":
            "📍 <b>Найдено!</b>\n\n"
            "Город: <b>{city}</b>\n"
            "Страна: <b>{country}</b>\n"
            "Часовой пояс: <b>{timezone}</b>\n"
            "Смещение UTC: <b>{utc_offset}</b>\n\n"
            "Всё верно?",
        "btn_tz_yes":           "✅ Да, сохранить",
        "btn_tz_no":            "❌ Нет, попробовать снова",
        "tz_saved":
            "✅ <b>Часовой пояс сохранён!</b>\n\n"
            "📍 {city}\n"
            "🌍 {timezone}\n\n"
            "Твои отчёты и уведомления теперь будут приходить "
            "в правильное местное время.",
        "tz_save_error":        "Что-то пошло не так. Используй /settings для повторной попытки.",
        "tz_retry_prompt":      "Не проблема. Напиши название города ещё раз:",
        "tz_skip_confirmed":
            "OK, пока используется UTC.\n\n"
            "Ты можешь изменить это в любой момент через /settings.",
        "settings_cancelled":   "❌ Отменено.",
        "plan_trial":           "✅ Pro (Пробный)",
        "plan_pro":             "✅ Pro",
        "plan_free":            "🆓 Бесплатный",
        "help_full":
            "📖 <b>Справка UptimeGuard</b>\n"
            "Твой тариф: <b>{plan_text}</b>\n\n"

            "─────────────────────\n"
            "⚙️ <b>Команды</b>\n"
            "─────────────────────\n\n"

            "/start — Главный экран с живым снимком\n\n"
            "/add — Добавить URL для мониторинга\n"
            "<i>Пример: https://мойсайт.com</i>\n\n"
            "/list — Все твои мониторы с действиями\n"
            "<i>Пауза, возобновление, удаление, заметки, пороги,\n"
            "webhooks, ключевые слова, подтверждения</i>\n\n"
            "/status — Быстрый статус по каждому монитору\n"
            "<i>Самый быстрый способ проверить всё</i>\n\n"
            "/report — Отчёт о доступности за 7 дней\n"
            "<i>% доступности и среднее время ответа</i>\n\n"
            "/incidents — История инцидентов\n"
            "<i>Хронология падений и длительностей</i>\n\n"
            "/testalert — Отправить тестовую пару уведомлений\n"
            "<i>Проверить работу уведомлений</i>\n\n"
            "/maintenance — Управление окнами обслуживания\n"
            "<i>Приостановить уведомления при плановом простое</i>\n\n"
            "/team — Управление участниками команды\n"
            "<i>Добавить участников для получения уведомлений (Pro)</i>\n\n"
            "/statuspage — Публичная страница статуса\n"
            "<i>Поделиться доступностью с клиентами</i>\n\n"
            "/referral — Реферальная ссылка и статистика\n"
            "<i>Зарабатывай дополнительные слоты, приглашая пользователей</i>\n\n"
            "/upgrade — Перейти на Pro\n\n"
            "/help — Это сообщение\n\n"

            "─────────────────────\n"
            "📦 <b>Бесплатный план</b>\n"
            "─────────────────────\n\n"

            "• До {free_limit} мониторов\n"
            "• Проверка каждые 5 минут\n"
            "• Уведомления о падении и восстановлении\n"
            "• История за 7 дней\n"
            "• Заметки к мониторам\n"
            "• Отложить уведомления\n"
            "• Публичная страница статуса\n"
            "• Окна обслуживания (1 окно)\n"
            "• Бонусные слоты за рефералы\n\n"

            "─────────────────────\n"
            "⭐ <b>Тариф Pro</b>\n"
            "─────────────────────\n\n"

            "• Неограниченное количество мониторов\n"
            "• Проверка каждую минуту\n"
            "• Предупреждения об истечении SSL\n"
            "• Уведомления о медленном ответе\n"
            "• Мониторинг по ключевому слову HTTP\n"
            "• Счётчик подтверждений\n"
            "• Интеграции webhook (Slack, PagerDuty)\n"
            "• Командные уведомления (до 5 участников)\n"
            "• Неограниченные окна обслуживания\n"
            "• Пользовательский заголовок + без брендинга\n"
            "• Полные еженедельные отчёты\n"
            "• Отслеживание среднего времени ответа\n\n"

            "─────────────────────\n"
            "💰 <b>Цены</b>\n"
            "─────────────────────\n\n"

            "📅 Ежемесячно    <b>{monthly} Stars</b>\n"
            "📆 3 Месяца      <b>{three_month} Stars</b>  "
            "<i>экономия {save_3m} Stars</i>\n"
            "📆 Ежегодно       <b>{yearly} Stars</b>  "
            "<i>экономия {save_yr} Stars</i>\n\n"
            "💬 <i>Не доволен? Напиши нам в течение 7 дней — полный возврат.</i>\n\n"

            "─────────────────────\n"
            "💡 <b>Советы</b>\n"
            "─────────────────────\n\n"

            "• Используй ⏸ <b>Паузу</b> при плановом обслуживании "
            "вместо удаления — история сохраняется.\n\n"
            "• Получил уведомление во время исправления? Нажми "
            "🔕 <b>Отложить</b>, чтобы заглушить повторы.\n\n"
            "• Добавь 📝 <b>Заметку</b> к каждому монитору через /list — "
            "она появляется в каждом уведомлении о падении.\n\n"
            "• 🐢 <b>Порог медленного ответа</b> — получай уведомление "
            "до полного падения сайта (Pro).\n\n"
            "• 🔑 <b>Мониторинг по ключевому слову</b> — проверяй наличие "
            "слова на странице при каждой проверке (Pro).\n\n"
            "• 🔢 <b>Счётчик подтверждений</b> — требуй N последовательных "
            "отказов перед уведомлением (Pro).\n\n"
            "• 🔗 <b>Webhooks</b> — подключи Slack или PagerDuty "
            "через /list → Webhook (Pro).\n\n"
            "• 🔐 SSL-предупреждения за 30, 7 и 1 день до истечения.\n\n"
            "• 👥 <b>Командные уведомления</b> — добавь участников через /team (Pro).",

        "btn_add_monitor":      "➕ Добавить монитор",
        "btn_test_alert":       "🧪 Тестовое уведомление",
        "btn_referral":         "👥 Реферальная ссылка",
        "btn_upgrade":          "⭐ Перейти на Pro",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"

# Maps each lang code to its option button label (flag + name in that language)
LANGUAGE_OPTIONS: dict[str, str] = {
    "en": "🇬🇧 English",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "ar": "🇸🇦 العربية",
    "pt": "🇧🇷 Português",
    "ru": "🇷🇺 Русский",
}


def ht(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in help/settings locale for `lang`, falling back to English.

    Usage:
        from locales.help_strings import ht
        ht("fr", "settings_menu", current_tz="Europe/Paris")
        ht("ru", "help_full", plan_text="Pro", free_limit=3, ...)
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string
    
    