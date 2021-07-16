install:
	pip install -e .['dev']

uninstall:
	pip uninstall guardian-core

test_cov:
	 export GD_ENV=DEV && pytest tests/  --cov=tips-arena-core

test:
	 export GD_ENV=DEV && pytest tests/ -v

cleanup:
	rm -r .pytest_cache && echo "Limpeza concluída..."