# locales/payment_strings.py
"""
Translation strings for handlers/payments.py and handlers/referral.py.

Usage:
    from locales.payment_strings import pt_
    pt_("fr", "upgrade_header")
    pt_("es", "payment_success", plan_label="Mensual", expiry="1 mayo 2026")
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # ── payments.py — upgrade page ────────────────────────────────────
        "upgrade_header":
            "⭐ <b>Upgrade to UptimeGuard Pro</b>\n\n"
            "<b>What you unlock:</b>\n"
            "✅ Unlimited monitors\n"
            "✅ 1-minute check interval\n"
            "✅ SSL certificate expiry warnings\n"
            "✅ Slow response threshold alerts\n"
            "✅ Webhook integrations (Slack, PagerDuty)\n"
            "✅ Team notifications\n"
            "✅ Public status page\n"
            "✅ Weekly summary reports\n\n"
            "─────────────────────────\n"
            "📅 <b>Monthly</b>       {monthly} ⭐\n"
            "📆 <b>3 Months</b>    {three_month} ⭐  "
            "<i>save {save_3m} Stars</i>\n"
            "📆 <b>Yearly</b>       {yearly} ⭐  "
            "<i>save {save_yr} Stars</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>Not happy? Message us within 7 days for a full refund.</i>",
        "btn_monthly":          "📅 Monthly — {price} ⭐",
        "btn_3month":           "📆 3 Months — {price} ⭐  ✨ Recommended",
        "btn_yearly":           "📆 Yearly — {price} ⭐  🏆 Best Value",

        # ── payments.py — invoice strings (kept concise for Telegram UI) ──
        "invoice_title_monthly":        "UptimeGuard Pro — Monthly",
        "invoice_title_3month":         "UptimeGuard Pro — 3 Months",
        "invoice_title_yearly":         "UptimeGuard Pro — Yearly",
        "invoice_desc_monthly":
            "Unlimited monitors · 1-min checks · SSL alerts · Webhooks",
        "invoice_desc_3month":
            "Save {save} Stars vs monthly. "
            "Unlimited monitors · 1-min checks · SSL alerts · Webhooks",
        "invoice_desc_yearly":
            "Save {save} Stars vs monthly. "
            "Unlimited monitors · 1-min checks · SSL alerts · Webhooks",
        "invoice_error":
            "⚠️ Something went wrong sending the invoice.\n\n"
            "Please try again or contact support.",

        # ── payments.py — payment success ─────────────────────────────────
        "payment_success":
            "🎉 <b>Welcome to UptimeGuard Pro!</b>\n\n"
            "📦 Plan: <b>{plan_label}</b>\n"
            "📅 Access until: <b>{expiry}</b>\n\n"
            "<b>Now active:</b>\n"
            "⚡ Monitors check every minute\n"
            "🔐 SSL expiry warnings\n"
            "🐢 Slow response alerts\n"
            "🔗 Webhook integrations\n"
            "👥 Team notifications\n"
            "🌐 Public status page\n\n"
            "Use /add to add unlimited monitors.",
        "plan_label_monthly":   "Monthly",
        "plan_label_3month":    "3 Months",
        "plan_label_yearly":    "Yearly",

        # ── referral.py ───────────────────────────────────────────────────
        "referral_page":
            "👥 <b>Your Referral Link</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "Share this link. When someone signs up and adds their "
            "first monitor, it counts as a qualified referral.\n\n"
            "─────────────────────────\n"
            "📊 <b>Your Stats</b>\n"
            "─────────────────────────\n"
            "Total referrals:     <b>{total}</b>\n"
            "Rewards earned:      <b>{rewards}</b>\n\n"
            "Progress to next reward:\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>{remaining} more to go</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>Reward</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ You're on Pro — referrals extend your Pro access.\n"
            "Every <b>{goal} referrals</b> = extra days added.",
        "referral_reward_free":
            "🆓 You're on Free — referrals unlock extra monitor slots.\n"
            "Every <b>{goal} referrals</b> = "
            "+{bonus} monitor slot(s).\n"
            "Current limit: <b>{limit} monitors</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} bonus)",
        "btn_refresh":          "🔄 Refresh Stats",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "upgrade_header":
            "⭐ <b>Passer à UptimeGuard Pro</b>\n\n"
            "<b>Ce que tu débloque :</b>\n"
            "✅ Moniteurs illimités\n"
            "✅ Vérification toutes les minutes\n"
            "✅ Alertes d'expiration SSL\n"
            "✅ Alertes de réponse lente\n"
            "✅ Intégrations webhook (Slack, PagerDuty)\n"
            "✅ Notifications d'équipe\n"
            "✅ Page de statut publique\n"
            "✅ Rapports hebdomadaires\n\n"
            "─────────────────────────\n"
            "📅 <b>Mensuel</b>       {monthly} ⭐\n"
            "📆 <b>3 Mois</b>        {three_month} ⭐  "
            "<i>économise {save_3m} Stars</i>\n"
            "📆 <b>Annuel</b>         {yearly} ⭐  "
            "<i>économise {save_yr} Stars</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>Pas satisfait ? Contacte-nous sous 7 jours pour un remboursement complet.</i>",
        "btn_monthly":          "📅 Mensuel — {price} ⭐",
        "btn_3month":           "📆 3 Mois — {price} ⭐  ✨ Recommandé",
        "btn_yearly":           "📆 Annuel — {price} ⭐  🏆 Meilleur rapport",
        "invoice_title_monthly":        "UptimeGuard Pro — Mensuel",
        "invoice_title_3month":         "UptimeGuard Pro — 3 Mois",
        "invoice_title_yearly":         "UptimeGuard Pro — Annuel",
        "invoice_desc_monthly":
            "Moniteurs illimités · Vérif. 1 min · Alertes SSL · Webhooks",
        "invoice_desc_3month":
            "Économise {save} Stars vs mensuel. "
            "Moniteurs illimités · Vérif. 1 min · Alertes SSL · Webhooks",
        "invoice_desc_yearly":
            "Économise {save} Stars vs mensuel. "
            "Moniteurs illimités · Vérif. 1 min · Alertes SSL · Webhooks",
        "invoice_error":
            "⚠️ Une erreur s'est produite lors de l'envoi de la facture.\n\n"
            "Réessaie ou contacte le support.",
        "payment_success":
            "🎉 <b>Bienvenue sur UptimeGuard Pro !</b>\n\n"
            "📦 Plan : <b>{plan_label}</b>\n"
            "📅 Accès jusqu'au : <b>{expiry}</b>\n\n"
            "<b>Maintenant actif :</b>\n"
            "⚡ Vérification toutes les minutes\n"
            "🔐 Alertes d'expiration SSL\n"
            "🐢 Alertes de réponse lente\n"
            "🔗 Intégrations webhook\n"
            "👥 Notifications d'équipe\n"
            "🌐 Page de statut publique\n\n"
            "Utilise /add pour ajouter des moniteurs illimités.",
        "plan_label_monthly":   "Mensuel",
        "plan_label_3month":    "3 Mois",
        "plan_label_yearly":    "Annuel",
        "referral_page":
            "👥 <b>Ton lien de parrainage</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "Partage ce lien. Quand quelqu'un s'inscrit et ajoute son "
            "premier moniteur, ça compte comme un parrainage qualifié.\n\n"
            "─────────────────────────\n"
            "📊 <b>Tes statistiques</b>\n"
            "─────────────────────────\n"
            "Total parrainages :     <b>{total}</b>\n"
            "Récompenses gagnées : <b>{rewards}</b>\n\n"
            "Progression vers la prochaine récompense :\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>Encore {remaining} à inviter</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>Récompense</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ Tu es sur Pro — les parrainages prolongent ton accès Pro.\n"
            "Tous les <b>{goal} parrainages</b> = jours supplémentaires ajoutés.",
        "referral_reward_free":
            "🆓 Tu es sur Gratuit — les parrainages débloquent des emplacements.\n"
            "Tous les <b>{goal} parrainages</b> = "
            "+{bonus} emplacement(s).\n"
            "Limite actuelle : <b>{limit} moniteurs</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} bonus)",
        "btn_refresh":          "🔄 Actualiser les stats",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "upgrade_header":
            "⭐ <b>Actualizar a UptimeGuard Pro</b>\n\n"
            "<b>Lo que desbloqueas:</b>\n"
            "✅ Monitores ilimitados\n"
            "✅ Verificación cada minuto\n"
            "✅ Alertas de expiración SSL\n"
            "✅ Alertas de respuesta lenta\n"
            "✅ Integraciones webhook (Slack, PagerDuty)\n"
            "✅ Notificaciones de equipo\n"
            "✅ Página de estado pública\n"
            "✅ Informes semanales\n\n"
            "─────────────────────────\n"
            "📅 <b>Mensual</b>       {monthly} ⭐\n"
            "📆 <b>3 Meses</b>     {three_month} ⭐  "
            "<i>ahorra {save_3m} Stars</i>\n"
            "📆 <b>Anual</b>         {yearly} ⭐  "
            "<i>ahorra {save_yr} Stars</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>¿No estás satisfecho? Escríbenos en 7 días para un reembolso completo.</i>",
        "btn_monthly":          "📅 Mensual — {price} ⭐",
        "btn_3month":           "📆 3 Meses — {price} ⭐  ✨ Recomendado",
        "btn_yearly":           "📆 Anual — {price} ⭐  🏆 Mejor valor",
        "invoice_title_monthly":        "UptimeGuard Pro — Mensual",
        "invoice_title_3month":         "UptimeGuard Pro — 3 Meses",
        "invoice_title_yearly":         "UptimeGuard Pro — Anual",
        "invoice_desc_monthly":
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_desc_3month":
            "Ahorra {save} Stars vs mensual. "
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_desc_yearly":
            "Ahorra {save} Stars vs mensual. "
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_error":
            "⚠️ Algo salió mal al enviar la factura.\n\n"
            "Intenta de nuevo o contacta al soporte.",
        "payment_success":
            "🎉 <b>¡Bienvenido a UptimeGuard Pro!</b>\n\n"
            "📦 Plan: <b>{plan_label}</b>\n"
            "📅 Acceso hasta: <b>{expiry}</b>\n\n"
            "<b>Ahora activo:</b>\n"
            "⚡ Verificación cada minuto\n"
            "🔐 Alertas de expiración SSL\n"
            "🐢 Alertas de respuesta lenta\n"
            "🔗 Integraciones webhook\n"
            "👥 Notificaciones de equipo\n"
            "🌐 Página de estado pública\n\n"
            "Usa /add para añadir monitores ilimitados.",
        "plan_label_monthly":   "Mensual",
        "plan_label_3month":    "3 Meses",
        "plan_label_yearly":    "Anual",
        "referral_page":
            "👥 <b>Tu enlace de referido</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "Comparte este enlace. Cuando alguien se registra y añade su "
            "primer monitor, cuenta como referido cualificado.\n\n"
            "─────────────────────────\n"
            "📊 <b>Tus estadísticas</b>\n"
            "─────────────────────────\n"
            "Total referidos:     <b>{total}</b>\n"
            "Recompensas ganadas: <b>{rewards}</b>\n\n"
            "Progreso hacia la próxima recompensa:\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>Faltan {remaining} más</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>Recompensa</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ Estás en Pro — los referidos extienden tu acceso Pro.\n"
            "Cada <b>{goal} referidos</b> = días adicionales añadidos.",
        "referral_reward_free":
            "🆓 Estás en Gratis — los referidos desbloquean espacios de monitor.\n"
            "Cada <b>{goal} referidos</b> = "
            "+{bonus} espacio(s).\n"
            "Límite actual: <b>{limit} monitores</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} bonus)",
        "btn_refresh":          "🔄 Actualizar estadísticas",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "upgrade_header":
            "⭐ <b>الترقية إلى UptimeGuard Pro</b>\n\n"
            "<b>ما الذي تفتحه:</b>\n"
            "✅ مراقبون غير محدودون\n"
            "✅ فحص كل دقيقة\n"
            "✅ تحذيرات انتهاء SSL\n"
            "✅ تنبيهات الاستجابة البطيئة\n"
            "✅ تكاملات Webhook (Slack, PagerDuty)\n"
            "✅ إشعارات الفريق\n"
            "✅ صفحة حالة عامة\n"
            "✅ تقارير أسبوعية\n\n"
            "─────────────────────────\n"
            "📅 <b>شهري</b>       {monthly} ⭐\n"
            "📆 <b>3 أشهر</b>    {three_month} ⭐  "
            "<i>وفّر {save_3m} نجمة</i>\n"
            "📆 <b>سنوي</b>       {yearly} ⭐  "
            "<i>وفّر {save_yr} نجمة</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>غير راضٍ؟ راسلنا خلال 7 أيام لاسترداد كامل.</i>",
        "btn_monthly":          "📅 شهري — {price} ⭐",
        "btn_3month":           "📆 3 أشهر — {price} ⭐  ✨ موصى به",
        "btn_yearly":           "📆 سنوي — {price} ⭐  🏆 الأفضل قيمة",
        "invoice_title_monthly":        "UptimeGuard Pro — شهري",
        "invoice_title_3month":         "UptimeGuard Pro — 3 أشهر",
        "invoice_title_yearly":         "UptimeGuard Pro — سنوي",
        "invoice_desc_monthly":
            "مراقبون غير محدودون · فحص 1 دقيقة · تنبيهات SSL · Webhooks",
        "invoice_desc_3month":
            "وفّر {save} نجمة مقارنة بالشهري. "
            "مراقبون غير محدودون · فحص 1 دقيقة · تنبيهات SSL · Webhooks",
        "invoice_desc_yearly":
            "وفّر {save} نجمة مقارنة بالشهري. "
            "مراقبون غير محدودون · فحص 1 دقيقة · تنبيهات SSL · Webhooks",
        "invoice_error":
            "⚠️ حدث خطأ أثناء إرسال الفاتورة.\n\n"
            "حاول مجدداً أو تواصل مع الدعم.",
        "payment_success":
            "🎉 <b>مرحباً بك في UptimeGuard Pro!</b>\n\n"
            "📦 الخطة: <b>{plan_label}</b>\n"
            "📅 الوصول حتى: <b>{expiry}</b>\n\n"
            "<b>نشط الآن:</b>\n"
            "⚡ الفحص كل دقيقة\n"
            "🔐 تحذيرات انتهاء SSL\n"
            "🐢 تنبيهات الاستجابة البطيئة\n"
            "🔗 تكاملات Webhook\n"
            "👥 إشعارات الفريق\n"
            "🌐 صفحة الحالة العامة\n\n"
            "استخدم /add لإضافة مراقبين غير محدودين.",
        "plan_label_monthly":   "شهري",
        "plan_label_3month":    "3 أشهر",
        "plan_label_yearly":    "سنوي",
        "referral_page":
            "👥 <b>رابط إحالتك</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "شارك هذا الرابط. عندما يسجّل أحدهم ويضيف "
            "مراقبه الأول، يُحتسب كإحالة مؤهلة.\n\n"
            "─────────────────────────\n"
            "📊 <b>إحصائياتك</b>\n"
            "─────────────────────────\n"
            "إجمالي الإحالات:     <b>{total}</b>\n"
            "المكافآت المكتسبة:  <b>{rewards}</b>\n\n"
            "التقدم نحو المكافأة التالية:\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>تبقّى {remaining} إحالة</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>المكافأة</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ أنت على Pro — الإحالات تمدّد وصولك إلى Pro.\n"
            "كل <b>{goal} إحالات</b> = أيام إضافية تُضاف.",
        "referral_reward_free":
            "🆓 أنت على المجاني — الإحالات تفتح فتحات مراقبة إضافية.\n"
            "كل <b>{goal} إحالات</b> = "
            "+{bonus} فتحة.\n"
            "الحد الحالي: <b>{limit} مراقب</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} مكافأة)",
        "btn_refresh":          "🔄 تحديث الإحصائيات",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "upgrade_header":
            "⭐ <b>Atualizar para UptimeGuard Pro</b>\n\n"
            "<b>O que você desbloqueia:</b>\n"
            "✅ Monitores ilimitados\n"
            "✅ Verificação a cada minuto\n"
            "✅ Alertas de expiração SSL\n"
            "✅ Alertas de resposta lenta\n"
            "✅ Integrações webhook (Slack, PagerDuty)\n"
            "✅ Notificações de equipe\n"
            "✅ Página de status pública\n"
            "✅ Relatórios semanais\n\n"
            "─────────────────────────\n"
            "📅 <b>Mensal</b>       {monthly} ⭐\n"
            "📆 <b>3 Meses</b>    {three_month} ⭐  "
            "<i>economize {save_3m} Stars</i>\n"
            "📆 <b>Anual</b>         {yearly} ⭐  "
            "<i>economize {save_yr} Stars</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>Não satisfeito? Nos contate em 7 dias para reembolso completo.</i>",
        "btn_monthly":          "📅 Mensal — {price} ⭐",
        "btn_3month":           "📆 3 Meses — {price} ⭐  ✨ Recomendado",
        "btn_yearly":           "📆 Anual — {price} ⭐  🏆 Melhor custo-benefício",
        "invoice_title_monthly":        "UptimeGuard Pro — Mensal",
        "invoice_title_3month":         "UptimeGuard Pro — 3 Meses",
        "invoice_title_yearly":         "UptimeGuard Pro — Anual",
        "invoice_desc_monthly":
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_desc_3month":
            "Economize {save} Stars vs mensal. "
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_desc_yearly":
            "Economize {save} Stars vs mensal. "
            "Monitores ilimitados · Verif. 1 min · Alertas SSL · Webhooks",
        "invoice_error":
            "⚠️ Algo deu errado ao enviar a fatura.\n\n"
            "Tente novamente ou entre em contato com o suporte.",
        "payment_success":
            "🎉 <b>Bem-vindo ao UptimeGuard Pro!</b>\n\n"
            "📦 Plano: <b>{plan_label}</b>\n"
            "📅 Acesso até: <b>{expiry}</b>\n\n"
            "<b>Agora ativo:</b>\n"
            "⚡ Verificação a cada minuto\n"
            "🔐 Alertas de expiração SSL\n"
            "🐢 Alertas de resposta lenta\n"
            "🔗 Integrações webhook\n"
            "👥 Notificações de equipe\n"
            "🌐 Página de status pública\n\n"
            "Use /add para adicionar monitores ilimitados.",
        "plan_label_monthly":   "Mensal",
        "plan_label_3month":    "3 Meses",
        "plan_label_yearly":    "Anual",
        "referral_page":
            "👥 <b>Seu link de indicação</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "Compartilhe este link. Quando alguém se cadastrar e adicionar seu "
            "primeiro monitor, conta como indicação qualificada.\n\n"
            "─────────────────────────\n"
            "📊 <b>Suas estatísticas</b>\n"
            "─────────────────────────\n"
            "Total de indicações:     <b>{total}</b>\n"
            "Recompensas ganhas:      <b>{rewards}</b>\n\n"
            "Progresso para a próxima recompensa:\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>Faltam {remaining} mais</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>Recompensa</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ Você está no Pro — as indicações estendem seu acesso Pro.\n"
            "A cada <b>{goal} indicações</b> = dias extras adicionados.",
        "referral_reward_free":
            "🆓 Você está no Gratuito — as indicações desbloqueiam slots de monitor.\n"
            "A cada <b>{goal} indicações</b> = "
            "+{bonus} slot(s).\n"
            "Limite atual: <b>{limit} monitores</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} bônus)",
        "btn_refresh":          "🔄 Atualizar estatísticas",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "upgrade_header":
            "⭐ <b>Перейти на UptimeGuard Pro</b>\n\n"
            "<b>Что ты получаешь:</b>\n"
            "✅ Неограниченное количество мониторов\n"
            "✅ Проверка каждую минуту\n"
            "✅ Предупреждения об истечении SSL\n"
            "✅ Уведомления о медленном ответе\n"
            "✅ Интеграции webhook (Slack, PagerDuty)\n"
            "✅ Командные уведомления\n"
            "✅ Публичная страница статуса\n"
            "✅ Еженедельные отчёты\n\n"
            "─────────────────────────\n"
            "📅 <b>Ежемесячно</b>    {monthly} ⭐\n"
            "📆 <b>3 Месяца</b>      {three_month} ⭐  "
            "<i>экономия {save_3m} Stars</i>\n"
            "📆 <b>Ежегодно</b>      {yearly} ⭐  "
            "<i>экономия {save_yr} Stars</i>\n"
            "─────────────────────────\n\n"
            "💬 <i>Не доволен? Напиши нам в течение 7 дней — полный возврат.</i>",
        "btn_monthly":          "📅 Ежемесячно — {price} ⭐",
        "btn_3month":           "📆 3 Месяца — {price} ⭐  ✨ Рекомендуем",
        "btn_yearly":           "📆 Ежегодно — {price} ⭐  🏆 Лучшая цена",
        "invoice_title_monthly":        "UptimeGuard Pro — Ежемесячно",
        "invoice_title_3month":         "UptimeGuard Pro — 3 Месяца",
        "invoice_title_yearly":         "UptimeGuard Pro — Ежегодно",
        "invoice_desc_monthly":
            "Без лимита мониторов · Проверка 1 мин · SSL · Webhooks",
        "invoice_desc_3month":
            "Экономия {save} Stars vs ежемесячно. "
            "Без лимита мониторов · Проверка 1 мин · SSL · Webhooks",
        "invoice_desc_yearly":
            "Экономия {save} Stars vs ежемесячно. "
            "Без лимита мониторов · Проверка 1 мин · SSL · Webhooks",
        "invoice_error":
            "⚠️ Что-то пошло не так при отправке счёта.\n\n"
            "Попробуй снова или обратись в поддержку.",
        "payment_success":
            "🎉 <b>Добро пожаловать в UptimeGuard Pro!</b>\n\n"
            "📦 Тариф: <b>{plan_label}</b>\n"
            "📅 Доступ до: <b>{expiry}</b>\n\n"
            "<b>Теперь активно:</b>\n"
            "⚡ Проверка каждую минуту\n"
            "🔐 Предупреждения об истечении SSL\n"
            "🐢 Уведомления о медленном ответе\n"
            "🔗 Интеграции webhook\n"
            "👥 Командные уведомления\n"
            "🌐 Публичная страница статуса\n\n"
            "Используй /add для добавления неограниченного числа мониторов.",
        "plan_label_monthly":   "Ежемесячно",
        "plan_label_3month":    "3 Месяца",
        "plan_label_yearly":    "Ежегодно",
        "referral_page":
            "👥 <b>Твоя реферальная ссылка</b>\n\n"
            "<code>{ref_link}</code>\n\n"
            "Поделись этой ссылкой. Когда кто-то зарегистрируется и добавит "
            "первый монитор — это засчитается как квалифицированный реферал.\n\n"
            "─────────────────────────\n"
            "📊 <b>Твоя статистика</b>\n"
            "─────────────────────────\n"
            "Всего рефералов:       <b>{total}</b>\n"
            "Наград получено:       <b>{rewards}</b>\n\n"
            "Прогресс до следующей награды:\n"
            "{bar} <b>{progress}/{goal}</b>\n"
            "<i>Ещё {remaining} до цели</i>\n\n"
            "─────────────────────────\n"
            "🎁 <b>Награда</b>\n"
            "─────────────────────────\n"
            "{reward_text}",
        "referral_reward_pro":
            "⭐ Ты на Pro — рефералы продлевают твой доступ.\n"
            "Каждые <b>{goal} реферала</b> = дополнительные дни.",
        "referral_reward_free":
            "🆓 Ты на бесплатном — рефералы открывают слоты для мониторов.\n"
            "Каждые <b>{goal} реферала</b> = "
            "+{bonus} слот(а).\n"
            "Текущий лимит: <b>{limit} мониторов</b>{bonus_str}.",
        "referral_bonus_str":   " (+{bonus} бонус)",
        "btn_refresh":          "🔄 Обновить статистику",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


def pt_(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in payment/referral locale for `lang`, falling back to English.

    Named pt_() to avoid collision with the 'pt' language code variable.

    Usage:
        from locales.payment_strings import pt_
        pt_("fr", "upgrade_header", monthly=250, three_month=600,
            yearly=2000, save_3m=150, save_yr=1000)
        pt_("ru", "payment_success", plan_label="Ежемесячно", expiry="1 мая 2026")
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string
    
    