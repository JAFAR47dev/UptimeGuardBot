# locales/team_strings.py
"""
Translation strings for handlers/statuspage.py and handlers/team.py.

Usage:
    from locales.team_strings import tt
    tt("fr", "sp_created", url="https://...", pro_extras="...")
    tt("es", "team_step1_prompt")
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # ── statuspage.py ─────────────────────────────────────────────────
        "sp_no_page_to_delete":
            "You don't have a status page to delete.",
        "sp_deleted":
            "🗑 <b>Status page deleted.</b>\n\n"
            "The URL is now inactive. Use /statuspage to create a new one.",
        "sp_title_pro_gate":
            "🔒 <b>Custom titles are a Pro feature.</b>\n\n"
            "Upgrade to set a custom title and remove the "
            "'Powered by UptimeGuard' footer.",
        "sp_btn_upgrade":           "⭐ Upgrade to Pro",
        "sp_no_page_for_title":
            "You don't have a status page yet. "
            "Run /statuspage first to create one, then set a title.",
        "sp_ask_title":
            "✏️ Send me the new title for your status page.\n\n"
            "Example: <code>Acme Corp — Service Status</code>\n\n"
            "Send /cancel to abort.",
        "sp_title_too_long":
            "⚠️ Title must be 80 characters or less. Try a shorter one:",
        "sp_title_updated":
            "✅ <b>Title updated!</b>\n\n"
            "🏷 New title: <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 Open Status Page",
        "sp_cancelled":             "❌ Cancelled.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro:</b> branding removed, custom title active.",
        "sp_existing_free":
            "\n\n🆓 <b>Free plan:</b> 'Powered by UptimeGuard' footer shown.\n"
            "Upgrade to Pro to remove branding and set a custom title.",
        "sp_existing_page":
            "📡 <b>Your Status Page</b>\n\n"
            "🏷 Title: <b>{title}</b>\n"
            "🔗 URL:\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>Commands:</b>\n"
            "/statuspage delete — remove your page\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — change the title\n",
        "sp_created_pro_extras":
            "\n✅ Branding removed — your page looks fully custom.\n"
            "Use /statuspage title to set a custom title.",
        "sp_created_free_extras":
            "\n🆓 Free plan: 'Powered by UptimeGuard' footer is shown.\n"
            "Upgrade to Pro to remove it and set a custom title.",
        "sp_created":
            "✅ <b>Status page created!</b>\n\n"
            "🔗 Share this URL with your clients:\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "The page updates live and auto-refreshes every 60 seconds.",
        "sp_callback_pro_line":
            "✅ Pro: no branding, custom title via /statuspage title",
        "sp_callback_free_line":
            "🆓 Free: 'Powered by UptimeGuard' footer shown.",
        "sp_callback_ready":
            "✅ <b>Status page ready!</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",

        # ── team.py ───────────────────────────────────────────────────────
        "team_pro_gate":
            "👥 <b>Team Notifications</b>\n\n"
            "Team notifications are a <b>Pro</b> feature.\n\n"
            "Upgrade to add up to {limit} teammates who receive the same "
            "down and recovery alerts as you.",
        "team_btn_upgrade":         "⭐ Upgrade to Pro",
        "team_empty":
            "👥 <b>Team Notifications</b>\n\n"
            "You have no teammates yet. You can add up to {limit}.\n\n"
            "Teammates receive the same down and recovery alerts as you, "
            "directly in their Telegram DMs.\n\n"
            "⚠️ <b>Important:</b> each teammate must send <code>/start</code> "
            "to this bot before they can receive alerts.",
        "team_btn_add":             "➕ Add Teammate",
        "team_list_header":
            "👥 <b>Team Notifications</b>\n\n"
            "<b>{count}/{limit}</b> teammate{plural} added.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — ID: <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>Reminder:</b> teammates must send <code>/start</code> "
            "to this bot to receive alerts.",
        "team_btn_remove":          "🗑 Remove {display}",
        "team_add_pro_gate":        "⭐ Team notifications are a Pro feature.",
        "team_limit_reached":
            "⚠️ You've reached the limit of {limit} teammates.\n\n"
            "Remove an existing teammate before adding a new one.",
        "team_step1_prompt":
            "👥 <b>Add Teammate — Step 1 of 2</b>\n\n"
            "Send your teammate's <b>Telegram user ID</b>.\n\n"
            "They can find their ID by messaging "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ They must also send <code>/start</code> to this bot first, "
            "otherwise Telegram will block the alert delivery.\n\n"
            "Send /cancel to abort.",
        "team_id_invalid":
            "⚠️ Please send a numeric Telegram user ID.\n\n"
            "Example: <code>123456789</code>\n\n"
            "Your teammate can find their ID via "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ You can't add yourself as a teammate.",
        "team_id_duplicate":
            "⚠️ User <code>{member_id}</code> is already on your team.",
        "team_id_ok":
            "✅ User ID <code>{member_id}</code> noted.\n\n"
            "👥 <b>Step 2 of 2</b> — Give them a label so you know who they are.\n\n"
            "Example: <i>John</i> or <i>DevOps Lead</i>\n\n"
            "Send /skip to use their user ID as the label, or /cancel to abort.",
        "team_label_too_long":
            "⚠️ Label must be 50 characters or less. Try a shorter one:",
        "team_something_wrong":
            "Something went wrong. Use /team add to try again.",
        "team_already_member":
            "⚠️ User <code>{member_id}</code> is already on your team.",
        "team_saved":
            "✅ <b>{display}</b> added to your team!\n\n"
            "👤 ID: <code>{member_id}</code>\n\n"
            "They will now receive the same down and recovery alerts as you.\n\n"
            "⚠️ Make sure they've sent <code>/start</code> to this bot, "
            "otherwise Telegram will block the delivery.",
        "team_remove_confirm":
            "⚠️ Remove <b>{display}</b> from your team?\n\n"
            "They will stop receiving alerts immediately.",
        "team_remove_not_found":    "Teammate not found.",
        "team_btn_yes_remove":      "✅ Yes, remove",
        "team_btn_cancel":          "❌ Cancel",
        "team_removed":
            "🗑 <b>{display}</b> removed from your team.\n\n"
            "Use /team to manage your teammates.",
        "team_remove_cancelled":    "❌ Cancelled. Teammate is still active.",
        "team_cancelled":           "❌ Cancelled.",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "sp_no_page_to_delete":
            "Tu n'as pas de page de statut à supprimer.",
        "sp_deleted":
            "🗑 <b>Page de statut supprimée.</b>\n\n"
            "L'URL est maintenant inactive. Utilise /statuspage pour en créer une nouvelle.",
        "sp_title_pro_gate":
            "🔒 <b>Les titres personnalisés sont une fonctionnalité Pro.</b>\n\n"
            "Passe à Pro pour définir un titre et supprimer le "
            "pied de page 'Powered by UptimeGuard'.",
        "sp_btn_upgrade":           "⭐ Passer à Pro",
        "sp_no_page_for_title":
            "Tu n'as pas encore de page de statut. "
            "Lance /statuspage pour en créer une, puis définis un titre.",
        "sp_ask_title":
            "✏️ Envoie-moi le nouveau titre de ta page de statut.\n\n"
            "Exemple : <code>Acme Corp — État des services</code>\n\n"
            "Envoie /cancel pour annuler.",
        "sp_title_too_long":
            "⚠️ Le titre doit faire 80 caractères ou moins. Essaie un titre plus court :",
        "sp_title_updated":
            "✅ <b>Titre mis à jour !</b>\n\n"
            "🏷 Nouveau titre : <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 Ouvrir la page de statut",
        "sp_cancelled":             "❌ Annulé.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro :</b> sans branding, titre personnalisé actif.",
        "sp_existing_free":
            "\n\n🆓 <b>Plan gratuit :</b> pied de page 'Powered by UptimeGuard' affiché.\n"
            "Passe à Pro pour supprimer le branding et définir un titre.",
        "sp_existing_page":
            "📡 <b>Ta page de statut</b>\n\n"
            "🏷 Titre : <b>{title}</b>\n"
            "🔗 URL :\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>Commandes :</b>\n"
            "/statuspage delete — supprimer ta page\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — changer le titre\n",
        "sp_created_pro_extras":
            "\n✅ Sans branding — ta page est entièrement personnalisée.\n"
            "Utilise /statuspage title pour définir un titre.",
        "sp_created_free_extras":
            "\n🆓 Plan gratuit : le pied de page 'Powered by UptimeGuard' est affiché.\n"
            "Passe à Pro pour le supprimer et définir un titre.",
        "sp_created":
            "✅ <b>Page de statut créée !</b>\n\n"
            "🔗 Partage cette URL avec tes clients :\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "La page se met à jour en direct et s'actualise toutes les 60 secondes.",
        "sp_callback_pro_line":
            "✅ Pro : sans branding, titre personnalisé via /statuspage title",
        "sp_callback_free_line":
            "🆓 Gratuit : pied de page 'Powered by UptimeGuard' affiché.",
        "sp_callback_ready":
            "✅ <b>Page de statut prête !</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",
        "team_pro_gate":
            "👥 <b>Notifications d'équipe</b>\n\n"
            "Les notifications d'équipe sont une fonctionnalité <b>Pro</b>.\n\n"
            "Passe à Pro pour ajouter jusqu'à {limit} coéquipiers qui reçoivent "
            "les mêmes alertes que toi.",
        "team_btn_upgrade":         "⭐ Passer à Pro",
        "team_empty":
            "👥 <b>Notifications d'équipe</b>\n\n"
            "Tu n'as pas encore de coéquipiers. Tu peux en ajouter jusqu'à {limit}.\n\n"
            "Les coéquipiers reçoivent les mêmes alertes de panne et de récupération, "
            "directement dans leurs DM Telegram.\n\n"
            "⚠️ <b>Important :</b> chaque coéquipier doit envoyer <code>/start</code> "
            "à ce bot avant de pouvoir recevoir des alertes.",
        "team_btn_add":             "➕ Ajouter un coéquipier",
        "team_list_header":
            "👥 <b>Notifications d'équipe</b>\n\n"
            "<b>{count}/{limit}</b> coéquipier{plural} ajouté{plural}.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — ID : <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>Rappel :</b> les coéquipiers doivent envoyer <code>/start</code> "
            "à ce bot pour recevoir des alertes.",
        "team_btn_remove":          "🗑 Retirer {display}",
        "team_add_pro_gate":        "⭐ Les notifications d'équipe sont une fonctionnalité Pro.",
        "team_limit_reached":
            "⚠️ Tu as atteint la limite de {limit} coéquipiers.\n\n"
            "Retire un coéquipier existant avant d'en ajouter un nouveau.",
        "team_step1_prompt":
            "👥 <b>Ajouter un coéquipier — Étape 1 sur 2</b>\n\n"
            "Envoie l'<b>ID Telegram</b> de ton coéquipier.\n\n"
            "Il peut trouver son ID en contactant "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ Il doit aussi envoyer <code>/start</code> à ce bot d'abord, "
            "sinon Telegram bloquera la livraison des alertes.\n\n"
            "Envoie /cancel pour annuler.",
        "team_id_invalid":
            "⚠️ Envoie un ID Telegram numérique.\n\n"
            "Exemple : <code>123456789</code>\n\n"
            "Ton coéquipier peut trouver son ID via "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ Tu ne peux pas t'ajouter toi-même comme coéquipier.",
        "team_id_duplicate":
            "⚠️ L'utilisateur <code>{member_id}</code> est déjà dans ton équipe.",
        "team_id_ok":
            "✅ ID <code>{member_id}</code> noté.\n\n"
            "👥 <b>Étape 2 sur 2</b> — Donne-lui un nom pour l'identifier.\n\n"
            "Exemple : <i>Jean</i> ou <i>Lead DevOps</i>\n\n"
            "Envoie /skip pour utiliser son ID comme nom, ou /cancel pour annuler.",
        "team_label_too_long":
            "⚠️ Le nom doit faire 50 caractères ou moins. Essaie un nom plus court :",
        "team_something_wrong":
            "Une erreur s'est produite. Utilise /team add pour réessayer.",
        "team_already_member":
            "⚠️ L'utilisateur <code>{member_id}</code> est déjà dans ton équipe.",
        "team_saved":
            "✅ <b>{display}</b> ajouté à ton équipe !\n\n"
            "👤 ID : <code>{member_id}</code>\n\n"
            "Il recevra désormais les mêmes alertes que toi.\n\n"
            "⚠️ Assure-toi qu'il a envoyé <code>/start</code> à ce bot, "
            "sinon Telegram bloquera la livraison.",
        "team_remove_confirm":
            "⚠️ Retirer <b>{display}</b> de ton équipe ?\n\n"
            "Il ne recevra plus d'alertes immédiatement.",
        "team_remove_not_found":    "Coéquipier introuvable.",
        "team_btn_yes_remove":      "✅ Oui, retirer",
        "team_btn_cancel":          "❌ Annuler",
        "team_removed":
            "🗑 <b>{display}</b> retiré de ton équipe.\n\n"
            "Utilise /team pour gérer tes coéquipiers.",
        "team_remove_cancelled":    "❌ Annulé. Le coéquipier est toujours actif.",
        "team_cancelled":           "❌ Annulé.",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "sp_no_page_to_delete":
            "No tienes una página de estado que eliminar.",
        "sp_deleted":
            "🗑 <b>Página de estado eliminada.</b>\n\n"
            "La URL ya no está activa. Usa /statuspage para crear una nueva.",
        "sp_title_pro_gate":
            "🔒 <b>Los títulos personalizados son una función Pro.</b>\n\n"
            "Actualiza para establecer un título personalizado y eliminar el "
            "pie de página 'Powered by UptimeGuard'.",
        "sp_btn_upgrade":           "⭐ Actualizar a Pro",
        "sp_no_page_for_title":
            "Aún no tienes una página de estado. "
            "Ejecuta /statuspage para crear una, luego establece un título.",
        "sp_ask_title":
            "✏️ Envíame el nuevo título para tu página de estado.\n\n"
            "Ejemplo: <code>Acme Corp — Estado del servicio</code>\n\n"
            "Envía /cancel para cancelar.",
        "sp_title_too_long":
            "⚠️ El título debe tener 80 caracteres o menos. Prueba uno más corto:",
        "sp_title_updated":
            "✅ <b>¡Título actualizado!</b>\n\n"
            "🏷 Nuevo título: <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 Abrir página de estado",
        "sp_cancelled":             "❌ Cancelado.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro:</b> sin branding, título personalizado activo.",
        "sp_existing_free":
            "\n\n🆓 <b>Plan gratuito:</b> pie de página 'Powered by UptimeGuard' visible.\n"
            "Actualiza a Pro para eliminar el branding y establecer un título.",
        "sp_existing_page":
            "📡 <b>Tu página de estado</b>\n\n"
            "🏷 Título: <b>{title}</b>\n"
            "🔗 URL:\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>Comandos:</b>\n"
            "/statuspage delete — eliminar tu página\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — cambiar el título\n",
        "sp_created_pro_extras":
            "\n✅ Sin branding — tu página se ve completamente personalizada.\n"
            "Usa /statuspage title para establecer un título.",
        "sp_created_free_extras":
            "\n🆓 Plan gratuito: se muestra el pie de página 'Powered by UptimeGuard'.\n"
            "Actualiza a Pro para eliminarlo y establecer un título.",
        "sp_created":
            "✅ <b>¡Página de estado creada!</b>\n\n"
            "🔗 Comparte esta URL con tus clientes:\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "La página se actualiza en vivo y se refresca cada 60 segundos.",
        "sp_callback_pro_line":
            "✅ Pro: sin branding, título personalizado via /statuspage title",
        "sp_callback_free_line":
            "🆓 Gratis: pie de página 'Powered by UptimeGuard' visible.",
        "sp_callback_ready":
            "✅ <b>¡Página de estado lista!</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",
        "team_pro_gate":
            "👥 <b>Notificaciones de equipo</b>\n\n"
            "Las notificaciones de equipo son una función <b>Pro</b>.\n\n"
            "Actualiza para añadir hasta {limit} compañeros que reciban "
            "las mismas alertas que tú.",
        "team_btn_upgrade":         "⭐ Actualizar a Pro",
        "team_empty":
            "👥 <b>Notificaciones de equipo</b>\n\n"
            "Aún no tienes compañeros. Puedes añadir hasta {limit}.\n\n"
            "Los compañeros reciben las mismas alertas de caída y recuperación, "
            "directamente en sus DMs de Telegram.\n\n"
            "⚠️ <b>Importante:</b> cada compañero debe enviar <code>/start</code> "
            "a este bot antes de poder recibir alertas.",
        "team_btn_add":             "➕ Añadir compañero",
        "team_list_header":
            "👥 <b>Notificaciones de equipo</b>\n\n"
            "<b>{count}/{limit}</b> compañero{plural} añadido{plural}.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — ID: <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>Recordatorio:</b> los compañeros deben enviar <code>/start</code> "
            "a este bot para recibir alertas.",
        "team_btn_remove":          "🗑 Eliminar {display}",
        "team_add_pro_gate":        "⭐ Las notificaciones de equipo son una función Pro.",
        "team_limit_reached":
            "⚠️ Has alcanzado el límite de {limit} compañeros.\n\n"
            "Elimina uno antes de añadir otro.",
        "team_step1_prompt":
            "👥 <b>Añadir compañero — Paso 1 de 2</b>\n\n"
            "Envía el <b>ID de Telegram</b> de tu compañero.\n\n"
            "Puede encontrar su ID contactando a "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ También debe enviar <code>/start</code> a este bot primero, "
            "de lo contrario Telegram bloqueará la entrega de alertas.\n\n"
            "Envía /cancel para cancelar.",
        "team_id_invalid":
            "⚠️ Envía un ID de Telegram numérico.\n\n"
            "Ejemplo: <code>123456789</code>\n\n"
            "Tu compañero puede encontrar su ID via "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ No puedes añadirte a ti mismo como compañero.",
        "team_id_duplicate":
            "⚠️ El usuario <code>{member_id}</code> ya está en tu equipo.",
        "team_id_ok":
            "✅ ID <code>{member_id}</code> anotado.\n\n"
            "👥 <b>Paso 2 de 2</b> — Dale un nombre para identificarlo.\n\n"
            "Ejemplo: <i>Juan</i> o <i>Lead DevOps</i>\n\n"
            "Envía /skip para usar su ID como nombre, o /cancel para cancelar.",
        "team_label_too_long":
            "⚠️ El nombre debe tener 50 caracteres o menos. Prueba uno más corto:",
        "team_something_wrong":
            "Algo salió mal. Usa /team add para intentarlo de nuevo.",
        "team_already_member":
            "⚠️ El usuario <code>{member_id}</code> ya está en tu equipo.",
        "team_saved":
            "✅ <b>{display}</b> añadido a tu equipo.\n\n"
            "👤 ID: <code>{member_id}</code>\n\n"
            "Recibirá las mismas alertas de caída y recuperación que tú.\n\n"
            "⚠️ Asegúrate de que haya enviado <code>/start</code> a este bot, "
            "de lo contrario Telegram bloqueará la entrega.",
        "team_remove_confirm":
            "⚠️ ¿Eliminar a <b>{display}</b> de tu equipo?\n\n"
            "Dejará de recibir alertas inmediatamente.",
        "team_remove_not_found":    "Compañero no encontrado.",
        "team_btn_yes_remove":      "✅ Sí, eliminar",
        "team_btn_cancel":          "❌ Cancelar",
        "team_removed":
            "🗑 <b>{display}</b> eliminado de tu equipo.\n\n"
            "Usa /team para gestionar tus compañeros.",
        "team_remove_cancelled":    "❌ Cancelado. El compañero sigue activo.",
        "team_cancelled":           "❌ Cancelado.",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "sp_no_page_to_delete":
            "ليس لديك صفحة حالة لحذفها.",
        "sp_deleted":
            "🗑 <b>تم حذف صفحة الحالة.</b>\n\n"
            "الرابط غير نشط الآن. استخدم /statuspage لإنشاء صفحة جديدة.",
        "sp_title_pro_gate":
            "🔒 <b>العناوين المخصصة ميزة Pro.</b>\n\n"
            "يُرقِّي إلى Pro لتحديد عنوان مخصص وإزالة "
            "تذييل 'Powered by UptimeGuard'.",
        "sp_btn_upgrade":           "⭐ الترقية إلى Pro",
        "sp_no_page_for_title":
            "ليس لديك صفحة حالة بعد. "
            "شغّل /statuspage لإنشاء واحدة، ثم حدد العنوان.",
        "sp_ask_title":
            "✏️ أرسل لي العنوان الجديد لصفحة حالتك.\n\n"
            "مثال: <code>Acme Corp — حالة الخدمة</code>\n\n"
            "أرسل /cancel للإلغاء.",
        "sp_title_too_long":
            "⚠️ يجب أن يكون العنوان 80 حرفاً أو أقل. جرّب عنواناً أقصر:",
        "sp_title_updated":
            "✅ <b>تم تحديث العنوان!</b>\n\n"
            "🏷 العنوان الجديد: <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 فتح صفحة الحالة",
        "sp_cancelled":             "❌ تم الإلغاء.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro:</b> بدون علامة تجارية، عنوان مخصص نشط.",
        "sp_existing_free":
            "\n\n🆓 <b>الخطة المجانية:</b> تذييل 'Powered by UptimeGuard' معروض.\n"
            "يُرقِّي إلى Pro لإزالة العلامة التجارية وتحديد عنوان.",
        "sp_existing_page":
            "📡 <b>صفحة حالتك</b>\n\n"
            "🏷 العنوان: <b>{title}</b>\n"
            "🔗 الرابط:\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>الأوامر:</b>\n"
            "/statuspage delete — حذف صفحتك\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — تغيير العنوان\n",
        "sp_created_pro_extras":
            "\n✅ بدون علامة تجارية — صفحتك تبدو مخصصة بالكامل.\n"
            "استخدم /statuspage title لتحديد عنوان.",
        "sp_created_free_extras":
            "\n🆓 الخطة المجانية: تذييل 'Powered by UptimeGuard' معروض.\n"
            "يُرقِّي إلى Pro لإزالته وتحديد عنوان.",
        "sp_created":
            "✅ <b>تم إنشاء صفحة الحالة!</b>\n\n"
            "🔗 شارك هذا الرابط مع عملائك:\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "الصفحة تتحدث مباشرة وتتجدد كل 60 ثانية.",
        "sp_callback_pro_line":
            "✅ Pro: بدون علامة تجارية، عنوان مخصص عبر /statuspage title",
        "sp_callback_free_line":
            "🆓 مجاني: تذييل 'Powered by UptimeGuard' معروض.",
        "sp_callback_ready":
            "✅ <b>صفحة الحالة جاهزة!</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",
        "team_pro_gate":
            "👥 <b>إشعارات الفريق</b>\n\n"
            "إشعارات الفريق ميزة <b>Pro</b>.\n\n"
            "يُرقِّي لإضافة ما يصل إلى {limit} زملاء يتلقون "
            "نفس التنبيهات التي تتلقاها.",
        "team_btn_upgrade":         "⭐ الترقية إلى Pro",
        "team_empty":
            "👥 <b>إشعارات الفريق</b>\n\n"
            "ليس لديك زملاء بعد. يمكنك إضافة ما يصل إلى {limit}.\n\n"
            "يتلقى الزملاء نفس تنبيهات التوقف والاستعادة مباشرةً في رسائلهم.\n\n"
            "⚠️ <b>مهم:</b> يجب على كل زميل إرسال <code>/start</code> "
            "إلى هذا البوت أولاً قبل استقبال التنبيهات.",
        "team_btn_add":             "➕ إضافة زميل",
        "team_list_header":
            "👥 <b>إشعارات الفريق</b>\n\n"
            "<b>{count}/{limit}</b> زميل مضاف.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — المعرّف: <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>تذكير:</b> يجب على الزملاء إرسال <code>/start</code> "
            "إلى هذا البوت لاستقبال التنبيهات.",
        "team_btn_remove":          "🗑 إزالة {display}",
        "team_add_pro_gate":        "⭐ إشعارات الفريق ميزة Pro.",
        "team_limit_reached":
            "⚠️ لقد وصلت إلى حد {limit} زملاء.\n\n"
            "أزل زميلاً موجوداً قبل إضافة زميل جديد.",
        "team_step1_prompt":
            "👥 <b>إضافة زميل — الخطوة 1 من 2</b>\n\n"
            "أرسل <b>معرّف تيليغرام</b> الخاص بزميلك.\n\n"
            "يمكنه العثور على معرّفه عبر التواصل مع "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ يجب أيضاً أن يرسل <code>/start</code> إلى هذا البوت أولاً، "
            "وإلا سيحظر تيليغرام تسليم التنبيهات.\n\n"
            "أرسل /cancel للإلغاء.",
        "team_id_invalid":
            "⚠️ أرسل معرّف تيليغرام رقمياً.\n\n"
            "مثال: <code>123456789</code>\n\n"
            "يمكن لزميلك العثور على معرّفه عبر "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ لا يمكنك إضافة نفسك كزميل.",
        "team_id_duplicate":
            "⚠️ المستخدم <code>{member_id}</code> موجود بالفعل في فريقك.",
        "team_id_ok":
            "✅ المعرّف <code>{member_id}</code> تمت ملاحظته.\n\n"
            "👥 <b>الخطوة 2 من 2</b> — أعطه تسمية لتعرفه.\n\n"
            "مثال: <i>أحمد</i> أو <i>قائد DevOps</i>\n\n"
            "أرسل /skip لاستخدام معرّفه كتسمية، أو /cancel للإلغاء.",
        "team_label_too_long":
            "⚠️ التسمية يجب أن تكون 50 حرفاً أو أقل. جرّب اسماً أقصر:",
        "team_something_wrong":
            "حدث خطأ ما. استخدم /team add للمحاولة مجدداً.",
        "team_already_member":
            "⚠️ المستخدم <code>{member_id}</code> موجود بالفعل في فريقك.",
        "team_saved":
            "✅ تمت إضافة <b>{display}</b> إلى فريقك!\n\n"
            "👤 المعرّف: <code>{member_id}</code>\n\n"
            "سيتلقى الآن نفس تنبيهات التوقف والاستعادة التي تتلقاها.\n\n"
            "⚠️ تأكد من أنه أرسل <code>/start</code> إلى هذا البوت، "
            "وإلا سيحظر تيليغرام التسليم.",
        "team_remove_confirm":
            "⚠️ إزالة <b>{display}</b> من فريقك؟\n\n"
            "سيتوقف عن استقبال التنبيهات فوراً.",
        "team_remove_not_found":    "الزميل غير موجود.",
        "team_btn_yes_remove":      "✅ نعم، إزالة",
        "team_btn_cancel":          "❌ إلغاء",
        "team_removed":
            "🗑 تمت إزالة <b>{display}</b> من فريقك.\n\n"
            "استخدم /team لإدارة زملائك.",
        "team_remove_cancelled":    "❌ تم الإلغاء. الزميل لا يزال نشطاً.",
        "team_cancelled":           "❌ تم الإلغاء.",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "sp_no_page_to_delete":
            "Você não tem uma página de status para excluir.",
        "sp_deleted":
            "🗑 <b>Página de status excluída.</b>\n\n"
            "A URL está inativa. Use /statuspage para criar uma nova.",
        "sp_title_pro_gate":
            "🔒 <b>Títulos personalizados são uma função Pro.</b>\n\n"
            "Atualize para definir um título personalizado e remover o "
            "rodapé 'Powered by UptimeGuard'.",
        "sp_btn_upgrade":           "⭐ Atualizar para Pro",
        "sp_no_page_for_title":
            "Você ainda não tem uma página de status. "
            "Execute /statuspage para criar uma, depois defina um título.",
        "sp_ask_title":
            "✏️ Envie o novo título para sua página de status.\n\n"
            "Exemplo: <code>Acme Corp — Status dos Serviços</code>\n\n"
            "Envie /cancel para cancelar.",
        "sp_title_too_long":
            "⚠️ O título deve ter 80 caracteres ou menos. Tente um mais curto:",
        "sp_title_updated":
            "✅ <b>Título atualizado!</b>\n\n"
            "🏷 Novo título: <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 Abrir página de status",
        "sp_cancelled":             "❌ Cancelado.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro:</b> sem branding, título personalizado ativo.",
        "sp_existing_free":
            "\n\n🆓 <b>Plano gratuito:</b> rodapé 'Powered by UptimeGuard' exibido.\n"
            "Atualize para Pro para remover o branding e definir um título.",
        "sp_existing_page":
            "📡 <b>Sua Página de Status</b>\n\n"
            "🏷 Título: <b>{title}</b>\n"
            "🔗 URL:\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>Comandos:</b>\n"
            "/statuspage delete — remover sua página\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — alterar o título\n",
        "sp_created_pro_extras":
            "\n✅ Sem branding — sua página parece totalmente personalizada.\n"
            "Use /statuspage title para definir um título.",
        "sp_created_free_extras":
            "\n🆓 Plano gratuito: rodapé 'Powered by UptimeGuard' exibido.\n"
            "Atualize para Pro para removê-lo e definir um título.",
        "sp_created":
            "✅ <b>Página de status criada!</b>\n\n"
            "🔗 Compartilhe esta URL com seus clientes:\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "A página atualiza em tempo real e se recarrega a cada 60 segundos.",
        "sp_callback_pro_line":
            "✅ Pro: sem branding, título personalizado via /statuspage title",
        "sp_callback_free_line":
            "🆓 Grátis: rodapé 'Powered by UptimeGuard' exibido.",
        "sp_callback_ready":
            "✅ <b>Página de status pronta!</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",
        "team_pro_gate":
            "👥 <b>Notificações de Equipe</b>\n\n"
            "Notificações de equipe são uma função <b>Pro</b>.\n\n"
            "Atualize para adicionar até {limit} membros que recebam "
            "os mesmos alertas que você.",
        "team_btn_upgrade":         "⭐ Atualizar para Pro",
        "team_empty":
            "👥 <b>Notificações de Equipe</b>\n\n"
            "Você ainda não tem membros de equipe. Pode adicionar até {limit}.\n\n"
            "Os membros recebem os mesmos alertas de queda e recuperação, "
            "diretamente nos DMs do Telegram.\n\n"
            "⚠️ <b>Importante:</b> cada membro deve enviar <code>/start</code> "
            "para este bot antes de receber alertas.",
        "team_btn_add":             "➕ Adicionar membro",
        "team_list_header":
            "👥 <b>Notificações de Equipe</b>\n\n"
            "<b>{count}/{limit}</b> membro{plural} adicionado{plural}.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — ID: <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>Lembrete:</b> os membros devem enviar <code>/start</code> "
            "para este bot para receber alertas.",
        "team_btn_remove":          "🗑 Remover {display}",
        "team_add_pro_gate":        "⭐ Notificações de equipe são uma função Pro.",
        "team_limit_reached":
            "⚠️ Você atingiu o limite de {limit} membros.\n\n"
            "Remova um membro antes de adicionar outro.",
        "team_step1_prompt":
            "👥 <b>Adicionar membro — Passo 1 de 2</b>\n\n"
            "Envie o <b>ID do Telegram</b> do seu membro.\n\n"
            "Ele pode encontrar seu ID enviando mensagem para "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ Ele também deve enviar <code>/start</code> para este bot primeiro, "
            "caso contrário o Telegram bloqueará a entrega dos alertas.\n\n"
            "Envie /cancel para cancelar.",
        "team_id_invalid":
            "⚠️ Envie um ID numérico do Telegram.\n\n"
            "Exemplo: <code>123456789</code>\n\n"
            "Seu membro pode encontrar o ID via "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ Você não pode se adicionar como membro.",
        "team_id_duplicate":
            "⚠️ O usuário <code>{member_id}</code> já está na sua equipe.",
        "team_id_ok":
            "✅ ID <code>{member_id}</code> anotado.\n\n"
            "👥 <b>Passo 2 de 2</b> — Dê um nome para identificá-lo.\n\n"
            "Exemplo: <i>João</i> ou <i>Lead DevOps</i>\n\n"
            "Envie /skip para usar o ID como nome, ou /cancel para cancelar.",
        "team_label_too_long":
            "⚠️ O nome deve ter 50 caracteres ou menos. Tente um mais curto:",
        "team_something_wrong":
            "Algo deu errado. Use /team add para tentar novamente.",
        "team_already_member":
            "⚠️ O usuário <code>{member_id}</code> já está na sua equipe.",
        "team_saved":
            "✅ <b>{display}</b> adicionado à sua equipe!\n\n"
            "👤 ID: <code>{member_id}</code>\n\n"
            "Ele receberá os mesmos alertas de queda e recuperação que você.\n\n"
            "⚠️ Certifique-se de que ele enviou <code>/start</code> para este bot, "
            "caso contrário o Telegram bloqueará a entrega.",
        "team_remove_confirm":
            "⚠️ Remover <b>{display}</b> da sua equipe?\n\n"
            "Ele deixará de receber alertas imediatamente.",
        "team_remove_not_found":    "Membro não encontrado.",
        "team_btn_yes_remove":      "✅ Sim, remover",
        "team_btn_cancel":          "❌ Cancelar",
        "team_removed":
            "🗑 <b>{display}</b> removido da sua equipe.\n\n"
            "Use /team para gerenciar seus membros.",
        "team_remove_cancelled":    "❌ Cancelado. O membro ainda está ativo.",
        "team_cancelled":           "❌ Cancelado.",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "sp_no_page_to_delete":
            "У тебя нет страницы статуса для удаления.",
        "sp_deleted":
            "🗑 <b>Страница статуса удалена.</b>\n\n"
            "URL больше не активен. Используй /statuspage для создания новой.",
        "sp_title_pro_gate":
            "🔒 <b>Пользовательские заголовки — функция Pro.</b>\n\n"
            "Перейди на Pro, чтобы задать заголовок и убрать "
            "подпись 'Powered by UptimeGuard'.",
        "sp_btn_upgrade":           "⭐ Перейти на Pro",
        "sp_no_page_for_title":
            "У тебя ещё нет страницы статуса. "
            "Запусти /statuspage для создания, затем задай заголовок.",
        "sp_ask_title":
            "✏️ Отправь мне новый заголовок для страницы статуса.\n\n"
            "Пример: <code>Acme Corp — Статус сервисов</code>\n\n"
            "Отправь /cancel для отмены.",
        "sp_title_too_long":
            "⚠️ Заголовок должен быть не длиннее 80 символов. Попробуй покороче:",
        "sp_title_updated":
            "✅ <b>Заголовок обновлён!</b>\n\n"
            "🏷 Новый заголовок: <b>{title}</b>\n"
            "🔗 <code>{url}</code>",
        "sp_btn_open":              "🔗 Открыть страницу статуса",
        "sp_cancelled":             "❌ Отменено.",
        "sp_existing_pro":
            "\n\n✅ <b>Pro:</b> без брендинга, пользовательский заголовок активен.",
        "sp_existing_free":
            "\n\n🆓 <b>Бесплатный план:</b> подпись 'Powered by UptimeGuard' отображается.\n"
            "Перейди на Pro, чтобы убрать брендинг и задать заголовок.",
        "sp_existing_page":
            "📡 <b>Твоя страница статуса</b>\n\n"
            "🏷 Заголовок: <b>{title}</b>\n"
            "🔗 URL:\n<code>{url}</code>"
            "{pro_line}\n\n"
            "<b>Команды:</b>\n"
            "/statuspage delete — удалить страницу\n"
            "{title_cmd}",
        "sp_existing_title_cmd":    "/statuspage title — изменить заголовок\n",
        "sp_created_pro_extras":
            "\n✅ Без брендинга — страница выглядит полностью кастомной.\n"
            "Используй /statuspage title для задания заголовка.",
        "sp_created_free_extras":
            "\n🆓 Бесплатный план: подпись 'Powered by UptimeGuard' отображается.\n"
            "Перейди на Pro, чтобы убрать её и задать заголовок.",
        "sp_created":
            "✅ <b>Страница статуса создана!</b>\n\n"
            "🔗 Поделись этим URL с клиентами:\n"
            "<code>{url}</code>"
            "{pro_extras}\n\n"
            "Страница обновляется в реальном времени и обновляется каждые 60 секунд.",
        "sp_callback_pro_line":
            "✅ Pro: без брендинга, заголовок через /statuspage title",
        "sp_callback_free_line":
            "🆓 Бесплатный: подпись 'Powered by UptimeGuard' отображается.",
        "sp_callback_ready":
            "✅ <b>Страница статуса готова!</b>\n\n"
            "🔗 <code>{url}</code>\n\n"
            "{pro_line}",
        "team_pro_gate":
            "👥 <b>Командные уведомления</b>\n\n"
            "Командные уведомления — функция <b>Pro</b>.\n\n"
            "Перейди на Pro, чтобы добавить до {limit} участников, которые "
            "получают те же уведомления, что и ты.",
        "team_btn_upgrade":         "⭐ Перейти на Pro",
        "team_empty":
            "👥 <b>Командные уведомления</b>\n\n"
            "У тебя пока нет участников команды. Можно добавить до {limit}.\n\n"
            "Участники получают те же уведомления о падении и восстановлении, "
            "прямо в их Telegram.\n\n"
            "⚠️ <b>Важно:</b> каждый участник должен отправить <code>/start</code> "
            "этому боту перед получением уведомлений.",
        "team_btn_add":             "➕ Добавить участника",
        "team_list_header":
            "👥 <b>Командные уведомления</b>\n\n"
            "<b>{count}/{limit}</b> участник(ов) добавлено.\n\n",
        "team_list_member":
            "👤 <b>{display}</b> — ID: <code>{member_id}</code>\n",
        "team_list_reminder":
            "\n⚠️ <b>Напоминание:</b> участники должны отправить <code>/start</code> "
            "этому боту для получения уведомлений.",
        "team_btn_remove":          "🗑 Удалить {display}",
        "team_add_pro_gate":        "⭐ Командные уведомления — функция Pro.",
        "team_limit_reached":
            "⚠️ Достигнут лимит в {limit} участников.\n\n"
            "Удали существующего участника перед добавлением нового.",
        "team_step1_prompt":
            "👥 <b>Добавить участника — Шаг 1 из 2</b>\n\n"
            "Отправь <b>Telegram ID</b> участника.\n\n"
            "Он может найти свой ID через "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
            "⚠️ Он также должен отправить <code>/start</code> этому боту сначала, "
            "иначе Telegram заблокирует доставку уведомлений.\n\n"
            "Отправь /cancel для отмены.",
        "team_id_invalid":
            "⚠️ Отправь числовой Telegram ID.\n\n"
            "Пример: <code>123456789</code>\n\n"
            "Участник может найти свой ID через "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
        "team_id_self":
            "⚠️ Нельзя добавить себя как участника.",
        "team_id_duplicate":
            "⚠️ Пользователь <code>{member_id}</code> уже в твоей команде.",
        "team_id_ok":
            "✅ ID <code>{member_id}</code> записан.\n\n"
            "👥 <b>Шаг 2 из 2</b> — Дай ему название для идентификации.\n\n"
            "Пример: <i>Иван</i> или <i>Лид DevOps</i>\n\n"
            "Отправь /skip, чтобы использовать ID как название, или /cancel для отмены.",
        "team_label_too_long":
            "⚠️ Название должно быть не длиннее 50 символов. Попробуй покороче:",
        "team_something_wrong":
            "Что-то пошло не так. Используй /team add для повторной попытки.",
        "team_already_member":
            "⚠️ Пользователь <code>{member_id}</code> уже в твоей команде.",
        "team_saved":
            "✅ <b>{display}</b> добавлен в команду!\n\n"
            "👤 ID: <code>{member_id}</code>\n\n"
            "Теперь он будет получать те же уведомления о падении и восстановлении.\n\n"
            "⚠️ Убедись, что он отправил <code>/start</code> этому боту, "
            "иначе Telegram заблокирует доставку.",
        "team_remove_confirm":
            "⚠️ Удалить <b>{display}</b> из команды?\n\n"
            "Он немедленно перестанет получать уведомления.",
        "team_remove_not_found":    "Участник не найден.",
        "team_btn_yes_remove":      "✅ Да, удалить",
        "team_btn_cancel":          "❌ Отмена",
        "team_removed":
            "🗑 <b>{display}</b> удалён из команды.\n\n"
            "Используй /team для управления участниками.",
        "team_remove_cancelled":    "❌ Отменено. Участник всё ещё активен.",
        "team_cancelled":           "❌ Отменено.",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


def tt(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in team/statuspage locale for `lang`, falling back to English.

    Usage:
        from locales.team_strings import tt
        tt("fr", "sp_created", url="https://...", pro_extras="...")
        tt("ru", "team_saved", display="Иван", member_id=123456789)
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string