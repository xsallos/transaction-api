requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

tests:
	$(cat .env.tests | xargs) pytest -v

run:
	fastapi dev ./src/main.py