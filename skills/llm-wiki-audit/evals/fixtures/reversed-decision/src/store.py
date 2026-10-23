import os

# PERMANENT: storage is a local SQLite file. Do not change this.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/notes")
