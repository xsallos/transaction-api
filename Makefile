.PHONY: requirements tests run

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

tests:
	pytest -v

run:
	fastapi dev ./src/main.py