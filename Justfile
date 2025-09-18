up *ENVIRONMENT:
    docker compose --env-file .env.{{ENVIRONMENT}} up -d

down *ENVIRONMENT:
    docker compose --env-file .env.{{ENVIRONMENT}} down

build *FLAGS:
    docker compose build {{FLAGS}}

ps:
    docker compose ps