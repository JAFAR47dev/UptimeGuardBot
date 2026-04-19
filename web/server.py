# web/server.py
import logging
from datetime import datetime
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

    active_monitors = [m for m in monitors if m["active"] == 1]
    down_count      = sum(1 for m in active_monitors if m["last_status"] == "down")

    if not monitors:
        overall_status  = "no-data"
        status_label    = "No Monitors"
        status_sublabel = "Add monitors to start tracking"
    elif down_count > 0:
        overall_status  = "degraded"
        status_label    = "Service Disruption"
        status_sublabel = f"{down_count} monitor{'s' if down_count > 1 else ''} currently down"
    else:
        overall_status  = "operational"
        status_label    = "All Systems Operational"
        status_sublabel = f"All {len(active_monitors)} monitors are healthy"

    rows_html = ""
    for m in monitors:
        label      = m.get("label") or m.get("url", "")
        url        = m.get("url", "")
        is_paused  = m["active"] == 2
        uptime_pct = get_uptime_percent(m["id"], days=7) if not is_paused else None

        if is_paused:
            state       = "paused"
            status_text = "Paused"
            uptime_str  = "—"
        elif m.get("last_status") == "up":
            state       = "up"
            status_text = "Operational"
            uptime_str  = f"{uptime_pct}%"
        elif m.get("last_status") == "down":
            state       = "down"
            status_text = "Outage"
            uptime_str  = f"{uptime_pct}%"
        else:
            state       = "pending"
            status_text = "Pending"
            uptime_str  = "—"

        last_checked = m.get("last_checked")
        if last_checked:
            try:
                last_dt = datetime.fromisoformat(last_checked)
                diff    = datetime.now() - last_dt
                mins    = int(diff.total_seconds() // 60)
                if mins < 1:
                    ago = "just now"
                elif mins == 1:
                    ago = "1m ago"
                elif mins < 60:
                    ago = f"{mins}m ago"
                else:
                    hrs = mins // 60
                    ago = f"{hrs}h {mins % 60}m ago"
            except Exception:
                ago = "—"
        else:
            ago = "not yet"

        # Uptime bar — 30 segments
        bar_html = _uptime_bar(uptime_pct, state)

        rows_html += f"""
        <div class="monitor-row" data-state="{state}">
            <div class="monitor-main">
                <div class="monitor-identity">
                    <div class="state-indicator">
                        <span class="pulse-ring"></span>
                        <span class="state-dot"></span>
                    </div>
                    <div class="monitor-text">
                        <span class="monitor-name">{_esc(label)}</span>
                        <span class="monitor-url">{_esc(url)}</span>
                    </div>
                </div>
                <div class="monitor-meta">
                    <div class="uptime-info">
                        <span class="uptime-value">{uptime_str}</span>
                        <span class="uptime-label">7d uptime</span>
                    </div>
                    <div class="status-pill" data-state="{state}">{status_text}</div>
                    <span class="check-time">↺ {ago}</span>
                </div>
            </div>
            <div class="uptime-bar-row">
                {bar_html}
                <span class="bar-label">30 days</span>
            </div>
        </div>"""

    branding_html = ""
    if show_branding:
        branding_html = """
        <div class="branding">
            <span>Powered by</span>
            <a href="https://t.me/UptimeGuardBot" target="_blank" rel="noopener">
                UptimeGuard
            </a>
        </div>"""

    now_utc   = datetime.now().strftime("%d %b %Y · %H:%M UTC")
    mon_count = len(monitors)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="60">
    <title>{_esc(title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg:        #0a0c0f;
            --surface:   #111418;
            --border:    #1e2328;
            --border-2:  #252a30;
            --text-1:    #e8eaed;
            --text-2:    #8b9099;
            --text-3:    #555b63;
            --green:     #00d084;
            --green-dim: #00d08420;
            --red:       #ff4444;
            --red-dim:   #ff444420;
            --amber:     #f5a623;
            --amber-dim: #f5a62320;
            --blue:      #4a9eff;
            --mono:      "IBM Plex Mono", monospace;
            --sans:      "IBM Plex Sans", sans-serif;
        }}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: var(--sans);
            background: var(--bg);
            color: var(--text-1);
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }}

        /* ── Scanline overlay ── */
        body::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(255,255,255,.012) 2px,
                rgba(255,255,255,.012) 4px
            );
            pointer-events: none;
            z-index: 0;
        }}

        /* ── Top bar ── */
        .topbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border);
            background: rgba(10,12,15,.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            height: 52px;
        }}

        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .topbar-logo {{
            font-family: var(--mono);
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .topbar-sep {{
            width: 1px;
            height: 16px;
            background: var(--border-2);
        }}

        .topbar-page-title {{
            font-size: 0.82rem;
            color: var(--text-2);
            font-weight: 400;
        }}

        .topbar-right {{
            font-family: var(--mono);
            font-size: 0.72rem;
            color: var(--text-3);
        }}

        /* ── Status hero ── */
        .hero {{
            position: relative;
            z-index: 1;
            padding: 56px 24px 48px;
            text-align: center;
            border-bottom: 1px solid var(--border);
            overflow: hidden;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(
                ellipse 60% 50% at 50% 0%,
                var(--glow-color, rgba(0,208,132,.06)) 0%,
                transparent 70%
            );
            pointer-events: none;
        }}

        .hero[data-status="operational"]  {{ --glow-color: rgba(0,208,132,.08); }}
        .hero[data-status="degraded"]     {{ --glow-color: rgba(255,68,68,.08); }}
        .hero[data-status="no-data"]      {{ --glow-color: rgba(139,144,153,.05); }}

        .status-orb {{
            width: 56px;
            height: 56px;
            border-radius: 50%;
            margin: 0 auto 20px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .status-orb::before {{
            content: "";
            position: absolute;
            inset: -6px;
            border-radius: 50%;
            opacity: .25;
            animation: orb-pulse 3s ease-in-out infinite;
        }}

        .status-orb::after {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 50%;
            opacity: .15;
        }}

        [data-status="operational"] .status-orb {{
            background: radial-gradient(circle at 35% 35%, #00ff9d, var(--green));
            box-shadow: 0 0 24px rgba(0,208,132,.4);
        }}
        [data-status="operational"] .status-orb::before {{
            background: var(--green);
        }}

        [data-status="degraded"] .status-orb {{
            background: radial-gradient(circle at 35% 35%, #ff7070, var(--red));
            box-shadow: 0 0 24px rgba(255,68,68,.4);
        }}
        [data-status="degraded"] .status-orb::before {{
            background: var(--red);
        }}

        [data-status="no-data"] .status-orb {{
            background: radial-gradient(circle at 35% 35%, #9ca3af, #6b7280);
        }}

        @keyframes orb-pulse {{
            0%, 100% {{ transform: scale(1); opacity: .25; }}
            50%        {{ transform: scale(1.3); opacity: .1; }}
        }}

        .hero-status {{
            font-size: 1.6rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            margin-bottom: 6px;
        }}

        .hero-sub {{
            font-size: 0.88rem;
            color: var(--text-2);
            font-weight: 300;
        }}

        .hero-stats {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 32px;
        }}

        .hero-stat {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }}

        .hero-stat-value {{
            font-family: var(--mono);
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-1);
        }}

        .hero-stat-label {{
            font-size: 0.72rem;
            color: var(--text-3);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        /* ── Main content ── */
        .container {{
            position: relative;
            z-index: 1;
            max-width: 760px;
            margin: 0 auto;
            padding: 40px 20px 80px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}

        .section-title {{
            font-family: var(--mono);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-3);
        }}

        .section-count {{
            font-family: var(--mono);
            font-size: 0.7rem;
            color: var(--text-3);
        }}

        /* ── Monitor card ── */
        .monitors-list {{
            display: flex;
            flex-direction: column;
            gap: 1px;
            background: var(--border);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}

        .monitor-row {{
            background: var(--surface);
            padding: 16px 20px;
            transition: background .15s;
        }}

        .monitor-row:hover {{
            background: #13171c;
        }}

        .monitor-main {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .monitor-identity {{
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
        }}

        /* ── State indicator ── */
        .state-indicator {{
            position: relative;
            width: 14px;
            height: 14px;
            flex-shrink: 0;
        }}

        .state-dot {{
            position: absolute;
            inset: 2px;
            border-radius: 50%;
        }}

        .pulse-ring {{
            position: absolute;
            inset: 0;
            border-radius: 50%;
            animation: none;
        }}

        [data-state="up"] .state-dot    {{ background: var(--green); box-shadow: 0 0 6px rgba(0,208,132,.6); }}
        [data-state="down"] .state-dot  {{ background: var(--red);   box-shadow: 0 0 6px rgba(255,68,68,.6); }}
        [data-state="paused"] .state-dot {{ background: var(--text-3); }}
        [data-state="pending"] .state-dot {{ background: var(--amber); }}

        [data-state="up"] .pulse-ring {{
            border: 1.5px solid var(--green);
            animation: ring-pulse 2.5s ease-out infinite;
        }}
        [data-state="down"] .pulse-ring {{
            border: 1.5px solid var(--red);
            animation: ring-pulse 1.5s ease-out infinite;
        }}

        @keyframes ring-pulse {{
            0%   {{ transform: scale(1);   opacity: .8; }}
            70%  {{ transform: scale(2.2); opacity: 0; }}
            100% {{ transform: scale(2.2); opacity: 0; }}
        }}

        .monitor-text {{
            display: flex;
            flex-direction: column;
            gap: 1px;
            min-width: 0;
        }}

        .monitor-name {{
            font-weight: 500;
            font-size: 0.92rem;
            color: var(--text-1);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .monitor-url {{
            font-family: var(--mono);
            font-size: 0.7rem;
            color: var(--text-3);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 260px;
        }}

        .monitor-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
            flex-shrink: 0;
        }}

        .uptime-info {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 1px;
        }}

        .uptime-value {{
            font-family: var(--mono);
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-1);
        }}

        .uptime-label {{
            font-size: 0.65rem;
            color: var(--text-3);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .status-pill {{
            font-family: var(--mono);
            font-size: 0.68rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border: 1px solid transparent;
        }}

        .status-pill[data-state="up"]      {{ color: var(--green); background: var(--green-dim);  border-color: rgba(0,208,132,.2); }}
        .status-pill[data-state="down"]    {{ color: var(--red);   background: var(--red-dim);    border-color: rgba(255,68,68,.2); }}
        .status-pill[data-state="paused"]  {{ color: var(--text-3); background: rgba(85,91,99,.15); border-color: var(--border-2); }}
        .status-pill[data-state="pending"] {{ color: var(--amber);  background: var(--amber-dim);  border-color: rgba(245,166,35,.2); }}

        .check-time {{
            font-family: var(--mono);
            font-size: 0.68rem;
            color: var(--text-3);
            white-space: nowrap;
        }}

        /* ── Uptime bar ── */
        .uptime-bar-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
        }}

        .uptime-bar {{
            display: flex;
            gap: 2px;
            flex: 1;
        }}

        .bar-seg {{
            flex: 1;
            height: 20px;
            border-radius: 2px;
            transition: opacity .15s;
        }}

        .bar-seg:hover {{ opacity: .8; }}

        .bar-seg.seg-up      {{ background: var(--green); opacity: .7; }}
        .bar-seg.seg-down    {{ background: var(--red); }}
        .bar-seg.seg-empty   {{ background: var(--border-2); }}

        .bar-label {{
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--text-3);
            white-space: nowrap;
        }}

        /* ── Empty state ── */
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-3);
            font-size: 0.88rem;
            font-family: var(--mono);
            background: var(--surface);
        }}

        /* ── Footer ── */
        .page-footer {{
            position: relative;
            z-index: 1;
            border-top: 1px solid var(--border);
            padding: 20px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .footer-meta {{
            font-family: var(--mono);
            font-size: 0.68rem;
            color: var(--text-3);
        }}

        .branding {{
            font-family: var(--mono);
            font-size: 0.68rem;
            color: var(--text-3);
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .branding a {{
            color: var(--text-2);
            text-decoration: none;
            border-bottom: 1px solid var(--border-2);
            padding-bottom: 1px;
            transition: color .15s, border-color .15s;
        }}

        .branding a:hover {{
            color: var(--text-1);
            border-color: var(--text-3);
        }}

        /* ── Responsive ── */
        @media (max-width: 540px) {{
            .monitor-meta {{ gap: 10px; }}
            .check-time   {{ display: none; }}
            .monitor-url  {{ max-width: 160px; }}
            .hero-stats   {{ gap: 20px; }}
            .topbar-page-title {{ display: none; }}
        }}

        @media (max-width: 400px) {{
            .uptime-info {{ display: none; }}
        }}
    </style>
</head>
<body>

    <!-- Top bar -->
    <header class="topbar">
        <div class="topbar-left">
            <span class="topbar-logo">UptimeGuard</span>
            <div class="topbar-sep"></div>
            <span class="topbar-page-title">{_esc(title)}</span>
        </div>
        <span class="topbar-right">{now_utc}</span>
    </header>

    <!-- Hero -->
    <div class="hero" data-status="{overall_status}">
        <div class="status-orb"></div>
        <h1 class="hero-status">{status_label}</h1>
        <p class="hero-sub">{status_sublabel}</p>
        <div class="hero-stats">
            <div class="hero-stat">
                <span class="hero-stat-value">{mon_count}</span>
                <span class="hero-stat-label">Monitors</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-value">{len(active_monitors) - down_count}</span>
                <span class="hero-stat-label">Online</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-value">{down_count}</span>
                <span class="hero-stat-label">Down</span>
            </div>
        </div>
    </div>

    <!-- Monitor list -->
    <div class="container">
        <div class="section-header">
            <span class="section-title">Services</span>
            <span class="section-count">{mon_count} total</span>
        </div>
        <div class="monitors-list">
            {''.join([rows_html]) if monitors else '<div class="empty-state">// no monitors configured</div>'}
        </div>
    </div>

    <!-- Footer -->
    <footer class="page-footer">
        <span class="footer-meta">auto-refreshes every 60s</span>
        {branding_html}
    </footer>

</body>
</html>"""


def _uptime_bar(uptime_pct, state: str) -> str:
    """Generate 30 bar segments. Without real per-day data we approximate."""
    segments = 30
    if uptime_pct is None or state == "paused":
        segs = [f'<div class="bar-seg seg-empty"></div>'] * segments
    else:
        # Fill proportionally — down segments at the end for visual drama
        up_count   = round((uptime_pct / 100) * segments)
        down_count = segments - up_count
        segs = (
            [f'<div class="bar-seg seg-up"></div>'] * up_count +
            [f'<div class="bar-seg seg-down"></div>'] * down_count
        )
    return f'<div class="uptime-bar">{"".join(segs)}</div>'


def _esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Route handlers
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

    user_id       = page["user_id"]
    monitors      = get_all_monitors(user_id)
    pro           = is_pro(user_id)
    title         = page["title"] or "Status Page"
    show_branding = not pro

    html = _render_page(title, monitors, show_branding)
    return web.Response(content_type="text/html", text=html)


def _not_found_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Not Found — UptimeGuard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #0a0c0f; --text-1: #e8eaed; --text-2: #8b9099; --mono: "IBM Plex Mono", monospace; }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--mono);
            background: var(--bg);
            color: var(--text-1);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .box { text-align: center; }
        .code { font-size: 4rem; font-weight: 600; color: #1e2328; margin-bottom: 12px; }
        .msg  { font-size: 0.88rem; color: var(--text-2); }
        .sub  { font-size: 0.72rem; color: #555b63; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="code">404</div>
        <p class="msg">Status page not found</p>
        <p class="sub">This page doesn't exist or has been removed.</p>
    </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

async def start_web_server(app, port: int = 8080):
    web_app = web.Application()
    web_app.router.add_get("/status/{slug}",  status_page_handler)
    web_app.router.add_get("/status/{slug}/", status_page_handler)

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    app.bot_data["web_runner"] = runner
    logger.info(f"Status page server running on port {port}")


async def stop_web_server(app):
    runner = app.bot_data.get("web_runner")
    if runner:
        await runner.cleanup()
        logger.info("Status page server stopped.")
