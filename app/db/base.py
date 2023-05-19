import databases
import sqlalchemy

from sqlalchemy.dialects.postgresql import UUID

from app.core.config import settings

database = databases.Database(settings.DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", UUID, primary_key=True, server_default=sqlalchemy.func.gen_random_uuid()),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("token", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

records = sqlalchemy.Table(
    "records",
    metadata,
    sqlalchemy.Column("id", UUID, primary_key=True, server_default=sqlalchemy.func.gen_random_uuid()),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("user_id", UUID, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("uploaded_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)
