# locales/utility_strings.py
"""
Translation strings for handlers/testalert.py and handlers/maintenance.py.

Usage:
    from locales.utility_strings import ut
    ut("fr", "testalert_cooldown", remaining=45)
    ut("es", "mw_step1_prompt")
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # ── testalert.py ──────────────────────────────────────────────────
        "testalert_cooldown":
            "⏳ Please wait <b>{remaining}s</b> before sending another test alert.",
        "testalert_no_monitors":
            "⚠️ You have no active monitors to test.\n\n"
            "Use /add to add your first monitor.",
        "testalert_sending":
            "🧪 Sending test alert for <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>Test Alert</b>\n\nWhich monitor do you want to test?",
        "testalert_not_found":
            "⚠️ Monitor not found.",

        # ── maintenance.py — list view ────────────────────────────────────
        "mw_list_empty":
            "🔧 <b>Maintenance Windows</b>\n\n"
            "You have no scheduled maintenance windows.\n\n"
            "Use /maintenance add to create one.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>Maintenance Windows</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro: unlimited windows.",
        "mw_list_plan_free":    "🆓 Free: {limit} window. {used_str}",
        "mw_list_used":         "Used.",
        "mw_list_available":    "Available.",
        "mw_btn_add":           "➕ Add Window",
        "mw_btn_delete":        "🗑 Delete — {label}",

        # ── maintenance.py — add flow ─────────────────────────────────────
        "mw_limit_reached":
            "⚠️ Free plan allows <b>{limit} maintenance window</b>.\n\n"
            "Upgrade to Pro for unlimited windows.",
        "mw_btn_upgrade":       "⭐ Upgrade to Pro",
        "mw_step1_prompt":
            "🔧 <b>Add Maintenance Window</b>\n\n"
            "Step 1 of 4 — Give this window a label.\n\n"
            "Example: <i>Nightly backup</i> or <i>Deploy window</i>\n\n"
            "Send /cancel to abort.",
        "mw_step1_too_long":
            "⚠️ Label must be 60 characters or less. Try a shorter one:",
        "mw_step2_prompt":
            "📆 <b>Step 2 of 4 — When does this window repeat?</b>\n\n"
            "Choose a preset or send /cancel to abort.",
        "mw_days_weekdays":     "Mon – Fri",
        "mw_days_everyday":     "Every day",
        "mw_days_weekends":     "Sat & Sun",
        "mw_days_oneoff":       "One-off (today only)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> selected.\n\n"
            "🕐 <b>Step 3 of 4 — Start time?</b>\n\n"
            "Send in 24-hour format. Example: <code>02:00</code>\n\n"
            "Send /cancel to abort.",
        "mw_step3_invalid":
            "⚠️ Please use 24-hour format. "
            "Example: <code>02:00</code> or <code>23:30</code>",
        "mw_step4_prompt":
            "✅ Start: <b>{start}</b>\n\n"
            "🕐 <b>Step 4 of 4 — End time?</b>\n\n"
            "Send in 24-hour format. Example: <code>04:00</code>\n"
            "<i>Overnight windows are supported, e.g. 23:00 – 01:00.</i>\n\n"
            "Send /cancel to abort.",
        "mw_step4_invalid":
            "⚠️ Please use 24-hour format. Example: <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ End time must be different from start time. Try again:",
        "mw_confirm_prompt":
            "✅ <b>Confirm Maintenance Window</b>\n\n"
            "🏷 Label: <b>{label}</b>\n"
            "🕐 Time: <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "During this window, no alerts will fire for any of your monitors.\n"
            "Checks still run and history is still recorded.\n\n"
            "Save this window?",
        "mw_overnight_note":    "\n<i>⏰ Overnight window — wraps past midnight.</i>",
        "mw_date_repeats":      "📆 Repeats: <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>One-off</b> — active today only",
        "mw_btn_save":          "✅ Save",
        "mw_btn_cancel":        "❌ Cancel",
        "mw_cancelled":         "❌ Cancelled. No window was saved.",
        "mw_saved":
            "✅ <b>Maintenance window saved!</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "No alerts will fire during this window.\n"
            "Use /maintenance to view or delete windows.",
        "mw_delete_not_found":  "⚠️ Window not found or already deleted.",
        "mw_deleted":
            "🗑 <b>{label}</b> has been deleted.\n\n"
            "Use /maintenance to manage your windows.",
        "mw_cancel_fallback":   "❌ Cancelled.",

        # day labels for list view (read from DB, displayed in list)
        "mw_days_label_everyday":   "Every day",
        "mw_days_label_weekdays":   "Weekdays (Mon–Fri)",
        "mw_days_label_weekends":   "Weekends (Sat–Sun)",
        "mw_days_label_oneoff":     "One-off (today only)",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "testalert_cooldown":
            "⏳ Attends <b>{remaining}s</b> avant d'envoyer une autre alerte test.",
        "testalert_no_monitors":
            "⚠️ Tu n'as pas de moniteurs actifs à tester.\n\n"
            "Utilise /add pour ajouter ton premier moniteur.",
        "testalert_sending":
            "🧪 Envoi d'une alerte test pour <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>Alerte test</b>\n\nQuel moniteur veux-tu tester ?",
        "testalert_not_found":
            "⚠️ Moniteur introuvable.",
        "mw_list_empty":
            "🔧 <b>Fenêtres de maintenance</b>\n\n"
            "Tu n'as aucune fenêtre de maintenance planifiée.\n\n"
            "Utilise /maintenance add pour en créer une.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>Fenêtres de maintenance</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro : fenêtres illimitées.",
        "mw_list_plan_free":    "🆓 Gratuit : {limit} fenêtre. {used_str}",
        "mw_list_used":         "Utilisée.",
        "mw_list_available":    "Disponible.",
        "mw_btn_add":           "➕ Ajouter une fenêtre",
        "mw_btn_delete":        "🗑 Supprimer — {label}",
        "mw_limit_reached":
            "⚠️ Le plan gratuit permet <b>{limit} fenêtre de maintenance</b>.\n\n"
            "Passe à Pro pour des fenêtres illimitées.",
        "mw_btn_upgrade":       "⭐ Passer à Pro",
        "mw_step1_prompt":
            "🔧 <b>Ajouter une fenêtre de maintenance</b>\n\n"
            "Étape 1/4 — Donne un nom à cette fenêtre.\n\n"
            "Exemple : <i>Sauvegarde nocturne</i> ou <i>Déploiement</i>\n\n"
            "Envoie /cancel pour annuler.",
        "mw_step1_too_long":
            "⚠️ Le nom doit faire 60 caractères maximum. Essaie un nom plus court :",
        "mw_step2_prompt":
            "📆 <b>Étape 2/4 — Quand cette fenêtre se répète-t-elle ?</b>\n\n"
            "Choisis un préréglage ou envoie /cancel pour annuler.",
        "mw_days_weekdays":     "Lun – Ven",
        "mw_days_everyday":     "Tous les jours",
        "mw_days_weekends":     "Sam & Dim",
        "mw_days_oneoff":       "Ponctuel (aujourd'hui seulement)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> sélectionné.\n\n"
            "🕐 <b>Étape 3/4 — Heure de début ?</b>\n\n"
            "Envoie au format 24h. Exemple : <code>02:00</code>\n\n"
            "Envoie /cancel pour annuler.",
        "mw_step3_invalid":
            "⚠️ Utilise le format 24h. "
            "Exemple : <code>02:00</code> ou <code>23:30</code>",
        "mw_step4_prompt":
            "✅ Début : <b>{start}</b>\n\n"
            "🕐 <b>Étape 4/4 — Heure de fin ?</b>\n\n"
            "Envoie au format 24h. Exemple : <code>04:00</code>\n"
            "<i>Les fenêtres de nuit sont prises en charge, ex. 23:00 – 01:00.</i>\n\n"
            "Envoie /cancel pour annuler.",
        "mw_step4_invalid":
            "⚠️ Utilise le format 24h. Exemple : <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ L'heure de fin doit être différente de l'heure de début. Réessaie :",
        "mw_confirm_prompt":
            "✅ <b>Confirmer la fenêtre de maintenance</b>\n\n"
            "🏷 Nom : <b>{label}</b>\n"
            "🕐 Horaire : <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "Pendant cette fenêtre, aucune alerte ne sera envoyée.\n"
            "Les vérifications continuent et l'historique est conservé.\n\n"
            "Enregistrer cette fenêtre ?",
        "mw_overnight_note":    "\n<i>⏰ Fenêtre de nuit — dépasse minuit.</i>",
        "mw_date_repeats":      "📆 Répétition : <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>Ponctuel</b> — actif aujourd'hui seulement",
        "mw_btn_save":          "✅ Enregistrer",
        "mw_btn_cancel":        "❌ Annuler",
        "mw_cancelled":         "❌ Annulé. Aucune fenêtre enregistrée.",
        "mw_saved":
            "✅ <b>Fenêtre de maintenance enregistrée !</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "Aucune alerte ne se déclenchera pendant cette fenêtre.\n"
            "Utilise /maintenance pour gérer tes fenêtres.",
        "mw_delete_not_found":  "⚠️ Fenêtre introuvable ou déjà supprimée.",
        "mw_deleted":
            "🗑 <b>{label}</b> a été supprimée.\n\n"
            "Utilise /maintenance pour gérer tes fenêtres.",
        "mw_cancel_fallback":   "❌ Annulé.",
        "mw_days_label_everyday":   "Tous les jours",
        "mw_days_label_weekdays":   "Jours ouvrés (Lun–Ven)",
        "mw_days_label_weekends":   "Week-end (Sam–Dim)",
        "mw_days_label_oneoff":     "Ponctuel (aujourd'hui seulement)",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "testalert_cooldown":
            "⏳ Espera <b>{remaining}s</b> antes de enviar otra alerta de prueba.",
        "testalert_no_monitors":
            "⚠️ No tienes monitores activos para probar.\n\n"
            "Usa /add para añadir tu primer monitor.",
        "testalert_sending":
            "🧪 Enviando alerta de prueba para <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>Alerta de prueba</b>\n\n¿Qué monitor quieres probar?",
        "testalert_not_found":
            "⚠️ Monitor no encontrado.",
        "mw_list_empty":
            "🔧 <b>Ventanas de mantenimiento</b>\n\n"
            "No tienes ventanas de mantenimiento programadas.\n\n"
            "Usa /maintenance add para crear una.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>Ventanas de mantenimiento</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro: ventanas ilimitadas.",
        "mw_list_plan_free":    "🆓 Gratis: {limit} ventana. {used_str}",
        "mw_list_used":         "Usada.",
        "mw_list_available":    "Disponible.",
        "mw_btn_add":           "➕ Añadir ventana",
        "mw_btn_delete":        "🗑 Eliminar — {label}",
        "mw_limit_reached":
            "⚠️ El plan gratuito permite <b>{limit} ventana de mantenimiento</b>.\n\n"
            "Actualiza a Pro para ventanas ilimitadas.",
        "mw_btn_upgrade":       "⭐ Actualizar a Pro",
        "mw_step1_prompt":
            "🔧 <b>Añadir ventana de mantenimiento</b>\n\n"
            "Paso 1 de 4 — Dale un nombre a esta ventana.\n\n"
            "Ejemplo: <i>Copia de seguridad nocturna</i> o <i>Despliegue</i>\n\n"
            "Envía /cancel para cancelar.",
        "mw_step1_too_long":
            "⚠️ El nombre debe tener 60 caracteres o menos. Prueba uno más corto:",
        "mw_step2_prompt":
            "📆 <b>Paso 2 de 4 — ¿Cuándo se repite esta ventana?</b>\n\n"
            "Elige un preset o envía /cancel para cancelar.",
        "mw_days_weekdays":     "Lun – Vie",
        "mw_days_everyday":     "Todos los días",
        "mw_days_weekends":     "Sáb & Dom",
        "mw_days_oneoff":       "Única vez (solo hoy)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> seleccionado.\n\n"
            "🕐 <b>Paso 3 de 4 — ¿Hora de inicio?</b>\n\n"
            "Envía en formato 24h. Ejemplo: <code>02:00</code>\n\n"
            "Envía /cancel para cancelar.",
        "mw_step3_invalid":
            "⚠️ Usa el formato 24h. "
            "Ejemplo: <code>02:00</code> o <code>23:30</code>",
        "mw_step4_prompt":
            "✅ Inicio: <b>{start}</b>\n\n"
            "🕐 <b>Paso 4 de 4 — ¿Hora de fin?</b>\n\n"
            "Envía en formato 24h. Ejemplo: <code>04:00</code>\n"
            "<i>Se admiten ventanas nocturnas, ej. 23:00 – 01:00.</i>\n\n"
            "Envía /cancel para cancelar.",
        "mw_step4_invalid":
            "⚠️ Usa el formato 24h. Ejemplo: <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ La hora de fin debe ser diferente a la de inicio. Inténtalo de nuevo:",
        "mw_confirm_prompt":
            "✅ <b>Confirmar ventana de mantenimiento</b>\n\n"
            "🏷 Nombre: <b>{label}</b>\n"
            "🕐 Horario: <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "Durante esta ventana no se enviarán alertas.\n"
            "Las verificaciones continúan y el historial se conserva.\n\n"
            "¿Guardar esta ventana?",
        "mw_overnight_note":    "\n<i>⏰ Ventana nocturna — pasa la medianoche.</i>",
        "mw_date_repeats":      "📆 Se repite: <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>Única vez</b> — activa solo hoy",
        "mw_btn_save":          "✅ Guardar",
        "mw_btn_cancel":        "❌ Cancelar",
        "mw_cancelled":         "❌ Cancelado. No se guardó ninguna ventana.",
        "mw_saved":
            "✅ <b>¡Ventana de mantenimiento guardada!</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "No se dispararán alertas durante esta ventana.\n"
            "Usa /maintenance para ver o eliminar ventanas.",
        "mw_delete_not_found":  "⚠️ Ventana no encontrada o ya eliminada.",
        "mw_deleted":
            "🗑 <b>{label}</b> ha sido eliminada.\n\n"
            "Usa /maintenance para gestionar tus ventanas.",
        "mw_cancel_fallback":   "❌ Cancelado.",
        "mw_days_label_everyday":   "Todos los días",
        "mw_days_label_weekdays":   "Días laborables (Lun–Vie)",
        "mw_days_label_weekends":   "Fin de semana (Sáb–Dom)",
        "mw_days_label_oneoff":     "Única vez (solo hoy)",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "testalert_cooldown":
            "⏳ انتظر <b>{remaining}s</b> قبل إرسال تنبيه اختبار آخر.",
        "testalert_no_monitors":
            "⚠️ ليس لديك مراقبون نشطون للاختبار.\n\n"
            "استخدم /add لإضافة أول مراقب.",
        "testalert_sending":
            "🧪 جارٍ إرسال تنبيه اختبار لـ <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>تنبيه اختبار</b>\n\nأي مراقب تريد اختباره؟",
        "testalert_not_found":
            "⚠️ المراقب غير موجود.",
        "mw_list_empty":
            "🔧 <b>نوافذ الصيانة</b>\n\n"
            "ليس لديك نوافذ صيانة مجدولة.\n\n"
            "استخدم /maintenance add لإنشاء نافذة.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>نوافذ الصيانة</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro: نوافذ غير محدودة.",
        "mw_list_plan_free":    "🆓 مجاني: {limit} نافذة. {used_str}",
        "mw_list_used":         "مستخدمة.",
        "mw_list_available":    "متاحة.",
        "mw_btn_add":           "➕ إضافة نافذة",
        "mw_btn_delete":        "🗑 حذف — {label}",
        "mw_limit_reached":
            "⚠️ الخطة المجانية تسمح بـ <b>{limit} نافذة صيانة</b>.\n\n"
            "يُرقِّي إلى Pro للحصول على نوافذ غير محدودة.",
        "mw_btn_upgrade":       "⭐ الترقية إلى Pro",
        "mw_step1_prompt":
            "🔧 <b>إضافة نافذة صيانة</b>\n\n"
            "الخطوة 1 من 4 — أعطِ هذه النافذة تسمية.\n\n"
            "مثال: <i>نسخ احتياطي ليلي</i> أو <i>نافذة نشر</i>\n\n"
            "أرسل /cancel للإلغاء.",
        "mw_step1_too_long":
            "⚠️ يجب أن تكون التسمية 60 حرفاً أو أقل. جرّب اسماً أقصر:",
        "mw_step2_prompt":
            "📆 <b>الخطوة 2 من 4 — متى تتكرر هذه النافذة؟</b>\n\n"
            "اختر إعداداً مسبقاً أو أرسل /cancel للإلغاء.",
        "mw_days_weekdays":     "الإثنين – الجمعة",
        "mw_days_everyday":     "كل يوم",
        "mw_days_weekends":     "السبت والأحد",
        "mw_days_oneoff":       "مرة واحدة (اليوم فقط)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> محدد.\n\n"
            "🕐 <b>الخطوة 3 من 4 — وقت البدء؟</b>\n\n"
            "أرسل بتنسيق 24 ساعة. مثال: <code>02:00</code>\n\n"
            "أرسل /cancel للإلغاء.",
        "mw_step3_invalid":
            "⚠️ استخدم تنسيق 24 ساعة. "
            "مثال: <code>02:00</code> أو <code>23:30</code>",
        "mw_step4_prompt":
            "✅ البدء: <b>{start}</b>\n\n"
            "🕐 <b>الخطوة 4 من 4 — وقت الانتهاء؟</b>\n\n"
            "أرسل بتنسيق 24 ساعة. مثال: <code>04:00</code>\n"
            "<i>النوافذ الليلية مدعومة، مثال: 23:00 – 01:00.</i>\n\n"
            "أرسل /cancel للإلغاء.",
        "mw_step4_invalid":
            "⚠️ استخدم تنسيق 24 ساعة. مثال: <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ يجب أن يختلف وقت الانتهاء عن وقت البدء. حاول مجدداً:",
        "mw_confirm_prompt":
            "✅ <b>تأكيد نافذة الصيانة</b>\n\n"
            "🏷 التسمية: <b>{label}</b>\n"
            "🕐 الوقت: <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "خلال هذه النافذة لن تُرسَل أي تنبيهات.\n"
            "تستمر الفحوصات وتُسجَّل السجلات.\n\n"
            "حفظ هذه النافذة؟",
        "mw_overnight_note":    "\n<i>⏰ نافذة ليلية — تمتد إلى ما بعد منتصف الليل.</i>",
        "mw_date_repeats":      "📆 تتكرر: <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>مرة واحدة</b> — نشطة اليوم فقط",
        "mw_btn_save":          "✅ حفظ",
        "mw_btn_cancel":        "❌ إلغاء",
        "mw_cancelled":         "❌ تم الإلغاء. لم تُحفظ أي نافذة.",
        "mw_saved":
            "✅ <b>تم حفظ نافذة الصيانة!</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "لن تُطلَق أي تنبيهات خلال هذه النافذة.\n"
            "استخدم /maintenance لعرض النوافذ أو حذفها.",
        "mw_delete_not_found":  "⚠️ النافذة غير موجودة أو تم حذفها بالفعل.",
        "mw_deleted":
            "🗑 تم حذف <b>{label}</b>.\n\n"
            "استخدم /maintenance لإدارة نوافذك.",
        "mw_cancel_fallback":   "❌ تم الإلغاء.",
        "mw_days_label_everyday":   "كل يوم",
        "mw_days_label_weekdays":   "أيام العمل (الإثنين–الجمعة)",
        "mw_days_label_weekends":   "عطلة نهاية الأسبوع (السبت–الأحد)",
        "mw_days_label_oneoff":     "مرة واحدة (اليوم فقط)",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "testalert_cooldown":
            "⏳ Aguarde <b>{remaining}s</b> antes de enviar outro alerta de teste.",
        "testalert_no_monitors":
            "⚠️ Você não tem monitores ativos para testar.\n\n"
            "Use /add para adicionar seu primeiro monitor.",
        "testalert_sending":
            "🧪 Enviando alerta de teste para <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>Alerta de Teste</b>\n\nQual monitor você quer testar?",
        "testalert_not_found":
            "⚠️ Monitor não encontrado.",
        "mw_list_empty":
            "🔧 <b>Janelas de Manutenção</b>\n\n"
            "Você não tem janelas de manutenção programadas.\n\n"
            "Use /maintenance add para criar uma.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>Janelas de Manutenção</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro: janelas ilimitadas.",
        "mw_list_plan_free":    "🆓 Grátis: {limit} janela. {used_str}",
        "mw_list_used":         "Usada.",
        "mw_list_available":    "Disponível.",
        "mw_btn_add":           "➕ Adicionar janela",
        "mw_btn_delete":        "🗑 Excluir — {label}",
        "mw_limit_reached":
            "⚠️ O plano gratuito permite <b>{limit} janela de manutenção</b>.\n\n"
            "Atualize para Pro para janelas ilimitadas.",
        "mw_btn_upgrade":       "⭐ Atualizar para Pro",
        "mw_step1_prompt":
            "🔧 <b>Adicionar janela de manutenção</b>\n\n"
            "Passo 1 de 4 — Dê um nome a esta janela.\n\n"
            "Exemplo: <i>Backup noturno</i> ou <i>Janela de deploy</i>\n\n"
            "Envie /cancel para cancelar.",
        "mw_step1_too_long":
            "⚠️ O nome deve ter 60 caracteres ou menos. Tente um nome mais curto:",
        "mw_step2_prompt":
            "📆 <b>Passo 2 de 4 — Quando esta janela se repete?</b>\n\n"
            "Escolha um preset ou envie /cancel para cancelar.",
        "mw_days_weekdays":     "Seg – Sex",
        "mw_days_everyday":     "Todos os dias",
        "mw_days_weekends":     "Sáb & Dom",
        "mw_days_oneoff":       "Única vez (só hoje)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> selecionado.\n\n"
            "🕐 <b>Passo 3 de 4 — Horário de início?</b>\n\n"
            "Envie no formato 24h. Exemplo: <code>02:00</code>\n\n"
            "Envie /cancel para cancelar.",
        "mw_step3_invalid":
            "⚠️ Use o formato 24h. "
            "Exemplo: <code>02:00</code> ou <code>23:30</code>",
        "mw_step4_prompt":
            "✅ Início: <b>{start}</b>\n\n"
            "🕐 <b>Passo 4 de 4 — Horário de fim?</b>\n\n"
            "Envie no formato 24h. Exemplo: <code>04:00</code>\n"
            "<i>Janelas noturnas são suportadas, ex. 23:00 – 01:00.</i>\n\n"
            "Envie /cancel para cancelar.",
        "mw_step4_invalid":
            "⚠️ Use o formato 24h. Exemplo: <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ O horário de fim deve ser diferente do de início. Tente novamente:",
        "mw_confirm_prompt":
            "✅ <b>Confirmar janela de manutenção</b>\n\n"
            "🏷 Nome: <b>{label}</b>\n"
            "🕐 Horário: <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "Durante esta janela, nenhum alerta será enviado.\n"
            "As verificações continuam e o histórico é mantido.\n\n"
            "Salvar esta janela?",
        "mw_overnight_note":    "\n<i>⏰ Janela noturna — passa da meia-noite.</i>",
        "mw_date_repeats":      "📆 Repete: <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>Única vez</b> — ativa só hoje",
        "mw_btn_save":          "✅ Salvar",
        "mw_btn_cancel":        "❌ Cancelar",
        "mw_cancelled":         "❌ Cancelado. Nenhuma janela foi salva.",
        "mw_saved":
            "✅ <b>Janela de manutenção salva!</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "Nenhum alerta será disparado durante esta janela.\n"
            "Use /maintenance para ver ou excluir janelas.",
        "mw_delete_not_found":  "⚠️ Janela não encontrada ou já excluída.",
        "mw_deleted":
            "🗑 <b>{label}</b> foi excluída.\n\n"
            "Use /maintenance para gerenciar suas janelas.",
        "mw_cancel_fallback":   "❌ Cancelado.",
        "mw_days_label_everyday":   "Todos os dias",
        "mw_days_label_weekdays":   "Dias úteis (Seg–Sex)",
        "mw_days_label_weekends":   "Fim de semana (Sáb–Dom)",
        "mw_days_label_oneoff":     "Única vez (só hoje)",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "testalert_cooldown":
            "⏳ Подожди <b>{remaining}s</b> перед отправкой следующего тестового уведомления.",
        "testalert_no_monitors":
            "⚠️ У тебя нет активных мониторов для тестирования.\n\n"
            "Используй /add для добавления первого монитора.",
        "testalert_sending":
            "🧪 Отправляю тестовое уведомление для <b>{label}</b>…",
        "testalert_picker":
            "🧪 <b>Тестовое уведомление</b>\n\nКакой монитор хочешь протестировать?",
        "testalert_not_found":
            "⚠️ Монитор не найден.",
        "mw_list_empty":
            "🔧 <b>Окна технического обслуживания</b>\n\n"
            "У тебя нет запланированных окон обслуживания.\n\n"
            "Используй /maintenance add для создания.\n\n"
            "{plan_note}",
        "mw_list_header":       "🔧 <b>Окна технического обслуживания</b>\n\n",
        "mw_list_row":
            "📅 <b>{label}</b>\n"
            "   🕐 {start} – {end}\n"
            "   📆 {days}\n\n",
        "mw_list_plan_pro":     "⭐ Pro: неограниченное количество окон.",
        "mw_list_plan_free":    "🆓 Бесплатный: {limit} окно. {used_str}",
        "mw_list_used":         "Использовано.",
        "mw_list_available":    "Доступно.",
        "mw_btn_add":           "➕ Добавить окно",
        "mw_btn_delete":        "🗑 Удалить — {label}",
        "mw_limit_reached":
            "⚠️ Бесплатный план позволяет <b>{limit} окно обслуживания</b>.\n\n"
            "Перейди на Pro для неограниченного количества окон.",
        "mw_btn_upgrade":       "⭐ Перейти на Pro",
        "mw_step1_prompt":
            "🔧 <b>Добавить окно обслуживания</b>\n\n"
            "Шаг 1 из 4 — Дай название этому окну.\n\n"
            "Пример: <i>Ночное резервное копирование</i> или <i>Окно деплоя</i>\n\n"
            "Отправь /cancel для отмены.",
        "mw_step1_too_long":
            "⚠️ Название должно быть не длиннее 60 символов. Попробуй покороче:",
        "mw_step2_prompt":
            "📆 <b>Шаг 2 из 4 — Когда повторяется это окно?</b>\n\n"
            "Выбери пресет или отправь /cancel для отмены.",
        "mw_days_weekdays":     "Пн – Пт",
        "mw_days_everyday":     "Каждый день",
        "mw_days_weekends":     "Сб и Вс",
        "mw_days_oneoff":       "Однократно (только сегодня)",
        "mw_step2_selected":
            "✅ <b>{days_label}</b> выбрано.\n\n"
            "🕐 <b>Шаг 3 из 4 — Время начала?</b>\n\n"
            "Отправь в формате 24ч. Пример: <code>02:00</code>\n\n"
            "Отправь /cancel для отмены.",
        "mw_step3_invalid":
            "⚠️ Используй формат 24ч. "
            "Пример: <code>02:00</code> или <code>23:30</code>",
        "mw_step4_prompt":
            "✅ Начало: <b>{start}</b>\n\n"
            "🕐 <b>Шаг 4 из 4 — Время окончания?</b>\n\n"
            "Отправь в формате 24ч. Пример: <code>04:00</code>\n"
            "<i>Ночные окна поддерживаются, напр. 23:00 – 01:00.</i>\n\n"
            "Отправь /cancel для отмены.",
        "mw_step4_invalid":
            "⚠️ Используй формат 24ч. Пример: <code>04:00</code>",
        "mw_step4_same_time":
            "⚠️ Время окончания должно отличаться от времени начала. Попробуй снова:",
        "mw_confirm_prompt":
            "✅ <b>Подтвердить окно обслуживания</b>\n\n"
            "🏷 Название: <b>{label}</b>\n"
            "🕐 Время: <b>{start} – {end}</b>{overnight}\n"
            "{date_line}\n\n"
            "В течение этого окна уведомления отправляться не будут.\n"
            "Проверки продолжаются и история сохраняется.\n\n"
            "Сохранить это окно?",
        "mw_overnight_note":    "\n<i>⏰ Ночное окно — переходит через полночь.</i>",
        "mw_date_repeats":      "📆 Повторяется: <b>{days_label}</b>",
        "mw_date_oneoff":       "📆 <b>Однократно</b> — активно только сегодня",
        "mw_btn_save":          "✅ Сохранить",
        "mw_btn_cancel":        "❌ Отмена",
        "mw_cancelled":         "❌ Отменено. Окно не сохранено.",
        "mw_saved":
            "✅ <b>Окно обслуживания сохранено!</b>\n\n"
            "🏷 <b>{label}</b>\n"
            "🕐 {start} – {end}\n"
            "📆 {days_label}\n\n"
            "Уведомления не будут срабатывать в течение этого окна.\n"
            "Используй /maintenance для просмотра и удаления окон.",
        "mw_delete_not_found":  "⚠️ Окно не найдено или уже удалено.",
        "mw_deleted":
            "🗑 <b>{label}</b> удалено.\n\n"
            "Используй /maintenance для управления окнами.",
        "mw_cancel_fallback":   "❌ Отменено.",
        "mw_days_label_everyday":   "Каждый день",
        "mw_days_label_weekdays":   "Будни (Пн–Пт)",
        "mw_days_label_weekends":   "Выходные (Сб–Вс)",
        "mw_days_label_oneoff":     "Однократно (только сегодня)",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


def ut(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in utility locale for `lang`, falling back to English.

    Usage:
        from locales.utility_strings import ut
        ut("fr", "testalert_cooldown", remaining=45)
        ut("ru", "mw_saved", label="Backup", start="02:00", end="04:00", days_label="Пн–Пт")
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string