# Project1
JWKS server

# COMMANDS
pytest --cov=app --cov-report term-missing

Invoke-RestMethod -Uri http://127.0.0.1:8080/auth -Method Post

Invoke-RestMethod -Uri http://127.0.0.1:8080/.well-known/jwks.json -Method Post

Invoke-RestMethod -Uri http://127.0.0.1:8080/.well-known/jwks.json -Method Get
