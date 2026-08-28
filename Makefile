install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v --tb=short

build:
	sam build

local:
	sam local start-api

deploy:
	sam build && sam deploy --guided

deploy-ci:
	sam build && sam deploy \
		--no-confirm-changeset \
		--no-fail-on-empty-changeset \
		--parameter-overrides \
			DBHost=$(DB_HOST) \
			DBPort=$(DB_PORT) \
			DBName=$(DB_NAME) \
			DBUser=$(DB_USER) \
			DBPassword=$(DB_PASSWORD) \
			JWTSecret=$(JWT_SECRET)
