# web/server.py
import logging
from datetime import datetime, timezone
from aiohttp import web
from db.database import (
    get_status_page_by_slug,
    get_all_monitors,
    get_uptime_percent,
    is_pro,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

def _render_page(title: str, monitors: list, show_branding: bool) -> str:
    """Build the full HTML string for a status page."""

    # Overall health banner
    down_count = sum(1 for m in monitors if m["last_status"] == "down" and m["active"] == 1)
    if not monitors:
        banner_color = "#6b7280"
        banner_icon  = "⚪"
        banner_text  = "No monitors configured"
    elif down_count > 0:
        banner_color = "#ef4444"
        banner_icon  = "🔴"
        banner_text  = f"{down_count} monitor{'s' if down_count > 1 else ''} currently DOWN"
    else:
        banner_color = "#22c55e"
        banner_icon  = "🟢"
        banner_text  = "All systems operational"

    # Build monitor rows
    rows_html = ""
    for m in monitors:
        label      = m["label"] or m["url"]
        is_paused  = m["active"] == 2
        uptime_pct = get_uptime_percent(m["id"], days=7) if not is_paused else None

        if is_paused:
            dot_color   = "#9ca3af"
            status_text = "Paused"
            uptime_str  = "—"
        elif m["last_status"] == "up":
            dot_color   = "#22c55e"
            status_text = "Operational"
            uptime_str  = f"{uptime_pct}%"
        elif m["last_status"] == "down":
            dot_color   = "#ef4444"
            status_text = "Down"
            uptime_str  = f"{uptime_pct}%"
        else:
            dot_color   = "#9ca3af"
            status_text = "Pending"
            uptime_str  = "—"

        if m.get("last_checked"):
            try:
                last_dt = datetime.fromisoformat(m["last_checked"])
                diff    = datetime.now() - last_dt
                mins    = int(diff.total_seconds() // 60)
                if mins < 1:
                    ago = "just now"
                elif mins == 1:
                    ago = "1 min ago"
                elif mins < 60:
                    ago = f"{mins} mins ago"
                else:
                    ago = f"{mins // 60}h {mins % 60}m ago"
            except Exception:
                ago = "unknown"
        else:
            ago = "not checked yet"

        rows_html += f"""
        <div class="monitor-row">
            <div class="monitor-left">
                <span class="dot" style="background:{dot_color}"></span>
                <div class="monitor-info">
                    <span class="monitor-label">{_esc(label)}</span>
                    <span class="monitor-url">{_esc(m['url'])}</span>
                </div>
            </div>
            <div class="monitor-right">
                <span class="uptime-badge">{uptime_str} uptime</span>
                <span class="status-text" style="color:{dot_color}">{status_text}</span>
                <span class="checked-ago">checked {ago}</span>
            </div>
        </div>
        """

    branding_html = (
        '<footer><p>Powered by <a href="https://t.me/UptimeGuardBot" '
        'target="_blank">UptimeGuard</a></p></footer>'
    ) if show_branding else ""

    now_utc = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="60">
    <title>{_esc(title)}</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         Helvetica, Arial, sans-serif;
            background: #f9fafb;
            color: #111827;
            min-height: 100vh;
        }}

        .banner {{
            background: {banner_color};
            color: #fff;
            text-align: center;
            padding: 18px 24px;
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0.01em;
        }}

        .container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 40px 20px 60px;
        }}

        h1 {{
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 6px;
        }}

        .subtitle {{
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 32px;
        }}

        .monitors-card {{
            background: #fff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,.06);
        }}

        .monitor-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid #f3f4f6;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .monitor-row:last-child {{ border-bottom: none; }}

        .monitor-left {{
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
        }}

        .dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .monitor-info {{
            display: flex;
            flex-direction: column;
            min-width: 0;
        }}

        .monitor-label {{
            font-weight: 600;
            font-size: 0.95rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .monitor-url {{
            font-size: 0.78rem;
            color: #9ca3af;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 280px;
        }}

        .monitor-right {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 2px;
            flex-shrink: 0;
        }}

        .uptime-badge {{
            font-size: 0.78rem;
            font-weight: 600;
            color: #374151;
            background: #f3f4f6;
            padding: 2px 8px;
            border-radius: 20px;
        }}

        .status-text {{
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .checked-ago {{
            font-size: 0.72rem;
            color: #9ca3af;
        }}

        .empty-state {{
            text-align: center;
            padding: 40px 20px;
            color: #9ca3af;
            font-size: 0.95rem;
        }}

        footer {{
            text-align: center;
            margin-top: 40px;
            font-size: 0.78rem;
            color: #9ca3af;
        }}

        footer a {{ color: #6b7280; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}

        @media (max-width: 500px) {{
            .monitor-url {{ max-width: 180px; }}
        }}
    </style>
</head>
<body>
    <div class="banner">{banner_icon} {_esc(banner_text)}</div>
    <div class="container">
        <h1>{_esc(title)}</h1>
        <p class="subtitle">Last updated: {now_utc} &nbsp;·&nbsp; Auto-refreshes every 60s</p>

        <div class="monitors-card">
            {''.join([rows_html]) if monitors else '<div class="empty-state">No monitors to display.</div>'}
        </div>
    </div>
    {branding_html}
</body>
</html>"""


def _esc(text: str) -> str:
    """Minimal HTML escaping for user-provided strings."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Route handler
# ---------------------------------------------------------------------------

async def status_page_handler(request: web.Request) -> web.Response:
    slug = request.match_info.get("slug", "").strip()

    if not slug:
        raise web.HTTPNotFound()

    page = get_status_page_by_slug(slug)
    if not page:
        return web.Response(
            content_type="text/html",
            text=_not_found_html(),
            status=404
        )

    user_id  = page["user_id"]
    monitors = get_all_monitors(user_id)   # active + paused, not deleted
    pro      = is_pro(user_id)

    title          = page["title"] or "Status Page"
    show_branding  = not pro

    html = _render_page(title, monitors, show_branding)
    return web.Response(content_type="text/html", text=html)


def _not_found_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page Not Found</title>
    <style>
        body { font-family: system-ui, sans-serif; display: flex;
               align-items: center; justify-content: center;
               min-height: 100vh; margin: 0; background: #f9fafb; }
        .box { text-align: center; }
        h1 { font-size: 2rem; color: #111827; }
        p  { color: #6b7280; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>404 — Page not found</h1>
        <p>This status page doesn't exist or has been removed.</p>
    </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

async def start_web_server(app, port: int = 8080):
    """
    Call this from bot.py's post_init.
    Starts the aiohttp web server on the given port and
    stores the runner on bot_data so it can be shut down cleanly.
    """
    web_app  = web.Application()
    web_app.router.add_get("/status/{slug}", status_page_handler)
    web_app.router.add_get("/status/{slug}/", status_page_handler)  # trailing slash

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    app.bot_data["web_runner"] = runner
    logger.info(f"Status page server running on port {port}")


async def stop_web_server(app):
    """Call this from bot.py's post_stop."""
    runner = app.bot_data.get("web_runner")
    if runner:
        await runner.cleanup()
        logger.info("Status page server stopped.")
