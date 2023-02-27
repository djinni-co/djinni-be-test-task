server:
	./m runserver

shell:
	./m shell

init:
	poetry install -q
	./m migrate
	./m loaddata wishlist/main/fixtures/item.json
