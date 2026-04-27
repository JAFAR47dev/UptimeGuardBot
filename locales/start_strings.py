# locales/start_strings.py
"""
Translation strings for handlers/start.py.

Supported languages: en, fr, es, ar, pt, ru
Fallback: en

Usage:
    from locales.start_strings import t
    text = t(lang, "welcome_greeting", name="Alice")
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# String tables
# ---------------------------------------------------------------------------

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        "welcome_greeting":     "👋 Hey {name}, welcome to <b>UptimeGuard</b>!\n\n",
        "welcome_back":         "👋 Hey {name}, you're back!\n\n",
        "welcome_body":
            "Get instant Telegram alerts the moment your website "
            "goes down — before your users notice.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>Referral reward:</b> Invite {goal} friends who add a monitor "
            "→ earn <b>+{bonus} free monitor slots</b>!\n\n"
            "Your invite link:\n<code>{ref_link}</code>",
        "plan_trial":           "✅ 7-day Pro trial active — all Pro features unlocked",
        "plan_free":            "🆓 Free plan",
        "checklist":
            "📋 <b>Getting started</b>\n"
            "✅ Joined UptimeGuard\n"
            "⬜ Add your first monitor\n"
            "⬜ Receive your first alert\n\n",
        "btn_add_first":        "➕ Add My First Monitor",
        "btn_how_it_works":     "📖 How it works",
        "btn_invite":           "👥 Invite Friends",
        "btn_add_monitor":      "➕ Add Monitor",
        "btn_invite_earn":      "👥 Invite Friends & Earn Rewards",
        "btn_upgrade":          "⭐ Upgrade to Pro",
        "btn_status":           "⚡ Status",
        "btn_list":             "📋 List",
        "btn_report":           "📊 Report",
        "health_down":          "{count} monitor(s) currently DOWN ⚠️",
        "health_paused":        "All monitors paused",
        "health_ok":            "All systems operational",
        "plan_trial_label":     "✅ Pro (Trial)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 Free",
        "slots_line":           "\n📦 Monitors: <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} referral bonus)",
        "referral_bar":         "\n👥 Referrals: {bar}",
        "nudge_testalert":
            "\n\n💡 <i>Tip: run /testalert to confirm your notifications work.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 Plan: <b>{plan_label}</b>{slots_line}\n"
            "📡 Monitors: <b>{total}</b> total • "
            "<b>{up}</b> up • "
            "<b>{down}</b> down • "
            "<b>{paused}</b> paused\n\n"
            "Status: <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>How UptimeGuard works</b>\n\n"
            "1️⃣ Add a URL with /add\n"
            "2️⃣ We ping it every 5 min (free) or 1 min (Pro)\n"
            "3️⃣ If it goes down you get an instant alert here\n"
            "4️⃣ When it recovers you get another alert\n\n"
            "<b>Pro also includes:</b>\n"
            "🔐 SSL expiry warnings\n"
            "🐢 Slow response alerts\n"
            "📊 Weekly summary reports\n"
            "🔗 Webhook integrations\n"
            "👥 Team notifications\n\n"
            "👇 Ready to add your first monitor?",
        "referral_title":       "👥 <b>Referral Programme</b>\n\n",
        "referral_progress":    "Progress to next reward: {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>Reward unlocked!</b> You've earned {tiers} reward tier(s).\n"
            "Rewards are applied automatically. Keep inviting to earn more!",
        "referral_remaining":
            "Invite <b>{remaining} more friend(s)</b> who add a monitor "
            "to unlock <b>+{bonus} free monitor slots</b>!",
        "referral_bonus_line":  "\n🎁 Bonus slots earned so far: <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 Your invite link:\n<code>{ref_link}</code>\n\n"
            "Share it with friends — they get UptimeGuard, "
            "you get +{bonus} monitor slots per {goal} who join!",
        "tz_prompt_title":      "🌍 <b>Quick setup — set your timezone</b>\n\n",
        "tz_prompt_body":
            "This helps reports and alerts arrive at the right local time for you.",
        "btn_set_tz":           "🌍 Set My Timezone",
        "btn_skip_tz":          "⏭ Skip",
        "admin_new_user":
            "👤 <b>New user joined UptimeGuard</b>\n\n"
            "Name: <b>{full_name}</b>\n"
            "Username: {username}\n"
            "ID: <code>{user_id}</code>\n"
            "Language: <b>{lang}</b>\n"
            "Time: {time}",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "welcome_greeting":     "👋 Salut {name}, bienvenue sur <b>UptimeGuard</b> !\n\n",
        "welcome_back":         "👋 Salut {name}, content de te revoir !\n\n",
        "welcome_body":
            "Reçois des alertes Telegram instantanées dès que ton site tombe "
            "— avant que tes utilisateurs s'en rendent compte.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>Parrainage :</b> Invite {goal} amis qui ajoutent un moniteur "
            "→ gagne <b>+{bonus} emplacements gratuits</b> !\n\n"
            "Ton lien d'invitation :\n<code>{ref_link}</code>",
        "plan_trial":           "✅ Essai Pro 7 jours actif — toutes les fonctions Pro débloquées",
        "plan_free":            "🆓 Plan gratuit",
        "checklist":
            "📋 <b>Pour commencer</b>\n"
            "✅ Rejoint UptimeGuard\n"
            "⬜ Ajouter ton premier moniteur\n"
            "⬜ Recevoir ta première alerte\n\n",
        "btn_add_first":        "➕ Ajouter mon premier moniteur",
        "btn_how_it_works":     "📖 Comment ça marche",
        "btn_invite":           "👥 Inviter des amis",
        "btn_add_monitor":      "➕ Ajouter un moniteur",
        "btn_invite_earn":      "👥 Inviter & gagner des récompenses",
        "btn_upgrade":          "⭐ Passer à Pro",
        "btn_status":           "⚡ Statut",
        "btn_list":             "📋 Liste",
        "btn_report":           "📊 Rapport",
        "health_down":          "{count} moniteur(s) actuellement HORS LIGNE ⚠️",
        "health_paused":        "Tous les moniteurs sont en pause",
        "health_ok":            "Tous les systèmes opérationnels",
        "plan_trial_label":     "✅ Pro (Essai)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 Gratuit",
        "slots_line":           "\n📦 Moniteurs : <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} bonus parrainage)",
        "referral_bar":         "\n👥 Parrainages : {bar}",
        "nudge_testalert":
            "\n\n💡 <i>Astuce : lance /testalert pour vérifier que tu reçois bien les alertes.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 Plan : <b>{plan_label}</b>{slots_line}\n"
            "📡 Moniteurs : <b>{total}</b> total • "
            "<b>{up}</b> actifs • "
            "<b>{down}</b> hors ligne • "
            "<b>{paused}</b> en pause\n\n"
            "Statut : <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>Comment fonctionne UptimeGuard</b>\n\n"
            "1️⃣ Ajoute une URL avec /add\n"
            "2️⃣ On la vérifie toutes les 5 min (gratuit) ou 1 min (Pro)\n"
            "3️⃣ Si elle tombe, tu reçois une alerte immédiate\n"
            "4️⃣ Quand elle revient, tu reçois une autre alerte\n\n"
            "<b>Pro inclut aussi :</b>\n"
            "🔐 Alertes expiration SSL\n"
            "🐢 Alertes réponse lente\n"
            "📊 Rapports hebdomadaires\n"
            "🔗 Intégrations webhook\n"
            "👥 Notifications d'équipe\n\n"
            "👇 Prêt à ajouter ton premier moniteur ?",
        "referral_title":       "👥 <b>Programme de parrainage</b>\n\n",
        "referral_progress":    "Progression vers la prochaine récompense : {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>Récompense débloquée !</b> Tu as gagné {tiers} niveau(x).\n"
            "Les récompenses sont appliquées automatiquement. Continue d'inviter !",
        "referral_remaining":
            "Invite <b>{remaining} ami(s) supplémentaire(s)</b> qui ajoutent un moniteur "
            "pour débloquer <b>+{bonus} emplacements gratuits</b> !",
        "referral_bonus_line":  "\n🎁 Bonus obtenus : <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 Ton lien d'invitation :\n<code>{ref_link}</code>\n\n"
            "Partage-le — tes amis obtiennent UptimeGuard, "
            "tu gagnes +{bonus} emplacements par {goal} inscrits !",
        "tz_prompt_title":      "🌍 <b>Configuration rapide — définis ton fuseau horaire</b>\n\n",
        "tz_prompt_body":
            "Cela permet que tes rapports et alertes arrivent au bon moment local.",
        "btn_set_tz":           "🌍 Définir mon fuseau horaire",
        "btn_skip_tz":          "⏭ Ignorer",
        "admin_new_user":
            "👤 <b>Nouvel utilisateur sur UptimeGuard</b>\n\n"
            "Nom : <b>{full_name}</b>\n"
            "Pseudo : {username}\n"
            "ID : <code>{user_id}</code>\n"
            "Langue : <b>{lang}</b>\n"
            "Heure : {time}",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "welcome_greeting":     "👋 ¡Hola {name}, bienvenido a <b>UptimeGuard</b>!\n\n",
        "welcome_back":         "👋 ¡Hola {name}, qué bueno verte de nuevo!\n\n",
        "welcome_body":
            "Recibe alertas instantáneas en Telegram cuando tu sitio caiga "
            "— antes de que tus usuarios lo noten.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>Recompensa por referidos:</b> Invita {goal} amigos que añadan un monitor "
            "→ gana <b>+{bonus} espacios gratuitos</b>.\n\n"
            "Tu enlace de invitación:\n<code>{ref_link}</code>",
        "plan_trial":           "✅ Prueba Pro de 7 días activa — todas las funciones Pro disponibles",
        "plan_free":            "🆓 Plan gratuito",
        "checklist":
            "📋 <b>Para empezar</b>\n"
            "✅ Te uniste a UptimeGuard\n"
            "⬜ Añadir tu primer monitor\n"
            "⬜ Recibir tu primera alerta\n\n",
        "btn_add_first":        "➕ Añadir mi primer monitor",
        "btn_how_it_works":     "📖 Cómo funciona",
        "btn_invite":           "👥 Invitar amigos",
        "btn_add_monitor":      "➕ Añadir monitor",
        "btn_invite_earn":      "👥 Invitar y ganar recompensas",
        "btn_upgrade":          "⭐ Actualizar a Pro",
        "btn_status":           "⚡ Estado",
        "btn_list":             "📋 Lista",
        "btn_report":           "📊 Informe",
        "health_down":          "{count} monitor(es) CAÍDO(S) ahora ⚠️",
        "health_paused":        "Todos los monitores en pausa",
        "health_ok":            "Todos los sistemas operativos",
        "plan_trial_label":     "✅ Pro (Prueba)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 Gratis",
        "slots_line":           "\n📦 Monitores: <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} bonus por referidos)",
        "referral_bar":         "\n👥 Referidos: {bar}",
        "nudge_testalert":
            "\n\n💡 <i>Consejo: ejecuta /testalert para confirmar que recibes alertas.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 Plan: <b>{plan_label}</b>{slots_line}\n"
            "📡 Monitores: <b>{total}</b> total • "
            "<b>{up}</b> activos • "
            "<b>{down}</b> caídos • "
            "<b>{paused}</b> en pausa\n\n"
            "Estado: <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>Cómo funciona UptimeGuard</b>\n\n"
            "1️⃣ Añade una URL con /add\n"
            "2️⃣ La verificamos cada 5 min (gratis) o 1 min (Pro)\n"
            "3️⃣ Si cae, recibes una alerta inmediata\n"
            "4️⃣ Cuando se recupera, recibes otra alerta\n\n"
            "<b>Pro también incluye:</b>\n"
            "🔐 Avisos de expiración SSL\n"
            "🐢 Alertas de respuesta lenta\n"
            "📊 Informes semanales\n"
            "🔗 Integraciones webhook\n"
            "👥 Notificaciones de equipo\n\n"
            "👇 ¿Listo para añadir tu primer monitor?",
        "referral_title":       "👥 <b>Programa de referidos</b>\n\n",
        "referral_progress":    "Progreso hacia la próxima recompensa: {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>¡Recompensa desbloqueada!</b> Has ganado {tiers} nivel(es).\n"
            "Las recompensas se aplican automáticamente. ¡Sigue invitando!",
        "referral_remaining":
            "Invita a <b>{remaining} amigo(s) más</b> que añadan un monitor "
            "para desbloquear <b>+{bonus} espacios gratuitos</b>.",
        "referral_bonus_line":  "\n🎁 Bonus ganados hasta ahora: <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 Tu enlace de invitación:\n<code>{ref_link}</code>\n\n"
            "Compártelo — tus amigos obtienen UptimeGuard, "
            "tú ganas +{bonus} espacios por cada {goal} que se unan.",
        "tz_prompt_title":      "🌍 <b>Configuración rápida — establece tu zona horaria</b>\n\n",
        "tz_prompt_body":
            "Esto ayuda a que los informes y alertas lleguen a la hora local correcta.",
        "btn_set_tz":           "🌍 Establecer mi zona horaria",
        "btn_skip_tz":          "⏭ Omitir",
        "admin_new_user":
            "👤 <b>Nuevo usuario en UptimeGuard</b>\n\n"
            "Nombre: <b>{full_name}</b>\n"
            "Usuario: {username}\n"
            "ID: <code>{user_id}</code>\n"
            "Idioma: <b>{lang}</b>\n"
            "Hora: {time}",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "welcome_greeting":     "👋 أهلاً {name}، مرحباً بك في <b>UptimeGuard</b>!\n\n",
        "welcome_back":         "👋 أهلاً {name}، يسعدنا عودتك!\n\n",
        "welcome_body":
            "احصل على تنبيهات فورية عبر تيليغرام فور توقف موقعك "
            "— قبل أن يلاحظ مستخدموك.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>مكافأة الإحالة:</b> ادعُ {goal} أصدقاء يضيفون مراقباً "
            "← احصل على <b>+{bonus} فتحات مجانية</b>!\n\n"
            "رابط دعوتك:\n<code>{ref_link}</code>",
        "plan_trial":           "✅ تجربة Pro لمدة 7 أيام — جميع مزايا Pro مفعّلة",
        "plan_free":            "🆓 الخطة المجانية",
        "checklist":
            "📋 <b>للبدء</b>\n"
            "✅ انضممت إلى UptimeGuard\n"
            "⬜ إضافة أول مراقب\n"
            "⬜ استلام أول تنبيه\n\n",
        "btn_add_first":        "➕ إضافة أول مراقب",
        "btn_how_it_works":     "📖 كيف يعمل",
        "btn_invite":           "👥 دعوة أصدقاء",
        "btn_add_monitor":      "➕ إضافة مراقب",
        "btn_invite_earn":      "👥 دعوة الأصدقاء وكسب المكافآت",
        "btn_upgrade":          "⭐ الترقية إلى Pro",
        "btn_status":           "⚡ الحالة",
        "btn_list":             "📋 القائمة",
        "btn_report":           "📊 التقرير",
        "health_down":          "{count} مراقب(ون) معطّل(ون) الآن ⚠️",
        "health_paused":        "جميع المراقبات في وضع الإيقاف المؤقت",
        "health_ok":            "جميع الأنظمة تعمل بشكل طبيعي",
        "plan_trial_label":     "✅ Pro (تجربة)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 مجاني",
        "slots_line":           "\n📦 المراقبون: <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} مكافأة إحالة)",
        "referral_bar":         "\n👥 الإحالات: {bar}",
        "nudge_testalert":
            "\n\n💡 <i>نصيحة: شغّل /testalert للتأكد من وصول التنبيهات.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 الخطة: <b>{plan_label}</b>{slots_line}\n"
            "📡 المراقبون: <b>{total}</b> إجمالي • "
            "<b>{up}</b> نشط • "
            "<b>{down}</b> معطّل • "
            "<b>{paused}</b> موقوف مؤقتاً\n\n"
            "الحالة: <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>كيف يعمل UptimeGuard</b>\n\n"
            "1️⃣ أضف رابطاً عبر /add\n"
            "2️⃣ نفحصه كل 5 دقائق (مجاني) أو دقيقة (Pro)\n"
            "3️⃣ إذا توقف، تصلك تنبيهات فورية\n"
            "4️⃣ عند استعادته، تصلك تنبيه آخر\n\n"
            "<b>Pro يشمل أيضاً:</b>\n"
            "🔐 تحذيرات انتهاء SSL\n"
            "🐢 تنبيهات الاستجابة البطيئة\n"
            "📊 تقارير أسبوعية\n"
            "🔗 تكامل Webhook\n"
            "👥 إشعارات الفريق\n\n"
            "👇 هل أنت مستعد لإضافة أول مراقب؟",
        "referral_title":       "👥 <b>برنامج الإحالة</b>\n\n",
        "referral_progress":    "التقدم نحو المكافأة التالية: {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>تم فتح المكافأة!</b> حصلت على {tiers} مستوى (مستويات).\n"
            "تُطبَّق المكافآت تلقائياً. استمر في الدعوة!",
        "referral_remaining":
            "ادعُ <b>{remaining} صديق(اً) آخر</b> يضيف مراقباً "
            "لفتح <b>+{bonus} فتحات مجانية</b>!",
        "referral_bonus_line":  "\n🎁 الفتحات المكتسبة حتى الآن: <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 رابط دعوتك:\n<code>{ref_link}</code>\n\n"
            "شاركه مع أصدقائك — يحصلون على UptimeGuard، "
            "وتحصل أنت على +{bonus} فتحات لكل {goal} ينضمون.",
        "tz_prompt_title":      "🌍 <b>إعداد سريع — حدد منطقتك الزمنية</b>\n\n",
        "tz_prompt_body":
            "يساعد هذا في وصول التقارير والتنبيهات في الوقت المحلي الصحيح.",
        "btn_set_tz":           "🌍 تحديد منطقتي الزمنية",
        "btn_skip_tz":          "⏭ تخطّ",
        "admin_new_user":
            "👤 <b>مستخدم جديد انضم إلى UptimeGuard</b>\n\n"
            "الاسم: <b>{full_name}</b>\n"
            "المعرّف: {username}\n"
            "المعرف الرقمي: <code>{user_id}</code>\n"
            "اللغة: <b>{lang}</b>\n"
            "الوقت: {time}",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "welcome_greeting":     "👋 Olá {name}, bem-vindo ao <b>UptimeGuard</b>!\n\n",
        "welcome_back":         "👋 Olá {name}, que bom ter você de volta!\n\n",
        "welcome_body":
            "Receba alertas instantâneos no Telegram assim que seu site cair "
            "— antes que seus usuários percebam.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>Recompensa por indicação:</b> Convide {goal} amigos que adicionem um monitor "
            "→ ganhe <b>+{bonus} vagas gratuitas</b>!\n\n"
            "Seu link de convite:\n<code>{ref_link}</code>",
        "plan_trial":           "✅ Período de teste Pro de 7 dias ativo — todos os recursos Pro desbloqueados",
        "plan_free":            "🆓 Plano gratuito",
        "checklist":
            "📋 <b>Primeiros passos</b>\n"
            "✅ Entrou no UptimeGuard\n"
            "⬜ Adicionar seu primeiro monitor\n"
            "⬜ Receber seu primeiro alerta\n\n",
        "btn_add_first":        "➕ Adicionar meu primeiro monitor",
        "btn_how_it_works":     "📖 Como funciona",
        "btn_invite":           "👥 Convidar amigos",
        "btn_add_monitor":      "➕ Adicionar monitor",
        "btn_invite_earn":      "👥 Convidar e ganhar recompensas",
        "btn_upgrade":          "⭐ Atualizar para Pro",
        "btn_status":           "⚡ Status",
        "btn_list":             "📋 Lista",
        "btn_report":           "📊 Relatório",
        "health_down":          "{count} monitor(es) FORA DO AR agora ⚠️",
        "health_paused":        "Todos os monitores pausados",
        "health_ok":            "Todos os sistemas operacionais",
        "plan_trial_label":     "✅ Pro (Teste)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 Gratuito",
        "slots_line":           "\n📦 Monitores: <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} bônus por indicação)",
        "referral_bar":         "\n👥 Indicações: {bar}",
        "nudge_testalert":
            "\n\n💡 <i>Dica: execute /testalert para confirmar que você recebe alertas.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 Plano: <b>{plan_label}</b>{slots_line}\n"
            "📡 Monitores: <b>{total}</b> total • "
            "<b>{up}</b> ativos • "
            "<b>{down}</b> fora do ar • "
            "<b>{paused}</b> pausados\n\n"
            "Status: <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>Como o UptimeGuard funciona</b>\n\n"
            "1️⃣ Adicione uma URL com /add\n"
            "2️⃣ Verificamos a cada 5 min (grátis) ou 1 min (Pro)\n"
            "3️⃣ Se cair, você recebe um alerta imediato\n"
            "4️⃣ Quando se recuperar, você recebe outro alerta\n\n"
            "<b>Pro também inclui:</b>\n"
            "🔐 Avisos de expiração SSL\n"
            "🐢 Alertas de resposta lenta\n"
            "📊 Relatórios semanais\n"
            "🔗 Integrações webhook\n"
            "👥 Notificações de equipe\n\n"
            "👇 Pronto para adicionar seu primeiro monitor?",
        "referral_title":       "👥 <b>Programa de indicação</b>\n\n",
        "referral_progress":    "Progresso para a próxima recompensa: {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>Recompensa desbloqueada!</b> Você ganhou {tiers} nível(is).\n"
            "As recompensas são aplicadas automaticamente. Continue convidando!",
        "referral_remaining":
            "Convide <b>{remaining} amigo(s) a mais</b> que adicionem um monitor "
            "para desbloquear <b>+{bonus} vagas gratuitas</b>!",
        "referral_bonus_line":  "\n🎁 Bônus ganhos até agora: <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 Seu link de convite:\n<code>{ref_link}</code>\n\n"
            "Compartilhe com amigos — eles ganham UptimeGuard, "
            "você ganha +{bonus} vagas a cada {goal} que entrarem.",
        "tz_prompt_title":      "🌍 <b>Configuração rápida — defina seu fuso horário</b>\n\n",
        "tz_prompt_body":
            "Isso ajuda relatórios e alertas a chegarem no horário local correto.",
        "btn_set_tz":           "🌍 Definir meu fuso horário",
        "btn_skip_tz":          "⏭ Pular",
        "admin_new_user":
            "👤 <b>Novo usuário no UptimeGuard</b>\n\n"
            "Nome: <b>{full_name}</b>\n"
            "Usuário: {username}\n"
            "ID: <code>{user_id}</code>\n"
            "Idioma: <b>{lang}</b>\n"
            "Hora: {time}",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "welcome_greeting":     "👋 Привет, {name}! Добро пожаловать в <b>UptimeGuard</b>!\n\n",
        "welcome_back":         "👋 Привет, {name}! Рады видеть тебя снова!\n\n",
        "welcome_body":
            "Получай мгновенные уведомления в Telegram, как только сайт упадёт "
            "— раньше, чем это заметят пользователи.\n\n"
            "📦 {plan_text}\n\n"
            "{checklist}"
            "🎁 <b>Реферальная награда:</b> Пригласи {goal} друзей, которые добавят мониторинг "
            "→ получи <b>+{bonus} бесплатных слотов</b>!\n\n"
            "Твоя реферальная ссылка:\n<code>{ref_link}</code>",
        "plan_trial":           "✅ Пробный период Pro на 7 дней — все функции Pro доступны",
        "plan_free":            "🆓 Бесплатный план",
        "checklist":
            "📋 <b>С чего начать</b>\n"
            "✅ Присоединился к UptimeGuard\n"
            "⬜ Добавить первый монитор\n"
            "⬜ Получить первое уведомление\n\n",
        "btn_add_first":        "➕ Добавить первый монитор",
        "btn_how_it_works":     "📖 Как это работает",
        "btn_invite":           "👥 Пригласить друзей",
        "btn_add_monitor":      "➕ Добавить монитор",
        "btn_invite_earn":      "👥 Приглашай и зарабатывай",
        "btn_upgrade":          "⭐ Перейти на Pro",
        "btn_status":           "⚡ Статус",
        "btn_list":             "📋 Список",
        "btn_report":           "📊 Отчёт",
        "health_down":          "{count} монитор(ов) сейчас НЕДОСТУПНО ⚠️",
        "health_paused":        "Все мониторы на паузе",
        "health_ok":            "Все системы работают нормально",
        "plan_trial_label":     "✅ Pro (Пробный)",
        "plan_pro_label":       "✅ Pro",
        "plan_free_label":      "🆓 Бесплатный",
        "slots_line":           "\n📦 Мониторы: <b>{active}/{limit}</b>{bonus_str}",
        "slots_bonus_str":      " (+{bonus} реферальный бонус)",
        "referral_bar":         "\n👥 Рефералы: {bar}",
        "nudge_testalert":
            "\n\n💡 <i>Совет: запусти /testalert, чтобы убедиться, что уведомления доходят.</i>",
        "returning_header":
            "{icon} <b>UptimeGuard</b>\n\n"
            "📦 План: <b>{plan_label}</b>{slots_line}\n"
            "📡 Мониторы: <b>{total}</b> всего • "
            "<b>{up}</b> активных • "
            "<b>{down}</b> недоступных • "
            "<b>{paused}</b> на паузе\n\n"
            "Статус: <b>{health_text}</b>"
            "{referral_line}"
            "{nudge_line}",
        "how_it_works":
            "📖 <b>Как работает UptimeGuard</b>\n\n"
            "1️⃣ Добавь URL командой /add\n"
            "2️⃣ Проверяем каждые 5 мин (бесплатно) или 1 мин (Pro)\n"
            "3️⃣ Если сайт упал — мгновенное уведомление\n"
            "4️⃣ Когда восстановится — ещё одно уведомление\n\n"
            "<b>Pro также включает:</b>\n"
            "🔐 Предупреждения об истечении SSL\n"
            "🐢 Уведомления о медленном ответе\n"
            "📊 Еженедельные отчёты\n"
            "🔗 Интеграции через webhook\n"
            "👥 Уведомления для команды\n\n"
            "👇 Готов добавить первый монитор?",
        "referral_title":       "👥 <b>Реферальная программа</b>\n\n",
        "referral_progress":    "Прогресс до следующей награды: {bar}\n\n",
        "referral_reward_hit":
            "🎉 <b>Награда разблокирована!</b> Ты заработал {tiers} уровень(ней).\n"
            "Награды применяются автоматически. Продолжай приглашать!",
        "referral_remaining":
            "Пригласи ещё <b>{remaining} друга(ей)</b>, которые добавят монитор, "
            "чтобы получить <b>+{bonus} бесплатных слотов</b>!",
        "referral_bonus_line":  "\n🎁 Бонусных слотов получено: <b>+{bonus}</b>",
        "referral_link_line":
            "\n\n📎 Твоя реферальная ссылка:\n<code>{ref_link}</code>\n\n"
            "Поделись с друзьями — они получают UptimeGuard, "
            "ты получаешь +{bonus} слотов за каждых {goal} присоединившихся.",
        "tz_prompt_title":      "🌍 <b>Быстрая настройка — установи часовой пояс</b>\n\n",
        "tz_prompt_body":
            "Это поможет отчётам и уведомлениям приходить в правильное местное время.",
        "btn_set_tz":           "🌍 Установить часовой пояс",
        "btn_skip_tz":          "⏭ Пропустить",
        "admin_new_user":
            "👤 <b>Новый пользователь в UptimeGuard</b>\n\n"
            "Имя: <b>{full_name}</b>\n"
            "Имя пользователя: {username}\n"
            "ID: <code>{user_id}</code>\n"
            "Язык: <b>{lang}</b>\n"
            "Время: {time}",
    },
}

# Languages supported — anything else falls back to English
SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------

def resolve_lang(language_code: str | None) -> str:
    """
    Normalise a Telegram language_code to one we support.
    'en-GB' → 'en', 'zh-hans' → fallback 'en', None → 'en'.
    """
    if not language_code:
        return _FALLBACK
    base = language_code.split("-")[0].lower()
    return base if base in SUPPORTED_LANGS else _FALLBACK


def t(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in `lang` (falling back to English) and format with kwargs.

    Example:
        t("fr", "welcome_greeting", name="Alice")
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string
