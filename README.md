# Inbox Intelligence — Email Classification + Reply Assistant

A compact, practical system that automatically classifies incoming emails and suggests short professional replies. Built for experimentation and lightweight deployment: FastAPI backend with an ML model, and a minimal React frontend with a polished dark UI.

---

## Features

- Fast hybrid classification (keyword heuristics + LinearSVC ML fallback)
- Three labels: `high_priority`, `normal`, `spam`
- Reply suggestion endpoint to generate one-sentence professional replies
- Minimal, responsive React UI with dark mode and smooth animations
- Docker + docker-compose for full-stack local deployment
- Nginx reverse proxy configuration for production-ready static serving and API proxying

---

## Architecture

```
                ┌──────────────────────┐
                │      Browser UI      │
                │  (React, Axios)      │
                └──────────┬───────────┘
                           │
                  (requests to /predict, /suggest_reply)
                           │
             ┌─────────────▼─────────────┐
             │         Nginx proxy       │
             │  (serves frontend build,  │
             │   proxies /api -> backend)│
             └───────┬─────────┬─────────┘
                     │         │
           (80/static)     (8000/api)
                     │         │
        ┌────────────▼─┐   ┌───▼────────┐
        │ Frontend     │   │ Backend     │
        │ (Nginx serve │   │ (FastAPI)   │
        │  static build)│  │  endpoints  │
        └──────────────┘   └─────────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  Model artifacts    │
                 │ model.pkl, vectorizer.pkl │
                 └────────────────────┘
```

---

## Tech Stack

- Frontend: React (Hooks), Axios, plain CSS (dark theme)
- Backend: FastAPI, Uvicorn, Pydantic
- ML: scikit-learn (LinearSVC + TfidfVectorizer)
- Deployment: Docker, docker-compose, Nginx

---

## Installation (developer/local)

Prerequisites:
- Node.js (v16+ / v18 recommended)
- Python 3.11+
- Docker & Docker Compose (optional for containerized run)

1) Clone repository

```bash
git clone <your-repo-url> inbox-intelligence
cd "inbox-intelligence"
```

2) Backend (local dev)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
# Run development server
uvicorn app:app --reload --port 8000
```

Open `http://localhost:8000/docs` to view the interactive API docs.

3) Frontend (local dev)

```bash
cd ../frontend
npm install
npm start
```

Open `http://localhost:3000` (development server).

4) Full stack with Docker Compose

From repository root:

```bash
# Build and start everything
docker-compose up --build

# Open UI via the reverse proxy (Nginx):
# http://localhost (port 80)

# Stop
docker-compose down
```

Notes:
- The frontend calls the backend at `http://localhost:8000` in development. When served through Nginx, the proxy routes API calls to the backend service.

---

## API Quick Example

### `POST /predict`
Request:

```json
{
  "text": "Your invoice #12345 is overdue. Please remit payment ASAP."
}
```

Response:

```json
{
  "label": "high_priority",
  "confidence": 1.0
}
```

### `POST /suggest_reply`
Request:

```json
{
  "label": "high_priority"
}
```

Response:

```json
{
  "suggested_reply": "Thank you for bringing this to my attention. I will prioritize this and get back to you shortly."
}
```

---

## Screenshots

Place UI screenshots in `./screenshots/` and reference them here. Examples:

- `screenshots/01-home.png` — initial app with textarea and Analyze button
- `screenshots/02-result.png` — result card with confidence bar
- `screenshots/03-suggest-reply.png` — suggested reply box

(You can add these images later. For now the README references the folder so Docker/CI artifact pages can show them.)

Example Markdown to insert an image:

```markdown
![Home screen](screenshots/01-home.png)
```

---

## Demo

A hosted demo is coming soon — this repo contains everything needed to run locally or in a container.

---

## Future Improvements

- Add probability calibration for meaningful confidence values
- Support email subject, sender parsing and richer metadata
- Add authentication and per-user settings
- Batch processing & saved histories
- Improve ML model (more data, transformer-based classifier)
- A/B testing and model versioning
- Light/dark theme toggle and keyboard shortcuts

---

If you want, I can also add a small `screenshots/` folder with placeholder images and wire README badges (build, docker) — tell me which you'd like next.

Enjoy — open `http://localhost:3000` and try pasting an email into the app.