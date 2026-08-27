# 🎯 Scout — AI-Powered Job Search & Intelligence Mobile App

**Scout** is a full-stack AI-powered mobile job-search application that transforms messy job listings into clean, structured, and easy-to-understand information.

Users can search jobs by **role, location, work type, experience level, skills, and posting date**. Scout processes job listings and uses **Google Gemini AI** to extract skills, experience, employment type, work mode, and concise summaries.

### Built With

* 📱 Flutter + Dart
* ⚡ FastAPI + Python
* 🐘 PostgreSQL + Supabase
* 🤖 Google Gemini
* 🔄 Riverpod + Dio + GoRouter

---

## ✨ Features

Scout lets users search and filter jobs by **role, location, work type, experience level, skills, and posting date**. Job listings are processed through **extraction, cleaning, normalization, deduplication, and Gemini AI analysis** to produce structured job information. Gemini extracts details such as **job role, experience level, employment type, work mode, required skills, nice-to-have skills, and a concise summary**. The Flutter mobile app provides a simple interface for browsing jobs, applying filters, viewing AI-generated insights, reading job details, and opening the original job listing.

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │  Flutter Mobile │
                    └────────┬────────┘
                             │ HTTP / REST API
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌─────────────┐
│  Job Data    │      │  PostgreSQL  │      │  Google     │
│  Providers   │      │  / Supabase  │      │  Gemini AI  │
└──────────────┘      └──────────────┘      └─────────────┘
```

---

## 🛠️ Tech Stack

**Backend**

`Python` · `FastAPI` · `Pydantic` · `SQLAlchemy` · `Alembic` · `PostgreSQL` · `Supabase` · `Google Gemini` · `Uvicorn`

**Mobile**

`Flutter` · `Dart` · `Riverpod` · `Dio` · `GoRouter` · `url_launcher`

---

## 📁 Project Structure

```text
Scout/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── cleaner/
│   │   ├── core/
│   │   ├── extractor/
│   │   ├── models/
│   │   ├── provider/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   └── requirements.txt
│
└── mobile_app/
    ├── lib/
    │   ├── core/
    │   ├── models/
    │   ├── providers/
    │   ├── services/
    │   ├── features/
    │   │   ├── search/
    │   │   ├── jobs/
    │   │   └── job_details/
    │   └── main.dart
    └── pubspec.yaml
```

---

# 🚀 Getting Started
 
## ⚙️ Backend

### 1. Clone

```bash
git clone https://github.com/saad-741/scout.git
cd scout/backend
```

### 2. Virtual Environment

**Windows**

```bash
python -m venv env
.\env\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create:

```text
backend/.env
```

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_connection_string
RAPIDAPI_KEY=your_RAPIDAPI_KEY
```

> ⚠️ Never commit `.env` to Git.

### 5. Database

```bash
alembic upgrade head
```

### 6. Start API

```bash
uvicorn app.main:app --reload
```

For a physical device:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📱 Flutter

```bash
cd scout/mobile_app
flutter pub get
flutter run
```

For a physical Android device, configure:

```text
mobile_app/.env
```

```env
API_BASE_URL=http://YOUR_LOCAL_IP:8000/api/v1
```

Your phone and computer must be connected to the same network.
