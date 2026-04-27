# locales/reports_strings.py
"""
Translation strings for handlers/reports.py and handlers/incidents.py.

Usage:
    from locales.reports_strings import rt
    rt("fr", "report_header")
    rt("es", "incident_down", duration="14 mins", started="3 Apr, 2:17 AM", error="Timeout")
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {

    # ── English ────────────────────────────────────────────────────────────
    "en": {
        # reports.py
        "report_no_monitors":   "No monitors found. Use /add to start.",
        "report_header":        "📊 <b>Uptime Report (Last 7 days)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 Uptime: <b>{uptime}%</b>\n"
            "   ⚡ Avg response: <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "N/A",

        # incidents.py — command entry
        "incidents_no_monitors":
            "You have no monitors yet. Use /add to add your first one.",
        "incidents_picker_title":
            "📋 <b>Incident Log</b>\n\nWhich monitor do you want to view?",
        "incidents_not_found":  "⚠️ Monitor not found.",

        # incidents.py — log rendering
        "incidents_title":      "📋 <b>Incident Log — {label}</b>",
        "incidents_subtitle":   "<i>Last {days} days</i>\n",
        "incidents_none":       "✅ No incidents recorded in this period.",
        "incidents_none_upsell":
            "\n<i>Free plan shows {free_days} days. "
            "Upgrade to Pro for 90-day history.</i>",
        "incident_ongoing":
            "🔴 <b>Ongoing</b> — started {started}\n"
            "   ⏱ Running for {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>Down {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…and {count} older incident{plural} not shown.</i>",
        "incidents_summary":
            "\n📊 <b>{count} incident{plural}</b> · "
            "<b>{total_down}</b> total downtime",
        "incidents_upsell":
            "\n<i>Free plan shows {free_days} days. "
            "Upgrade to Pro for 90-day history.</i>",
        "incidents_error_unknown": "Unknown error",
    },

    # ── French ─────────────────────────────────────────────────────────────
    "fr": {
        "report_no_monitors":   "Aucun moniteur trouvé. Utilise /add pour commencer.",
        "report_header":        "📊 <b>Rapport de disponibilité (7 derniers jours)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 Disponibilité : <b>{uptime}%</b>\n"
            "   ⚡ Réponse moy. : <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "N/D",
        "incidents_no_monitors":
            "Tu n'as pas encore de moniteurs. Utilise /add pour en ajouter un.",
        "incidents_picker_title":
            "📋 <b>Journal d'incidents</b>\n\nQuel moniteur veux-tu consulter ?",
        "incidents_not_found":  "⚠️ Moniteur introuvable.",
        "incidents_title":      "📋 <b>Journal d'incidents — {label}</b>",
        "incidents_subtitle":   "<i>{days} derniers jours</i>\n",
        "incidents_none":       "✅ Aucun incident enregistré sur cette période.",
        "incidents_none_upsell":
            "\n<i>Plan gratuit : {free_days} jours. "
            "Passe à Pro pour 90 jours d'historique.</i>",
        "incident_ongoing":
            "🔴 <b>En cours</b> — débuté le {started}\n"
            "   ⏱ En cours depuis {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>Panne de {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…et {count} incident{plural} plus ancien{plural} non affiché{plural}.</i>",
        "incidents_summary":
            "\n📊 <b>{count} incident{plural}</b> · "
            "<b>{total_down}</b> de panne au total",
        "incidents_upsell":
            "\n<i>Plan gratuit : {free_days} jours. "
            "Passe à Pro pour 90 jours d'historique.</i>",
        "incidents_error_unknown": "Erreur inconnue",
    },

    # ── Spanish ────────────────────────────────────────────────────────────
    "es": {
        "report_no_monitors":   "No se encontraron monitores. Usa /add para empezar.",
        "report_header":        "📊 <b>Informe de disponibilidad (últimos 7 días)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 Disponibilidad: <b>{uptime}%</b>\n"
            "   ⚡ Resp. promedio: <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "N/D",
        "incidents_no_monitors":
            "Aún no tienes monitores. Usa /add para añadir uno.",
        "incidents_picker_title":
            "📋 <b>Registro de incidentes</b>\n\n¿Qué monitor quieres ver?",
        "incidents_not_found":  "⚠️ Monitor no encontrado.",
        "incidents_title":      "📋 <b>Registro de incidentes — {label}</b>",
        "incidents_subtitle":   "<i>Últimos {days} días</i>\n",
        "incidents_none":       "✅ No se registraron incidentes en este período.",
        "incidents_none_upsell":
            "\n<i>Plan gratuito: {free_days} días. "
            "Actualiza a Pro para ver 90 días de historial.</i>",
        "incident_ongoing":
            "🔴 <b>En curso</b> — inicio {started}\n"
            "   ⏱ En curso hace {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>Caído {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…y {count} incidente{plural} anterior{plural} no mostrado{plural}.</i>",
        "incidents_summary":
            "\n📊 <b>{count} incidente{plural}</b> · "
            "<b>{total_down}</b> de tiempo de inactividad total",
        "incidents_upsell":
            "\n<i>Plan gratuito: {free_days} días. "
            "Actualiza a Pro para 90 días de historial.</i>",
        "incidents_error_unknown": "Error desconocido",
    },

    # ── Arabic ─────────────────────────────────────────────────────────────
    "ar": {
        "report_no_monitors":   "لم يُعثر على مراقبين. استخدم /add للبدء.",
        "report_header":        "📊 <b>تقرير التوفر (آخر 7 أيام)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 التوفر: <b>{uptime}%</b>\n"
            "   ⚡ متوسط الاستجابة: <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "غير متاح",
        "incidents_no_monitors":
            "ليس لديك مراقبون بعد. استخدم /add لإضافة واحد.",
        "incidents_picker_title":
            "📋 <b>سجل الحوادث</b>\n\nأي مراقب تريد عرضه؟",
        "incidents_not_found":  "⚠️ المراقب غير موجود.",
        "incidents_title":      "📋 <b>سجل الحوادث — {label}</b>",
        "incidents_subtitle":   "<i>آخر {days} أيام</i>\n",
        "incidents_none":       "✅ لا توجد حوادث مسجّلة في هذه الفترة.",
        "incidents_none_upsell":
            "\n<i>الخطة المجانية: {free_days} أيام. "
            "يُرقِّي إلى Pro للحصول على سجل 90 يوماً.</i>",
        "incident_ongoing":
            "🔴 <b>جارٍ</b> — بدأ {started}\n"
            "   ⏱ مستمر منذ {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>توقف لمدة {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…و{count} حادثة أقدم غير معروضة.</i>",
        "incidents_summary":
            "\n📊 <b>{count} حادثة</b> · "
            "<b>{total_down}</b> إجمالي وقت التوقف",
        "incidents_upsell":
            "\n<i>الخطة المجانية: {free_days} أيام. "
            "يُرقِّي إلى Pro للحصول على سجل 90 يوماً.</i>",
        "incidents_error_unknown": "خطأ غير معروف",
    },

    # ── Portuguese ─────────────────────────────────────────────────────────
    "pt": {
        "report_no_monitors":   "Nenhum monitor encontrado. Use /add para começar.",
        "report_header":        "📊 <b>Relatório de Disponibilidade (Últimos 7 dias)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 Disponibilidade: <b>{uptime}%</b>\n"
            "   ⚡ Resp. média: <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "N/D",
        "incidents_no_monitors":
            "Você ainda não tem monitores. Use /add para adicionar um.",
        "incidents_picker_title":
            "📋 <b>Registro de Incidentes</b>\n\nQual monitor você quer ver?",
        "incidents_not_found":  "⚠️ Monitor não encontrado.",
        "incidents_title":      "📋 <b>Registro de Incidentes — {label}</b>",
        "incidents_subtitle":   "<i>Últimos {days} dias</i>\n",
        "incidents_none":       "✅ Nenhum incidente registrado neste período.",
        "incidents_none_upsell":
            "\n<i>Plano gratuito: {free_days} dias. "
            "Atualize para Pro para ver 90 dias de histórico.</i>",
        "incident_ongoing":
            "🔴 <b>Em andamento</b> — iniciou {started}\n"
            "   ⏱ Em andamento há {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>Fora do ar por {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…e mais {count} incidente{plural} antigo{plural} não exibido{plural}.</i>",
        "incidents_summary":
            "\n📊 <b>{count} incidente{plural}</b> · "
            "<b>{total_down}</b> de tempo de inatividade total",
        "incidents_upsell":
            "\n<i>Plano gratuito: {free_days} dias. "
            "Atualize para Pro para 90 dias de histórico.</i>",
        "incidents_error_unknown": "Erro desconhecido",
    },

    # ── Russian ────────────────────────────────────────────────────────────
    "ru": {
        "report_no_monitors":   "Мониторов не найдено. Используй /add для начала.",
        "report_header":        "📊 <b>Отчёт о доступности (последние 7 дней)</b>\n\n",
        "report_row":
            "{icon} <b>{label}</b>\n"
            "   📈 Доступность: <b>{uptime}%</b>\n"
            "   ⚡ Среднее время ответа: <b>{avg_ms}ms</b>\n\n",
        "report_avg_na":        "Н/Д",
        "incidents_no_monitors":
            "У тебя пока нет мониторов. Используй /add для добавления.",
        "incidents_picker_title":
            "📋 <b>Журнал инцидентов</b>\n\nКакой монитор хочешь просмотреть?",
        "incidents_not_found":  "⚠️ Монитор не найден.",
        "incidents_title":      "📋 <b>Журнал инцидентов — {label}</b>",
        "incidents_subtitle":   "<i>Последние {days} дней</i>\n",
        "incidents_none":       "✅ Инцидентов за этот период не зафиксировано.",
        "incidents_none_upsell":
            "\n<i>Бесплатный план: {free_days} дней. "
            "Перейди на Pro для истории за 90 дней.</i>",
        "incident_ongoing":
            "🔴 <b>Продолжается</b> — начался {started}\n"
            "   ⏱ Длится {duration}\n"
            "   ❌ {error}",
        "incident_resolved":
            "⚫ <b>Недоступность {duration}</b> — {started}\n"
            "   ❌ {error}",
        "incidents_hidden":
            "\n<i>…и ещё {count} более старых инцидент(ов) не показано.</i>",
        "incidents_summary":
            "\n📊 <b>{count} инцидент(ов)</b> · "
            "<b>{total_down}</b> суммарного простоя",
        "incidents_upsell":
            "\n<i>Бесплатный план: {free_days} дней. "
            "Перейди на Pro для истории за 90 дней.</i>",
        "incidents_error_unknown": "Неизвестная ошибка",
    },
}

SUPPORTED_LANGS = set(_STRINGS.keys())
_FALLBACK       = "en"


def rt(lang: str, key: str, **kwargs) -> str:
    """
    Look up `key` in reports/incidents locale for `lang`, falling back to English.

    Usage:
        rt("fr", "report_header")
        rt("es", "incident_resolved", duration="14 mins", started="3 Abr, 2:17 AM", error="Timeout")
    """
    table  = _STRINGS.get(lang) or _STRINGS[_FALLBACK]
    string = table.get(key) or _STRINGS[_FALLBACK].get(key, f"[{key}]")
    return string.format(**kwargs) if kwargs else string
