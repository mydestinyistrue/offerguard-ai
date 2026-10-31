# OfferGuard AI — Frontend Client (PWA)

The frontend client for **OfferGuard AI** is a responsive, mobile-first Progressive Web Application (PWA) built with **React 19**, **Vite**, and **TailwindCSS**. It provides an interactive forensic dashboard for detecting task scams, inspecting scam progression stages, performing in-browser zero-retention OCR, and generating official 1930 Cybercrime Helpline FIR complaint packs.

---

## Table of Contents

- [Features](#features)
  - [Client-Side In-Browser OCR](#client-side-in-browser-ocr)
  - [Interactive Scam-Stage Radar](#interactive-scam-stage-radar)
  - [Instant Evidence Breakdown & Signal Quotes](#instant-evidence-breakdown--signal-quotes)
  - [One-Tap Helpline 1930 FIR Generator](#one-tap-helpline-1930-fir-generator)
  - [Trilingual Localization](#trilingual-localization)
  - [Dark & Light Theme Support](#dark--light-theme-support)
- [Project Structure](#project-structure)
- [Components Architecture](#components-architecture)
- [Global Contexts](#global-contexts)
- [Environment Setup](#environment-setup)
- [Installation & Running Locally](#installation--running-locally)
  - [Prerequisites](#prerequisites)
  - [Development Server](#development-server)
  - [Production Build](#production-build)
- [API Proxy & Integration](#api-proxy--integration)

---

## Features

### Client-Side In-Browser OCR
- Powered by **Tesseract.js WebAssembly (WASM)**.
- Performs $2\times$ canvas scaling, grayscale conversion, and threshold contrast enhancement directly inside the browser.
- **Zero Server Retention:** Image data never leaves the client's device, ensuring sensitive personal chat screenshots remain private.

### Interactive Scam-Stage Radar
- Visualizes the 5-stage social engineering progression:
  - **Stage 0:** Bait Solicitation
  - **Stage 1:** Trust Hook & Small Payout
  - **Stage 2:** Prepaid Task Deposit Trap
  - **Stage 3:** Withdrawal Lock-In & Tax Extortion
  - **Stage 4:** Exit Scam & Communication Blackout
- Displays real-time predictive warnings on what psychological tactic the scammer will use next (`NextMoveCard`).
- For genuine offers, the radar gracefully indicates `No Scam` with a clean emerald badge and pinned 0% state.

### Instant Evidence Breakdown & Signal Quotes
- Highlights exact suspicious phrases extracted from the conversation (e.g., upfront payment demands, Telegram migration, crypto tasks).
- Badges detected signals by severity and forensic category.

### One-Tap Helpline 1930 FIR Generator
- Extracts suspect UPI IDs, phone numbers, and defrauded amounts.
- Prepares a formatted criminal complaint draft ready for copy-pasting into the National Cyber Crime Reporting Portal (`cybercrime.gov.in`).
- Provides one-click calling to emergency helpline `1930`.

### Trilingual Localization
- Full user interface and forensic advice available in:
  - **English**
  - **Hindi (हिन्दी)**
  - **Punjabi (ਪੰਜਾਬੀ)**

### Dark & Light Theme Support
- Persistent theme selection stored in `localStorage`.
- High-contrast color palette optimized for accessibility and low-light environments.

---

## Project Structure

```bash
frontend/
├── index.html                   # HTML5 shell & PWA entry point
├── package.json                 # Node dependencies & scripts
├── vite.config.js               # Vite config with /api reverse proxy
├── eslint.config.js             # Linting and style rules
├── public/                      # Public static assets
│   ├── emblem.png               # National emblem graphic
│   ├── favicon.ico              # Standard favicon
│   ├── favicon.png              # High-res PNG favicon
│   ├── favicon.svg              # Vector favicon
│   ├── icons.svg                # SVG sprites
│   ├── logo.jpg                 # Brand graphic
│   └── logo.png                 # Main logo
└── src/
    ├── App.jsx                  # Main router & layout shell
    ├── App.css                  # Custom component styling
    ├── main.jsx                 # React DOM mount point
    ├── index.css                # TailwindCSS design directives
    ├── assets/                  # Bundled assets (emblem, hero, logo)
    ├── components/              # Modular UI components
    │   ├── AdviceSection.jsx    # Actionable victim defense guidance & golden hour steps
    │   ├── CompanyCheck.jsx     # MCA registry match & domain risk badges
    │   ├── EvidenceCard.jsx     # Extracted suspicious quotes with severity tags
    │   ├── Footer.jsx           # Legal disclosures, Helpline 1930 links & credits
    │   ├── Navbar.jsx           # Header navigation, language & dark/light theme switch
    │   ├── NextMoveCard.jsx     # Predictive scammer psychology forecaster
    │   ├── ReportPack.jsx       # 1930 FIR dossier generator & one-tap export
    │   ├── RiskGauge.jsx        # SVG circular risk score visualizer (0–100)
    │   ├── StageTimeline.jsx    # 5-stage monotonic scam progression radar
    │   └── VerdictBanner.jsx    # Dynamic risk banner (Scam, Suspicious, Genuine)
    ├── context/                 # Global state contexts
    │   ├── LanguageContext.jsx  # Trilingual language provider
    │   └── ThemeContext.jsx     # Theme provider (dark / light mode)
    ├── pages/                   # Route views
    │   ├── HomePage.jsx         # Primary forensic scan interface
    │   ├── AboutPage.jsx        # Architecture & problem statement
    │   ├── EvalPage.jsx         # Live interactive 70-case benchmark test runner
    │   └── PrivacyPage.jsx      # Zero-retention privacy policy
    └── utils/                   # Utilities
        ├── ocrService.js        # Client-side Tesseract.js WebAssembly OCR engine
        └── translations.js      # Trilingual string dictionary
```

---

## Components Architecture

| Component | Responsibility |
|---|---|
| `VerdictBanner.jsx` | Renders high-visibility classification badges (`SCAM`, `SUSPICIOUS`, `LIKELY_GENUINE`, `UNSURE`) with risk level context. |
| `RiskGauge.jsx` | Animated circular SVG meter displaying composite risk score from 0 to 100. |
| `StageTimeline.jsx` | Visual horizontal progress radar displaying active scam stages and monotonic progress. |
| `NextMoveCard.jsx` | Displays predictive psychology forecast on the scammer's subsequent coercive move. |
| `CompanyCheck.jsx` | Shows MCA corporate registry status, CIN identification, and domain security flags. |
| `EvidenceCard.jsx` | Lists specific text quotes triggering forensic signals with severity chips. |
| `AdviceSection.jsx` | Displays step-by-step guidance on account freezing, evidence preservation, and golden hour reporting. |
| `ReportPack.jsx` | Interactive modal & section to preview, copy, or export the official 1930 cybercrime police complaint. |

---

## Global Contexts

- **`LanguageContext`**:
  - Exposes `language` (`"en"`, `"hi"`, `"pa"`) and `setLanguage()`.
  - Automatically loads translated strings via `utils/translations.js`.
- **`ThemeContext`**:
  - Exposes `theme` (`"dark"` or `"light"`) and `toggleTheme()`.
  - Manages `dark` class on root HTML element and synchronizes with `localStorage`.

---

## Environment Setup

Create a `.env` file in the `frontend/` directory (optional for development, as Vite proxies `/api` to `http://127.0.0.1:8000` by default):

```bash
# Backend API Base URL (leave blank if using Vite proxy)
VITE_API_URL=http://localhost:8000
```

---

## Installation & Running Locally

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher

### Development Server

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the Vite development server:
   ```bash
   npm run dev
   ```

3. Open your browser at `http://localhost:5173`.

### Production Build

1. Build the production bundle:
   ```bash
   npm run build
   ```

2. Preview the production build locally:
   ```bash
   npm run preview
   ```

---

## API Proxy & Integration

Vite is configured in `vite.config.js` to automatically proxy all calls matching `/api/*` directly to the backend server:

```javascript
server: {
  host: '0.0.0.0',
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
}
```

This prevents Cross-Origin Resource Sharing (CORS) complications during local development and testing.
