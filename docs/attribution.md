# AI and Open-Source Attribution

> As required by CT BuildFest 2.0 hackathon rules, this document lists all AI tools, open-source libraries, datasets, and third-party resources used in building TaskGuard.

## AI Tools Used

| Tool | Provider | Use in Project | Extent |
|------|----------|---------------|--------|
| Groq Cloud (openai/gpt-oss-120b) | Groq | High-speed LPU reasoning engine for real-time forensic chat analysis, next-move prediction, and multilingual explanations | Primary runtime LLM for real-time analysis (<350ms latency) |
| Google Gemini 2.0 Flash | Google | Core LLM fallback for structured scam analysis and verdict validation | Secondary runtime fallback |
| Antigravity IDE | Google DeepMind | Development assistance — code generation, debugging, architecture planning | Development-time tool |

## Open-Source Libraries

### Backend (Python)
| Library | Version | License | Use |
|---------|---------|---------|-----|
| FastAPI | ≥0.100 | MIT | Web API framework |
| Uvicorn | Latest | BSD-3 | ASGI server |
| Pydantic | v2 | MIT | Data validation and schemas |
| google-genai | Latest | Apache 2.0 | Gemini API client |
| RapidFuzz | Latest | MIT | Fuzzy string matching for company name lookup |
| tldextract | Latest | BSD-3 | Domain extraction and analysis |
| python-dotenv | Latest | BSD-3 | Environment variable loading |
| python-multipart | Latest | Apache 2.0 | File upload handling |

### Frontend (JavaScript/TypeScript)
| Library | Version | License | Use |
|---------|---------|---------|-----|
| React | 18.x | MIT | UI component framework |
| Vite | 5.x | MIT | Build tool and dev server |
| Tailwind CSS | 4.x | MIT | Utility-first CSS framework |
| Framer Motion | 10.x | MIT | Animations and transitions |
| Lucide React | Latest | ISC | Icon library |
| React Router | 6.x | MIT | Client-side routing |

## Datasets

| Dataset | Source | License | Use |
|---------|--------|---------|-----|
| RoC-wise Company Master Data | data.gov.in | Open Government License India | Company registry verification (SQLite snapshot) |
| Test cases | Synthetic | Created by team | 60 labelled test cases based on publicly reported scam patterns |

## References and Research Sources

All research sources used to understand task scam patterns are listed in the README.md file under "Sources." These are secondary sources (news reports, analysis articles) used for educational understanding of scam patterns.

## Code Attribution

- All substantial blocks of AI-generated code are marked with comments where appropriate
- The hybrid rules + LLM architecture was designed by the team, with AI assistance in implementation
- Test cases are synthetic and anonymised — no real victim data was used

---

*Last updated: 30 October 2026*
