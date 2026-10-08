const STYLE_ID = 'tool-ui-shell-styles';

export function injectToolShellStyles() {
  if (typeof document === 'undefined' || document.getElementById(STYLE_ID)) {
    return;
  }

  const styleSheet = document.createElement('style');
  styleSheet.id = STYLE_ID;
  styleSheet.type = 'text/css';
  styleSheet.innerText = `
    .tool-shell {
      padding: 20px;
      background: linear-gradient(180deg, #f6f8fc 0%, #eef3fb 100%);
      border-radius: 24px;
    }
    .tool-shell__card {
      max-width: 1080px;
      margin: 0 auto;
      border-radius: 24px;
      border: 1px solid #e6ecf5;
      overflow: hidden;
    }
    .tool-shell__inner {
      padding: 8px 8px 24px;
    }
    .tool-shell__hero {
      margin-bottom: 24px;
      padding: 24px;
      border-radius: 20px;
      color: #ffffff;
      box-shadow: 0 18px 40px rgba(37, 99, 235, 0.18);
    }
    .tool-shell__hero--blue {
      background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 45%, #60a5fa 100%);
    }
    .tool-shell__hero--teal {
      background: linear-gradient(135deg, #0f766e 0%, #0f766e 35%, #14b8a6 100%);
      box-shadow: 0 18px 40px rgba(15, 118, 110, 0.2);
    }
    .tool-shell__hero--violet {
      background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 48%, #a78bfa 100%);
      box-shadow: 0 18px 40px rgba(91, 33, 182, 0.2);
    }
    .tool-shell__hero--amber {
      background: linear-gradient(135deg, #b45309 0%, #d97706 50%, #f59e0b 100%);
      box-shadow: 0 18px 40px rgba(180, 83, 9, 0.2);
    }
    .tool-shell__hero-content {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      flex-wrap: wrap;
    }
    .tool-shell__eyebrow {
      font-size: 13px;
      letter-spacing: 1px;
      opacity: 0.82;
      margin-bottom: 8px;
    }
    .tool-shell__title {
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 10px;
    }
    .tool-shell__desc {
      font-size: 14px;
      line-height: 1.8;
      opacity: 0.94;
      max-width: 620px;
    }
    .tool-shell__stats {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .tool-shell__stat {
      min-width: 136px;
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(255,255,255,0.16);
      backdrop-filter: blur(8px);
    }
    .tool-shell__stat-label {
      font-size: 12px;
      opacity: 0.8;
      margin-bottom: 6px;
    }
    .tool-shell__stat-value {
      font-size: 18px;
      font-weight: 700;
    }
    .tool-shell__panel {
      height: 100%;
      padding: 20px;
      border-radius: 20px;
      border: 1px solid #dbe7f5;
      background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
    }
    .tool-shell__panel--soft {
      background: #f8fbff;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
    }
    .tool-shell__panel-title {
      font-size: 18px;
      font-weight: 700;
      color: #1f2937;
      margin-bottom: 6px;
    }
    .tool-shell__panel-desc {
      font-size: 13px;
      color: #6b7280;
      line-height: 1.7;
      margin-bottom: 18px;
    }
    .tool-shell__tip {
      margin-top: 8px;
      padding: 14px 16px;
      border-radius: 16px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      font-size: 13px;
      line-height: 1.8;
    }
    .tool-shell__tip--teal {
      background: #f0fdfa;
      border-color: #99f6e4;
      color: #0f766e;
    }
    .tool-shell__actions {
      margin-top: 18px;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      flex-wrap: wrap;
    }
    .tool-shell__primary-btn {
      min-width: 160px;
      height: 44px;
      border-radius: 14px;
      box-shadow: 0 12px 26px rgba(37, 99, 235, 0.18);
    }
    .tool-shell__primary-btn--teal {
      box-shadow: 0 12px 26px rgba(20, 184, 166, 0.2);
    }
    .tool-shell__result {
      margin-top: 20px;
      padding: 18px;
      border-radius: 20px;
      background: linear-gradient(180deg, #f8fbff 0%, #f2f7ff 100%);
      border: 1px solid #dbe7f5;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.72);
    }
    .tool-shell__result--teal {
      background: linear-gradient(180deg, #f7fcfb 0%, #eefaf7 100%);
      border-color: #d8eeea;
    }
    .tool-shell__result-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }
    .tool-shell__result-title {
      font-size: 18px;
      font-weight: 700;
      color: #1f2937;
      margin-bottom: 6px;
    }
    .tool-shell__result-desc {
      font-size: 13px;
      color: #6b7280;
    }
    .tool-shell__result-tag {
      padding: 8px 12px;
      border-radius: 999px;
      background: #dbeafe;
      color: #1d4ed8;
      font-size: 12px;
      border: 1px solid #bfdbfe;
    }
    .tool-shell__result--teal .tool-shell__result-tag {
      background: #ccfbf1;
      color: #0f766e;
      border-color: #99f6e4;
    }
    .tool-shell__result-body {
      padding: 12px;
      border-radius: 16px;
      background: rgba(255,255,255,0.82);
      border: 1px solid #e5edf8;
    }
    .tool-shell__result--teal .tool-shell__result-body {
      border-color: #dfeeea;
    }
    .tool-shell__stack {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .tool-shell__choice-card {
      height: 100%;
      padding: 14px 16px;
      border-radius: 16px;
      background: #ffffff;
      border: 1px solid #e5edf8;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
    }
    .tool-shell__choice-title {
      font-size: 14px;
      font-weight: 700;
      color: #1f2937;
    }
    .tool-shell__choice-desc {
      font-size: 12px;
      line-height: 1.7;
      color: #6b7280;
      white-space: normal;
    }
    .tool-shell__divider-space {
      height: 8px;
    }
    .tool-shell__card--compact {
      max-width: 1180px;
    }
    .tool-shell__inner--compact {
      padding: 8px 8px 20px;
    }
    .tool-shell__hero--compact {
      margin-bottom: 18px;
      padding: 20px 22px;
    }
    .tool-shell__compact-tabs {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .tool-shell__compact-tab {
      border: 1px solid #ecd7bd;
      background: linear-gradient(180deg, #fffdfa 0%, #fff7ed 100%);
      border-radius: 18px;
      padding: 14px 16px;
      text-align: left;
      cursor: pointer;
      transition: all .18s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .tool-shell__compact-tab:hover {
      transform: translateY(-1px);
      box-shadow: 0 12px 24px rgba(180, 83, 9, 0.1);
    }
    .tool-shell__compact-tab--active {
      background: linear-gradient(135deg, #92400e 0%, #c2410c 55%, #f59e0b 100%);
      border-color: transparent;
      color: #fff;
      box-shadow: 0 16px 28px rgba(146, 64, 14, 0.22);
    }
    .tool-shell__compact-tab-title {
      font-size: 15px;
      font-weight: 700;
    }
    .tool-shell__compact-tab-desc {
      font-size: 12px;
      line-height: 1.6;
      opacity: .82;
    }
    .tool-shell__compact-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
      gap: 16px;
      align-items: start;
    }
    .tool-shell__panel--compact,
    .tool-shell__result--compact {
      margin-top: 0;
      height: 100%;
    }
    .tool-shell__panel-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }
    .tool-shell__method-pill {
      border-radius: 999px;
      padding: 7px 10px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .08em;
      background: #fff3e0;
      color: #b45309;
      border: 1px solid #f6c98d;
    }
    .tool-shell__compact-form .el-form-item {
      margin-bottom: 14px;
    }
    .tool-shell__compact-fields {
      display: grid;
      gap: 14px;
    }
    .tool-shell__compact-fields--two {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .tool-shell__compact-fields--single {
      grid-template-columns: minmax(0, 1fr);
    }
    .tool-shell__actions--compact {
      margin-top: 14px;
    }
    @media (max-width: 980px) {
      .tool-shell__compact-grid {
        grid-template-columns: 1fr;
      }
    }
    @media (max-width: 720px) {
      .tool-shell__compact-fields--two {
        grid-template-columns: 1fr;
      }
    }
  `;
  document.head.appendChild(styleSheet);
}
