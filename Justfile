up *ENVIRONMENT:
    docker compose --env-file .env.{{ENVIRONMENT}} up -d

down *ENVIRONMENT:
    docker compose --env-file .env.{{ENVIRONMENT}} down

build *FLAGS:
    docker compose build {{FLAGS}}

ps *ENVIRONMENT:
    docker compose --env-file .env.{{ENVIRONMENT}} ps