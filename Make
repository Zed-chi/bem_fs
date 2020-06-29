install:
	poetry install

lint:
	poetry run flake8 ./bem_fs_maker

publish:
	poetry build
	poetry publish -r test