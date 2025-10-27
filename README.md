# Agri Insight Backend (LangChain + FastAPI)

This backend fetches YouTube playlist videos, retrieves their transcripts, embeds them using LangChain, and stores them in a PostgreSQL vector database with pgvector. Built with FastAPI.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
Create a `.env` file in the root:
```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:5432/<database>
API_KEYS=your_api_key_1,your_api_key_2  # comma-separated
HOST_PORT=8000  # optional
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```
- The app will be available at http://localhost:${HOST_PORT} (default: http://localhost:8000)

### 4. Run the server locally
```bash
uvicorn main:app --reload
```

### 5. Database Migration
```bash
alembic upgrade head
```

## API Usage

### Fetch and Store Transcripts
- **Endpoint:** `POST /api/v1/youtube/fetch_and_store_transcripts?playlist_id=YOUR_PLAYLIST_ID`
- **Description:** Fetches transcripts for all videos in a playlist, sanitizes and chunks them, embeds each chunk, and stores in the vector DB.

### Query Transcripts
- **Endpoint:** `POST /api/v1/youtube/query_transcripts`
- **Body:** `{ "query": "your search query", "top_k": 3 }`
- **Description:** Returns the most relevant transcript chunks for a given query.

## Notes
- Make sure your PostgreSQL database has the pgvector extension enabled.
- The embedding model used is `all-MiniLM-L6-v2` via LangChain's HuggingFaceEmbeddings.

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations, similar to Laravel's artisan migrate.

### Setup
1. Set your PostgreSQL connection string in the `.env` file as `DATABASE_URL`:
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

