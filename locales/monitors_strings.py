# locales/monitors_strings.py
"""
Translation strings for handlers/monitors.py — high-impact flows only.

Covered: /add flow, /list output, /status output, post-add follow-up.
Deep-flow setup conversations (threshold, note, webhook, keyword, confirm)
remain in English as they are used by already-engaged power users.

Re-uses the same t() / resolve_lang() helpers from locales.start_strings.
Import via:
    from locales.monitors_strings import mt
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # /add flow
        "add_rate_limit":
            "⏳ Please wait <b>{remaining}s</b> before adding another monitor.",
        "add_limit_reached":
            "⚠️ You've used all <b>{limit}{bonus_str}</b> monitor slots.\n\n"
            "Upgrade to Pro for unlimited monitors, or invite friends "
            "to earn bonus slots via /start.",
        "add_limit_bonus_str":  " (+{bonus} referral bonus)",
        "btn_upgrade_pro":      "⭐ Upgrade to Pro",
        "add_ask_url":
            "🌐 Send me the URL to monitor.\n\n"
            "Example: <code>https://mysite.com</code>\n\n"
            "Send /cancel to abort.",
        "add_invalid_url":
            "⚠️ That doesn't look like a valid URL.\n\n"
            "Please send a full URL like:\n<code>https://mysite.com</code>",
        "add_duplicate_url":
            "⚠️ You're already monitoring <code>{url}</code>\n\n"
            "Use /list to see your active monitors.",
        "add_unreachable":
            "❌ <b>Could not reach that URL.</b>\n\n"
            "Error: {error}\n\n"
            "Double-check the URL and try again, or send a different one.",
        "add_url_ok":
            "✅ URL looks good!\n\n"
            "🏷 Give it a label (or /skip to use the URL as label):",
        "add_something_wrong":
            "⚠️ Something went wrong. Send /cancel and try again.",
        "add_success":
            "✅ <b>Monitor added!</b>\n\n"
            "🏷 Label: {label}\n"
            "🌐 URL: <code>{url}</code>\n"
            "⏱ Check interval: every {interval} min"
            "{slots_line}\n\n"
            "I'll alert you instantly if it goes down.",
        "add_success_nolabel":
            "✅ <b>Monitor added!</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ Every {interval} min\n\n"
            "You'll be alerted instantly on downtime.",
        "add_slots_line":       "\n📦 Monitors used: <b>{active}/{limit}</b>",

        # post-add follow-up
        "followup_up":
            "🟢 <b>{label}</b> is <b>UP</b> and being monitored.\n\n"
            "You'll get an instant alert the moment it goes down. "
            "Run /testalert to make sure notifications reach you.",
        "followup_down":
            "🔴 <b>{label}</b> appears to be <b>DOWN</b> right now!\n\n"
            "Checking again on the next interval. "
            "You'll get a full alert either way.",

        # /list
        "list_no_monitors":     "You have no monitors yet.\n\nUse /add to add one.",
        "list_header":          "📋 <b>Your Monitors:</b>\n\n",
        "list_paused_suffix":   " (paused)",
        "list_uptime":          "   📊 Uptime (7d): {uptime_str}\n",
        "list_keyword":         "   🔑 Keyword: <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (case-sensitive)",
        "list_confirms":        "   🌍 Confirmations: {count} checks\n",
        "list_threshold":       "   🐢 Slow alert: {threshold_str}\n",
        "list_threshold_none":  "not set",
        "list_webhook":         "   🔗 Webhook: <code>{domain}</code>\n",

        # /status
        "status_no_monitors":   "No monitors yet. Use /add to add your first one.",
        "status_header":        "⚡ <b>Monitor Status</b>\n",
        "status_paused":        "Paused",
        "status_up":            "Up",
        "status_down":          "Down",
        "status_pending":       "Pending first check",
        "status_just_now":      "just now",
        "status_1min":          "1 min ago",
        "status_mins":          "{mins} mins ago",
        "status_hours":         "{h}h ago",
        "status_not_checked":   "not checked yet",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",

        # keyboard buttons (monitors)
        "btn_resume":           "▶️ Resume {label}",
        "btn_pause":            "⏸ Pause {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ Edit Note",
        "btn_add_note":         "📝 Add Note",
        "btn_edit_keyword":     "✏️ Keyword",
        "btn_add_keyword":      "🔑 Keyword",
        "btn_confirmations":    "🌍 Confirmations",
        "btn_threshold":        "🐢 Threshold",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "add_rate_limit":
            "⏳ Attends <b>{remaining}s</b> avant d'ajouter un autre moniteur.",
        "add_limit_reached":
            "⚠️ Tu as utilisé tous tes <b>{limit}{bonus_str}</b> emplacements.\n\n"
            "Passe à Pro pour des moniteurs illimités, ou invite des amis "
            "pour gagner des emplacements via /start.",
        "add_limit_bonus_str":  " (+{bonus} bonus parrainage)",
        "btn_upgrade_pro":      "⭐ Passer à Pro",
        "add_ask_url":
            "🌐 Envoie-moi l'URL à surveiller.\n\n"
            "Exemple : <code>https://monsite.com</code>\n\n"
            "Envoie /cancel pour annuler.",
        "add_invalid_url":
            "⚠️ Ça ne ressemble pas à une URL valide.\n\n"
            "Envoie une URL complète comme :\n<code>https://monsite.com</code>",
        "add_duplicate_url":
            "⚠️ Tu surveilles déjà <code>{url}</code>\n\n"
            "Utilise /list pour voir tes moniteurs actifs.",
        "add_unreachable":
            "❌ <b>Impossible d'atteindre cette URL.</b>\n\n"
            "Erreur : {error}\n\n"
            "Vérifie l'URL et réessaie, ou envoie une autre URL.",
        "add_url_ok":
            "✅ L'URL est valide !\n\n"
            "🏷 Donne-lui un nom (ou /skip pour utiliser l'URL comme nom) :",
        "add_something_wrong":
            "⚠️ Une erreur s'est produite. Envoie /cancel et réessaie.",
        "add_success":
            "✅ <b>Moniteur ajouté !</b>\n\n"
            "🏷 Nom : {label}\n"
            "🌐 URL : <code>{url}</code>\n"
            "⏱ Vérification toutes les {interval} min"
            "{slots_line}\n\n"
            "Je t'alerterai immédiatement en cas de panne.",
        "add_success_nolabel":
            "✅ <b>Moniteur ajouté !</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ Toutes les {interval} min\n\n"
            "Tu seras alerté instantanément en cas de panne.",
        "add_slots_line":       "\n📦 Moniteurs utilisés : <b>{active}/{limit}</b>",
        "followup_up":
            "🟢 <b>{label}</b> est <b>EN LIGNE</b> et surveillé.\n\n"
            "Tu recevras une alerte immédiate si ça tombe. "
            "Lance /testalert pour vérifier que les notifications fonctionnent.",
        "followup_down":
            "🔴 <b>{label}</b> semble être <b>HORS LIGNE</b> en ce moment !\n\n"
            "Nouvelle vérification au prochain intervalle. "
            "Tu recevras une alerte dans tous les cas.",
        "list_no_monitors":     "Tu n'as pas encore de moniteurs.\n\nUtilise /add pour en ajouter un.",
        "list_header":          "📋 <b>Tes moniteurs :</b>\n\n",
        "list_paused_suffix":   " (en pause)",
        "list_uptime":          "   📊 Disponibilité (7j) : {uptime_str}\n",
        "list_keyword":         "   🔑 Mot-clé : <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (sensible à la casse)",
        "list_confirms":        "   🌍 Confirmations : {count} vérifications\n",
        "list_threshold":       "   🐢 Alerte lenteur : {threshold_str}\n",
        "list_threshold_none":  "non défini",
        "list_webhook":         "   🔗 Webhook : <code>{domain}</code>\n",
        "status_no_monitors":   "Aucun moniteur. Utilise /add pour commencer.",
        "status_header":        "⚡ <b>Statut des moniteurs</b>\n",
        "status_paused":        "En pause",
        "status_up":            "En ligne",
        "status_down":          "Hors ligne",
        "status_pending":       "En attente de la première vérification",
        "status_just_now":      "à l'instant",
        "status_1min":          "il y a 1 min",
        "status_mins":          "il y a {mins} min",
        "status_hours":         "il y a {h}h",
        "status_not_checked":   "pas encore vérifié",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",
        "btn_resume":           "▶️ Reprendre {label}",
        "btn_pause":            "⏸ Pause {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ Modifier la note",
        "btn_add_note":         "📝 Ajouter une note",
        "btn_edit_keyword":     "✏️ Mot-clé",
        "btn_add_keyword":      "🔑 Mot-clé",
        "btn_confirmations":    "🌍 Confirmations",
        "btn_threshold":        "🐢 Seuil",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "add_rate_limit":
            "⏳ Espera <b>{remaining}s</b> antes de añadir otro monitor.",
        "add_limit_reached":
            "⚠️ Has usado todos tus <b>{limit}{bonus_str}</b> espacios.\n\n"
            "Actualiza a Pro para monitores ilimitados, o invita amigos "
            "para ganar espacios extra via /start.",
        "add_limit_bonus_str":  " (+{bonus} bonus por referidos)",
        "btn_upgrade_pro":      "⭐ Actualizar a Pro",
        "add_ask_url":
            "🌐 Envíame la URL a monitorear.\n\n"
            "Ejemplo: <code>https://misitioweb.com</code>\n\n"
            "Envía /cancel para cancelar.",
        "add_invalid_url":
            "⚠️ Eso no parece una URL válida.\n\n"
            "Envía una URL completa como:\n<code>https://misitioweb.com</code>",
        "add_duplicate_url":
            "⚠️ Ya estás monitoreando <code>{url}</code>\n\n"
            "Usa /list para ver tus monitores activos.",
        "add_unreachable":
            "❌ <b>No se pudo alcanzar esa URL.</b>\n\n"
            "Error: {error}\n\n"
            "Verifica la URL e intenta de nuevo, o envía una diferente.",
        "add_url_ok":
            "✅ ¡URL válida!\n\n"
            "🏷 Dale un nombre (o /skip para usar la URL como nombre):",
        "add_something_wrong":
            "⚠️ Algo salió mal. Envía /cancel e intenta de nuevo.",
        "add_success":
            "✅ <b>¡Monitor añadido!</b>\n\n"
            "🏷 Nombre: {label}\n"
            "🌐 URL: <code>{url}</code>\n"
            "⏱ Intervalo: cada {interval} min"
            "{slots_line}\n\n"
            "Te alertaré al instante si cae.",
        "add_success_nolabel":
            "✅ <b>¡Monitor añadido!</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ Cada {interval} min\n\n"
            "Serás alertado al instante si cae.",
        "add_slots_line":       "\n📦 Monitores usados: <b>{active}/{limit}</b>",
        "followup_up":
            "🟢 <b>{label}</b> está <b>ACTIVO</b> y siendo monitoreado.\n\n"
            "Recibirás una alerta inmediata si cae. "
            "Ejecuta /testalert para verificar que las notificaciones funcionan.",
        "followup_down":
            "🔴 <b>{label}</b> parece estar <b>CAÍDO</b> ahora mismo.\n\n"
            "Se verificará en el próximo intervalo. "
            "Recibirás una alerta de cualquier manera.",
        "list_no_monitors":     "Aún no tienes monitores.\n\nUsa /add para añadir uno.",
        "list_header":          "📋 <b>Tus monitores:</b>\n\n",
        "list_paused_suffix":   " (pausado)",
        "list_uptime":          "   📊 Disponibilidad (7d): {uptime_str}\n",
        "list_keyword":         "   🔑 Palabra clave: <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (sensible a mayúsculas)",
        "list_confirms":        "   🌍 Confirmaciones: {count} verificaciones\n",
        "list_threshold":       "   🐢 Alerta lentitud: {threshold_str}\n",
        "list_threshold_none":  "no establecido",
        "list_webhook":         "   🔗 Webhook: <code>{domain}</code>\n",
        "status_no_monitors":   "Sin monitores aún. Usa /add para empezar.",
        "status_header":        "⚡ <b>Estado de monitores</b>\n",
        "status_paused":        "Pausado",
        "status_up":            "Activo",
        "status_down":          "Caído",
        "status_pending":       "Esperando primera verificación",
        "status_just_now":      "ahora mismo",
        "status_1min":          "hace 1 min",
        "status_mins":          "hace {mins} min",
        "status_hours":         "hace {h}h",
        "status_not_checked":   "aún no verificado",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",
        "btn_resume":           "▶️ Reanudar {label}",
        "btn_pause":            "⏸ Pausar {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ Editar nota",
        "btn_add_note":         "📝 Añadir nota",
        "btn_edit_keyword":     "✏️ Palabra clave",
        "btn_add_keyword":      "🔑 Palabra clave",
        "btn_confirmations":    "🌍 Confirmaciones",
        "btn_threshold":        "🐢 Umbral",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "add_rate_limit":
            "⏳ انتظر <b>{remaining}s</b> قبل إضافة مراقب آخر.",
        "add_limit_reached":
            "⚠️ لقد استخدمت جميع <b>{limit}{bonus_str}</b> فتحة مراقبة.\n\n"
            "يُرقِّي إلى Pro لمراقبين غير محدودين، أو ادعُ أصدقاء "
            "لكسب فتحات إضافية عبر /start.",
        "add_limit_bonus_str":  " (+{bonus} مكافأة إحالة)",
        "btn_upgrade_pro":      "⭐ الترقية إلى Pro",
        "add_ask_url":
            "🌐 أرسل لي الرابط الذي تريد مراقبته.\n\n"
            "مثال: <code>https://موقعي.com</code>\n\n"
            "أرسل /cancel للإلغاء.",
        "add_invalid_url":
            "⚠️ هذا لا يبدو رابطاً صحيحاً.\n\n"
            "أرسل رابطاً كاملاً مثل:\n<code>https://موقعي.com</code>",
        "add_duplicate_url":
            "⚠️ أنت بالفعل تراقب <code>{url}</code>\n\n"
            "استخدم /list لعرض مراقبيك النشطين.",
        "add_unreachable":
            "❌ <b>تعذّر الوصول إلى هذا الرابط.</b>\n\n"
            "الخطأ: {error}\n\n"
            "تحقق من الرابط وحاول مجدداً، أو أرسل رابطاً آخر.",
        "add_url_ok":
            "✅ الرابط صحيح!\n\n"
            "🏷 أعطه تسمية (أو /skip لاستخدام الرابط كتسمية):",
        "add_something_wrong":
            "⚠️ حدث خطأ ما. أرسل /cancel وحاول مجدداً.",
        "add_success":
            "✅ <b>تمت إضافة المراقب!</b>\n\n"
            "🏷 التسمية: {label}\n"
            "🌐 الرابط: <code>{url}</code>\n"
            "⏱ الفاصل الزمني: كل {interval} دقيقة"
            "{slots_line}\n\n"
            "سأنبّهك فوراً إذا توقف الموقع.",
        "add_success_nolabel":
            "✅ <b>تمت إضافة المراقب!</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ كل {interval} دقيقة\n\n"
            "ستُنبَّه فوراً في حال التوقف.",
        "add_slots_line":       "\n📦 المراقبون المستخدمون: <b>{active}/{limit}</b>",
        "followup_up":
            "🟢 <b>{label}</b> يعمل <b>بشكل طبيعي</b> ويتم مراقبته.\n\n"
            "ستحصل على تنبيه فوري إذا توقف. "
            "شغّل /testalert للتأكد من وصول الإشعارات.",
        "followup_down":
            "🔴 <b>{label}</b> يبدو <b>متوقفاً</b> الآن!\n\n"
            "سيتم التحقق في الفترة التالية. "
            "ستحصل على تنبيه في كلتا الحالتين.",
        "list_no_monitors":     "ليس لديك مراقبون بعد.\n\nاستخدم /add لإضافة واحد.",
        "list_header":          "📋 <b>مراقبوك:</b>\n\n",
        "list_paused_suffix":   " (موقوف مؤقتاً)",
        "list_uptime":          "   📊 التوفر (7 أيام): {uptime_str}\n",
        "list_keyword":         "   🔑 الكلمة المفتاحية: <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (حساس لحالة الأحرف)",
        "list_confirms":        "   🌍 التأكيدات: {count} فحوصات\n",
        "list_threshold":       "   🐢 تنبيه البطء: {threshold_str}\n",
        "list_threshold_none":  "غير محدد",
        "list_webhook":         "   🔗 Webhook: <code>{domain}</code>\n",
        "status_no_monitors":   "لا يوجد مراقبون بعد. استخدم /add للبدء.",
        "status_header":        "⚡ <b>حالة المراقبين</b>\n",
        "status_paused":        "موقوف مؤقتاً",
        "status_up":            "يعمل",
        "status_down":          "متوقف",
        "status_pending":       "في انتظار أول فحص",
        "status_just_now":      "الآن",
        "status_1min":          "منذ دقيقة",
        "status_mins":          "منذ {mins} دقيقة",
        "status_hours":         "منذ {h} ساعة",
        "status_not_checked":   "لم يتم الفحص بعد",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",
        "btn_resume":           "▶️ استئناف {label}",
        "btn_pause":            "⏸ إيقاف مؤقت {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ تعديل الملاحظة",
        "btn_add_note":         "📝 إضافة ملاحظة",
        "btn_edit_keyword":     "✏️ الكلمة المفتاحية",
        "btn_add_keyword":      "🔑 كلمة مفتاحية",
        "btn_confirmations":    "🌍 التأكيدات",
        "btn_threshold":        "🐢 الحد الأقصى",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "add_rate_limit":
            "⏳ Aguarde <b>{remaining}s</b> antes de adicionar outro monitor.",
        "add_limit_reached":
            "⚠️ Você usou todos os <b>{limit}{bonus_str}</b> slots de monitor.\n\n"
            "Atualize para Pro para monitores ilimitados, ou convide amigos "
            "para ganhar slots extras via /start.",
        "add_limit_bonus_str":  " (+{bonus} bônus por indicação)",
        "btn_upgrade_pro":      "⭐ Atualizar para Pro",
        "add_ask_url":
            "🌐 Envie-me a URL para monitorar.\n\n"
            "Exemplo: <code>https://meusite.com</code>\n\n"
            "Envie /cancel para cancelar.",
        "add_invalid_url":
            "⚠️ Isso não parece uma URL válida.\n\n"
            "Envie uma URL completa como:\n<code>https://meusite.com</code>",
        "add_duplicate_url":
            "⚠️ Você já está monitorando <code>{url}</code>\n\n"
            "Use /list para ver seus monitores ativos.",
        "add_unreachable":
            "❌ <b>Não foi possível acessar essa URL.</b>\n\n"
            "Erro: {error}\n\n"
            "Verifique a URL e tente novamente, ou envie uma diferente.",
        "add_url_ok":
            "✅ URL válida!\n\n"
            "🏷 Dê um nome a ela (ou /skip para usar a URL como nome):",
        "add_something_wrong":
            "⚠️ Algo deu errado. Envie /cancel e tente novamente.",
        "add_success":
            "✅ <b>Monitor adicionado!</b>\n\n"
            "🏷 Nome: {label}\n"
            "🌐 URL: <code>{url}</code>\n"
            "⏱ Intervalo: a cada {interval} min"
            "{slots_line}\n\n"
            "Vou te alertar imediatamente se cair.",
        "add_success_nolabel":
            "✅ <b>Monitor adicionado!</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ A cada {interval} min\n\n"
            "Você será alertado imediatamente se cair.",
        "add_slots_line":       "\n📦 Monitores usados: <b>{active}/{limit}</b>",
        "followup_up":
            "🟢 <b>{label}</b> está <b>NO AR</b> e sendo monitorado.\n\n"
            "Você receberá um alerta imediato se cair. "
            "Execute /testalert para confirmar que as notificações chegam.",
        "followup_down":
            "🔴 <b>{label}</b> parece estar <b>FORA DO AR</b> agora!\n\n"
            "Verificaremos no próximo intervalo. "
            "Você receberá um alerta de qualquer forma.",
        "list_no_monitors":     "Você ainda não tem monitores.\n\nUse /add para adicionar um.",
        "list_header":          "📋 <b>Seus monitores:</b>\n\n",
        "list_paused_suffix":   " (pausado)",
        "list_uptime":          "   📊 Disponibilidade (7d): {uptime_str}\n",
        "list_keyword":         "   🔑 Palavra-chave: <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (sensível a maiúsculas)",
        "list_confirms":        "   🌍 Confirmações: {count} verificações\n",
        "list_threshold":       "   🐢 Alerta lentidão: {threshold_str}\n",
        "list_threshold_none":  "não definido",
        "list_webhook":         "   🔗 Webhook: <code>{domain}</code>\n",
        "status_no_monitors":   "Nenhum monitor ainda. Use /add para começar.",
        "status_header":        "⚡ <b>Status dos Monitores</b>\n",
        "status_paused":        "Pausado",
        "status_up":            "No ar",
        "status_down":          "Fora do ar",
        "status_pending":       "Aguardando primeira verificação",
        "status_just_now":      "agora mesmo",
        "status_1min":          "há 1 min",
        "status_mins":          "há {mins} min",
        "status_hours":         "há {h}h",
        "status_not_checked":   "ainda não verificado",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",
        "btn_resume":           "▶️ Retomar {label}",
        "btn_pause":            "⏸ Pausar {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ Editar nota",
        "btn_add_note":         "📝 Adicionar nota",
        "btn_edit_keyword":     "✏️ Palavra-chave",
        "btn_add_keyword":      "🔑 Palavra-chave",
        "btn_confirmations":    "🌍 Confirmações",
        "btn_threshold":        "🐢 Limite",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "add_rate_limit":
            "⏳ Подожди <b>{remaining}s</b> перед добавлением следующего монитора.",
        "add_limit_reached":
            "⚠️ Ты использовал все <b>{limit}{bonus_str}</b> слота.\n\n"
            "Перейди на Pro для неограниченных мониторов или пригласи друзей "
            "через /start, чтобы получить бонусные слоты.",
        "add_limit_bonus_str":  " (+{bonus} реферальный бонус)",
        "btn_upgrade_pro":      "⭐ Перейти на Pro",
        "add_ask_url":
            "🌐 Отправь мне URL для мониторинга.\n\n"
            "Пример: <code>https://мойсайт.com</code>\n\n"
            "Отправь /cancel для отмены.",
        "add_invalid_url":
            "⚠️ Это не похоже на правильный URL.\n\n"
            "Отправь полный URL, например:\n<code>https://мойсайт.com</code>",
        "add_duplicate_url":
            "⚠️ Ты уже мониторишь <code>{url}</code>\n\n"
            "Используй /list для просмотра активных мониторов.",
        "add_unreachable":
            "❌ <b>Не удалось подключиться к этому URL.</b>\n\n"
            "Ошибка: {error}\n\n"
            "Проверь URL и попробуй снова, или отправь другой.",
        "add_url_ok":
            "✅ URL выглядит правильно!\n\n"
            "🏷 Дай ему название (или /skip, чтобы использовать URL как название):",
        "add_something_wrong":
            "⚠️ Что-то пошло не так. Отправь /cancel и попробуй снова.",
        "add_success":
            "✅ <b>Монитор добавлен!</b>\n\n"
            "🏷 Название: {label}\n"
            "🌐 URL: <code>{url}</code>\n"
            "⏱ Интервал проверки: каждые {interval} мин"
            "{slots_line}\n\n"
            "Я мгновенно оповещу тебя, если сайт упадёт.",
        "add_success_nolabel":
            "✅ <b>Монитор добавлен!</b>\n\n"
            "🌐 <code>{url}</code>\n"
            "⏱ Каждые {interval} мин\n\n"
            "Ты получишь мгновенное уведомление при падении.",
        "add_slots_line":       "\n📦 Используется мониторов: <b>{active}/{limit}</b>",
        "followup_up":
            "🟢 <b>{label}</b> <b>работает</b> и мониторится.\n\n"
            "Ты получишь мгновенное уведомление, если сайт упадёт. "
            "Запусти /testalert, чтобы убедиться в доставке уведомлений.",
        "followup_down":
            "🔴 <b>{label}</b> похоже <b>недоступен</b> прямо сейчас!\n\n"
            "Следующая проверка скоро. "
            "Ты получишь уведомление в любом случае.",
        "list_no_monitors":     "У тебя пока нет мониторов.\n\nИспользуй /add для добавления.",
        "list_header":          "📋 <b>Твои мониторы:</b>\n\n",
        "list_paused_suffix":   " (на паузе)",
        "list_uptime":          "   📊 Доступность (7д): {uptime_str}\n",
        "list_keyword":         "   🔑 Ключевое слово: <code>{keyword}</code>{case_str}\n",
        "list_keyword_cs":      " (с учётом регистра)",
        "list_confirms":        "   🌍 Подтверждений: {count} проверки\n",
        "list_threshold":       "   🐢 Алерт медлительности: {threshold_str}\n",
        "list_threshold_none":  "не установлен",
        "list_webhook":         "   🔗 Webhook: <code>{domain}</code>\n",
        "status_no_monitors":   "Мониторов пока нет. Используй /add для начала.",
        "status_header":        "⚡ <b>Статус мониторов</b>\n",
        "status_paused":        "На паузе",
        "status_up":            "Работает",
        "status_down":          "Недоступен",
        "status_pending":       "Ожидание первой проверки",
        "status_just_now":      "только что",
        "status_1min":          "1 мин назад",
        "status_mins":          "{mins} мин назад",
        "status_hours":         "{h}ч назад",
        "status_not_checked":   "ещё не проверялся",
        "status_line":          "{icon} <b>{label}</b> — {status_text} <i>({ago})</i>",
        "btn_resume":           "▶️ Возобновить {label}",
        "btn_pause":            "⏸ Пауза {label}",
        "btn_delete":           "🗑",
        "btn_edit_note":        "✏️ Изменить заметку",
        "btn_add_note":         "📝 Добавить заметку",
        "btn_edit_keyword":     "✏️ Ключевое слово",
        "btn_add_keyword":      "🔑 Ключевое слово",
        "btn_confirmations":    "🌍 Подтверждения",
        "btn_threshold":        "🐢 Порог",
        "btn_edit_webhook":     "✏️ Webhook",
        "btn_add_webhook":      "🔗 Webhook",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


def mt(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in monitors locale for `lang`, falling back to English.

    Usage:
        from locales.monitors_strings import mt
        mt("fr", "add_ask_url")
        mt("es", "add_success", label="My Store", url="...", interval=5, slots_line="")
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string
