# Agri Insight Backend (LangChain + FastAPI)

This backend service fetches YouTube playlist videos, retrieves their transcripts, embeds them using LangChain, and stores them in a Supabase vector database. Built with FastAPI.

## Features
- Fetch video transcripts from a YouTube playlist
- Embed transcripts using Sentence Transformers (via LangChain)
- Store transcripts and embeddings in Supabase vector DB (pgvector)

## Project Structure
```
.
├── api/
│   └── v1/
│       ├── api.py
│       └── endpoints.py
├── models/
├── schemas/
├── services/
│   ├── vector_db_service.py
│   └── youtube_service.py
├── utils/
├── main.py
├── requirements.txt
├── .env
├── docker/
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Install dependencies (for local development)
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
Create a `.env` file in the root:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
YOUTUBE_API_KEY=your_youtube_api_key
# Optionally set the host port for Docker Compose (default is 8000):
HOST_PORT=8000
```

### 3. Run with Docker Compose
Build and start the app using Docker Compose:
```bash
docker-compose up --build
```
- The app will be available at http://localhost:${HOST_PORT} (default: http://localhost:8000)
- The Dockerfile is located at `docker/Dockerfile` and is referenced in `docker-compose.yml`.

### 4. Run the server locally (without Docker)
```bash
uvicorn main:app --reload
```

## API Usage

### Fetch and Store Transcripts
- **Endpoint:** `POST /api/v1/youtube/fetch_and_store_transcripts?playlist_id=YOUR_PLAYLIST_ID`
- **Response:**
  ```json
  [
    {"videoId": "abc123", "title": "Video Title", "transcript": "..."},
    ...
  ]
  ```

## Notes
- The Supabase table `youtube_transcripts` should have columns: `video_id`, `title`, `transcript`, `embedding` (vector/float[]).
- Make sure your Supabase project has pgvector enabled.
- The embedding model used is `all-MiniLM-L6-v2` via LangChain's HuggingFaceEmbeddings.

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations, similar to Laravel's artisan migrate.

### Setup
1. Set your Supabase/Postgres connection string in the `.env` file as `DATABASE_URL`:
   ```env
   DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:5432/<database>
   ```
   Or update `alembic.ini` directly.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Creating and Running Migrations
- To autogenerate a migration after changing models:
  ```bash
  alembic revision --autogenerate -m "your message"
  ```
- To apply migrations (create/update tables):
  ```bash
  python manage.py migrate
  ```

This will create or update the `youtube_transcripts` table automatically.
