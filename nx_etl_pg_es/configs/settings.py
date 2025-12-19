from configs.setting_model import EnvSettings

settings = EnvSettings()

pg_config = {
    "dbname": settings.admin_postgres_db,
    "user": settings.admin_postgres_user,
    "password": settings.admin_postgres_password,
    "host": settings.admin_postgres_host,
    "port": settings.admin_postgres_port,
}

redis_config = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

elastic_config = {
    "host": settings.elastic_host,
    "port": settings.elastic_port,
}