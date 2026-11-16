"""CSS and small HTML fragments preserving the two source UI identities."""

BASE_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { font-family: 'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; font-synthesis:none; text-rendering:optimizeLegibility; }
html, body, [data-testid="stAppViewContainer"], .stApp { background: var(--app-bg) !important; color: var(--ink) !important; }
.stApp { font-family:'DM Sans',sans-serif !important; }
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer { visibility:hidden; height:0; }
[data-testid="stMainBlockContainer"] { max-width: 1440px; padding-top: 0.75rem; padding-bottom: 2.5rem; }
section[data-testid="stSidebar"] { background: var(--sidebar-bg) !important; border-right:1px solid var(--sidebar-line); }
section[data-testid="stSidebar"] > div { padding: 1.55rem 1.05rem 1.25rem; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { margin-bottom:0; }
section[data-testid="stSidebar"] [data-testid="stRadio"] > label { display:none; }
section[data-testid="stSidebar"] [role="radiogroup"] { gap:6px; }
section[data-testid="stSidebar"] [role="radiogroup"] label { padding:9px 11px; border-radius:8px; color:var(--sidebar-muted) !important; font-size:12px; font-weight:600; }
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background:var(--nav-active-bg); color:var(--nav-active-text) !important; }
section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display:none; }
section[data-testid="stSidebar"] [role="radiogroup"] label p { font-size:12px !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid var(--card-line) !important; border-radius:10px !important; background:#fff !important; box-shadow:0 2px 9px rgba(22,40,70,.025); }
[data-testid="stTextInput"] label, [data-testid="stNumberInput"] label { color:var(--label) !important; font-size:11px !important; font-weight:700 !important; padding-bottom:2px !important; }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input { color:#29384e !important; font-size:12px !important; }
div[data-baseweb="input"] { border-radius:6px !important; }
div[data-baseweb="input"] > div { border-color:#dfe5ed !important; background:#fff !important; min-height:39px; }
div[data-baseweb="input"]:focus-within > div { border-color:var(--primary) !important; box-shadow:0 0 0 2px color-mix(in srgb,var(--primary) 12%,transparent) !important; }
[data-testid="stTextInput"] [data-testid="InputInstructions"] { display:none; }
[data-testid="stButton"] > button { min-height:37px; border-radius:6px; border:1px solid var(--primary) !important; color:#fff !important; background:var(--primary) !important; font-size:11px !important; font-weight:700 !important; transition:all .15s ease; }
[data-testid="stButton"] > button:hover:not(:disabled) { border-color:var(--primary-dark) !important; background:var(--primary-dark) !important; }
[data-testid="stButton"] > button:disabled { opacity:.52; cursor:not-allowed; }
[data-testid="stButton"] > button[kind="secondary"] { color:var(--primary) !important; background:#fff !important; }
[data-testid="stButton"] > button[kind="secondary"]:hover:not(:disabled) { background:var(--nav-active-bg) !important; }
[data-testid="stCaptionContainer"] p { font-size:10px !important; color:var(--muted) !important; }
[data-testid="stAlert"] { font-size:12px; }
[data-testid="stProgress"] > div > div { background:var(--primary) !important; }
hr { border-color:var(--card-line) !important; }
.block-spacer { height:2px; }
.page-topbar { height:50px; display:flex; align-items:center; justify-content:space-between; padding:0 3px 10px; margin-bottom:24px; border-bottom:1px solid var(--card-line); color:var(--muted); font-size:11px; }
.page-topbar strong { color:var(--ink); font-weight:700; }
.page-wrap { max-width:1080px; margin:0 auto; padding:8px 12px 20px; }
.page-eyebrow { display:flex; align-items:center; gap:9px; color:var(--muted); font-size:9px; font-weight:700; letter-spacing:1.5px; }
.page-eyebrow .line { width:22px; height:1px; background:var(--card-line); }
.page-title { margin:10px 0 6px; color:var(--heading); font:800 29px 'Manrope',sans-serif; letter-spacing:-1.05px; line-height:1.2; }
.page-description { margin:0; color:var(--muted); font-size:12px; line-height:1.65; }
.demo-banner { display:flex; align-items:flex-start; gap:10px; margin:21px 0 22px; padding:12px 14px; border:1px solid #eadfbd; border-radius:8px; color:#78653e; background:#fffaf0; font-size:10px; line-height:1.6; }
.demo-banner strong { color:#665229; }
.demo-mark { display:grid; width:18px; height:18px; flex:0 0 18px; place-items:center; border-radius:50%; color:#fff; background:#b28b3e; font:700 11px/1 Georgia,serif; }
.stepper { display:flex; align-items:center; gap:15px; margin:26px 0 20px; padding:16px 21px; border:1px solid var(--card-line); border-radius:10px; background:#fff; }
.step { display:flex; align-items:center; gap:10px; min-width:0; }
.step-number { display:grid; width:26px; height:26px; flex:0 0 26px; place-items:center; border:1px solid #dce3ef; border-radius:50%; color:#8995a6; font-size:10px; font-weight:700; }
.step.active .step-number { color:#fff; border-color:#315ee8; background:#315ee8; box-shadow:0 0 0 4px #edf2ff; }
.step strong,.step small { display:block; white-space:nowrap; }
.step strong { color:#47566b; font-size:10px; font-weight:700; }
.step.active strong { color:#294fb9; }
.step small { margin-top:3px; color:#9aa4b2; font-size:9px; }
.step-connector { height:1px; flex:1; min-width:20px; background:#e7ebf1; }
.card-heading { display:flex; align-items:center; gap:12px; margin-bottom:17px; padding-bottom:15px; border-bottom:1px solid #eff2f6; }
.card-icon { display:grid; width:34px; height:34px; flex:0 0 34px; place-items:center; border-radius:9px; }
.card-icon svg { width:18px; height:18px; fill:none; stroke:currentColor; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; }
.applicant-icon { color:#4f6ed4; background:#eff3ff; }
.loan-icon { color:#218e76; background:#eaf8f4; }
.card-heading h2 { margin:0 0 4px; color:#263750; font:700 13px 'Manrope',sans-serif; }
.card-heading p { margin:0; color:#8b96a5; font-size:10px; }
.section-count { margin-left:auto; align-self:flex-start; color:#7e8ca3; font-size:9px; font-weight:700; letter-spacing:.7px; }
.field-help { margin-top:-8px; margin-bottom:4px; color:#929dac; font-size:9px; }
.field-error { margin-top:-6px; margin-bottom:4px; color:#c34e4e; font-size:10px; }
.amount-preview { margin-top:-8px; margin-bottom:3px; color:#929dac; font-size:10px; }
.privacy-note { display:flex; align-items:center; gap:9px; margin:17px 0 13px; padding:11px 13px; border:1px solid #e8edf3; border-radius:7px; color:#7e8b9d; background:#fafbfd; font-size:9px; line-height:1.55; }
.privacy-note strong { color:#56657a; }
.required-note { color:#929dac; font-size:9px; }
.form-actions { display:flex; justify-content:space-between; align-items:center; gap:15px; margin:10px 0 19px; }
.workflow-heading { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:15px; }
.workflow-heading h2 { margin:0 0 5px; color:#263750; font:700 13px 'Manrope',sans-serif; }
.workflow-heading p { margin:0; color:#8995a5; font-size:10px; line-height:1.55; }
.workflow-note { flex:0 0 auto; padding:6px 9px; border:1px solid #e6ebf5; border-radius:99px; color:#71809a; background:#f8faff; font-size:9px; font-weight:600; }
.manual-step-head { display:flex; align-items:center; gap:10px; margin:1px 0 7px; color:#34445b; font-size:10px; font-weight:700; }
.manual-step-no { display:grid; width:27px; height:27px; place-items:center; border:1px solid #dce4f2; border-radius:50%; color:#5d76c7; background:#f2f5ff; font-size:9px; }
.manual-step-head.complete .manual-step-no { border-color:#1d9b6e; color:#fff; background:#1d9b6e; }
.manual-step-head.error .manual-step-no { border-color:#cc5555; color:#fff; background:#cc5555; }
.manual-step-head.locked { opacity:.5; }
.manual-hint { margin:0 0 8px; color:#9aa4b2; font-size:9px; min-height:14px; }
.manual-hint.complete { color:#16845e; }
.manual-hint.error { color:#c34e4e; }
.manual-message { margin:12px 0 0; color:#8a96a6; font-size:10px; line-height:1.55; }
.manual-response { margin-top:12px; padding:12px 13px; border:1px solid #dce9e2; border-radius:7px; background:#fbfefc; }
.manual-response.error { border-color:#f0dada; background:#fffafa; }
.manual-response-title { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:8px; color:#33445b; font-size:10px; font-weight:700; }
.manual-response-meta { color:#8793a4; font-size:9px; font-weight:400; }
.manual-response pre { max-height:220px; overflow:auto; margin:0; padding:10px; border-radius:5px; color:#dce6f6; background:#17243a; font:9px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace; white-space:pre-wrap; overflow-wrap:anywhere; }
.progress-card { margin:18px 0; padding:19px 21px 16px; border:1px solid #e5ebf4; border-radius:10px; background:#fff; box-shadow:0 2px 8px rgba(25,45,80,.025); }
.progress-heading { display:flex; align-items:center; justify-content:space-between; gap:15px; margin-bottom:14px; }
.progress-eyebrow { display:block; margin-bottom:5px; color:#8b97a9; font-size:8px; font-weight:700; letter-spacing:1.25px; }
.progress-title { margin:0; color:#263750; font:700 13px 'Manrope',sans-serif; }
.progress-counter { color:#6f7d91; font-size:10px; font-weight:700; white-space:nowrap; }
.progress-track { height:6px; overflow:hidden; margin-bottom:17px; border-radius:99px; background:#edf1f6; }
.progress-fill { height:100%; border-radius:99px; transition:width .28s ease; background:#315ee8; }
.progress-fill.complete { background:#1d9b6e; }
.progress-fill.error { background:#cc5555; }
.progress-steps { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
.progress-step { display:flex; align-items:flex-start; gap:8px; min-width:0; color:#8793a5; }
.progress-indicator { display:grid; width:23px; height:23px; flex:0 0 23px; place-items:center; border:1px solid #dce3ed; border-radius:50%; color:#8793a5; background:#fff; font-size:9px; font-weight:700; }
.progress-label { padding-top:3px; color:#8793a5; font-size:9px; font-weight:600; line-height:1.45; }
.progress-step.active .progress-indicator { border-color:#315ee8; color:#fff; background:#315ee8; box-shadow:0 0 0 3px #edf2ff; }
.progress-step.active .progress-label { color:#315ee8; }
.progress-step.complete .progress-indicator { border-color:#1d9b6e; color:#fff; background:#1d9b6e; }
.progress-step.complete .progress-label { color:#16845e; }
.progress-step.error .progress-indicator { border-color:#cc5555; color:#fff; background:#cc5555; }
.progress-step.error .progress-label { color:#c34e4e; }
.progress-message { margin:13px 0 0; color:#8a96a6; font-size:9px; }
.response-card { margin:16px 0; padding:17px 19px; border:1px solid #dce9e2; border-radius:9px; background:#fbfefc; }
.response-card.error { border-color:#f0dada; background:#fffafa; }
.response-title { margin:0 0 5px; color:#263750; font:700 13px 'Manrope',sans-serif; }
.response-summary { margin:0 0 8px; color:#768496; font-size:11px; line-height:1.55; }
.response-meta { color:#8793a4; font-size:9px; }
.response-raw { margin-top:10px; }
.response-raw summary { color:#6f7d91; cursor:pointer; font-size:10px; }
.response-raw pre { max-height:260px; overflow:auto; margin-top:7px; padding:11px; border-radius:6px; color:#dce6f6; background:#17243a; font:9px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace; white-space:pre-wrap; overflow-wrap:anywhere; }
.page-footer { display:flex; justify-content:space-between; gap:15px; margin-top:27px; padding-top:15px; border-top:1px solid var(--card-line); color:#9aa4b2; font-size:9px; }
/* Operations portal styling */
.ops-heading { margin:0 0 6px; color:#1d3429; font:800 27px 'Manrope',sans-serif; letter-spacing:-.9px; }
.ops-eyebrow { color:#6f8979; font-size:8px; font-weight:700; letter-spacing:1.5px; }
.ops-description { margin:0; color:#76857d; font-size:11px; line-height:1.6; }
.ops-demo-banner { display:flex; align-items:flex-start; gap:10px; margin:0 0 22px; padding:12px 14px; border:1px solid #e9dfc5; border-radius:7px; color:#786b4e; background:#fcf8ee; font-size:9px; line-height:1.55; }
.ops-demo-banner strong { color:#645635; }
.ops-environment { padding:6px 9px; border:1px solid #dfe9e2; border-radius:20px; color:#567a65; background:#f8fcf9; font-size:8px; font-weight:700; letter-spacing:.9px; }
.ops-panel-heading { display:flex; align-items:center; justify-content:space-between; gap:15px; margin-bottom:13px; padding-bottom:14px; border-bottom:1px solid #e8eee9; }
.ops-panel-heading h2 { margin:0; color:#2c4036; font:700 13px 'Manrope',sans-serif; }
.ops-panel-kicker { display:block; margin-bottom:5px; color:#779182; font-size:8px; font-weight:700; letter-spacing:1.25px; }
.ops-panel-note { color:#87958d; font-size:9px; }
.ops-table-wrap { width:100%; overflow-x:auto; }
.ops-table { width:100%; border-collapse:collapse; text-align:left; white-space:nowrap; }
.ops-table th { padding:12px 13px; border-bottom:1px solid #e5ece7; color:#75867c; background:#f7faf8; font-size:9px; font-weight:700; }
.ops-table td { padding:13px; border-bottom:1px solid #edf2ee; color:#33463c; font-size:10px; }
.ops-table tbody tr:last-child td { border-bottom:0; }
.ops-table tbody tr:hover { background:#fbfdfb; }
.ops-panel-footer { display:flex; justify-content:space-between; gap:12px; margin:13px -3px -2px; padding-top:11px; border-top:1px solid #e8eee9; color:#8a9890; font-size:8px; }
.ops-footer { display:flex; justify-content:space-between; gap:15px; margin-top:20px; color:#98a49d; font-size:8px; }
@media(max-width:800px) { .page-wrap { padding-left:0; padding-right:0; }.stepper { gap:7px; padding:13px 10px; }.step { gap:6px; }.step strong { font-size:9px; }.step small { font-size:8px; }.progress-steps { grid-template-columns:repeat(2,minmax(0,1fr)); row-gap:13px; } }
@media(max-width:560px) { [data-testid="stMainBlockContainer"] { padding-left:1rem; padding-right:1rem; }.page-title { font-size:24px; }.stepper { gap:5px; padding:12px 8px; }.step { gap:5px; }.step-number { width:23px; height:23px; flex-basis:23px; }.step strong { font-size:8px; }.step small { display:none; }.step-connector { min-width:7px; }.progress-steps { grid-template-columns:1fr; gap:10px; }.workflow-heading { flex-direction:column; gap:8px; }.form-actions,.page-footer,.ops-panel-footer,.ops-footer { flex-direction:column; align-items:flex-start; } }
"""


def theme_css(operations: bool = False) -> str:
    if operations:
        vars_css = """
        :root { --app-bg:#f3f6f4; --sidebar-bg:#13251f; --sidebar-line:#20382e; --sidebar-muted:#a9beb2; --nav-active-bg:rgba(119,180,145,.14); --nav-active-text:#eaf6ee; --ink:#1e2d29; --heading:#1d3429; --muted:#76857d; --label:#40554a; --card-line:#dfe7e2; --primary:#247a5a; --primary-dark:#1d674b; }
        """
        return BASE_CSS + vars_css
    vars_css = """
    :root { --app-bg:#f5f7fb; --sidebar-bg:#ffffff; --sidebar-line:#e9edf3; --sidebar-muted:#69778a; --nav-active-bg:#eff3ff; --nav-active-text:#2f5bdd; --ink:#182230; --heading:#182b49; --muted:#7d8999; --label:#48566a; --card-line:#e8edf3; --primary:#315ee8; --primary-dark:#244dce; }
    """
    return BASE_CSS + vars_css


def loandesk_brand() -> str:
    return """
    <div style="display:flex;align-items:center;gap:11px;padding:0 11px;color:#172b4d;font:800 22px 'Manrope',sans-serif;letter-spacing:-1.2px">
      <span style="width:27px;height:27px;display:flex;align-items:flex-end;gap:3px;padding:5px;border-radius:8px;background:#315ee8">
        <i style="display:block;width:4px;height:8px;border-radius:3px;background:#fff;opacity:.75"></i><i style="display:block;width:4px;height:13px;border-radius:3px;background:#fff"></i><i style="display:block;width:4px;height:17px;border-radius:3px;background:#fff;opacity:.85"></i>
      </span><span>loan<span style="color:#6880a5;font-weight:500">desk</span></span>
    </div>
    <div style="margin:53px 12px 13px;color:#9aa4b3;font-size:10px;font-weight:700;letter-spacing:1.35px">WORKSPACE</div>
    """


def operations_brand() -> str:
    return """
    <div style="display:flex;align-items:center;gap:11px;padding:0 10px;color:#f7fbf8">
      <span style="display:grid;width:36px;height:36px;place-items:center;border-radius:10px;color:#142c22;background:#9fd3b4;font:800 11px 'Manrope',sans-serif">LO</span>
      <span><strong style="display:block;font:800 19px 'Manrope',sans-serif;letter-spacing:-.8px">lending</strong><small style="display:block;margin-top:2px;color:#8fa99b;font-size:8px;font-weight:700;letter-spacing:2px">OPERATIONS</small></span>
    </div>
    <div style="margin:58px 12px 13px;color:#769184;font-size:9px;font-weight:700;letter-spacing:1.45px">WORKSPACE</div>
    """
