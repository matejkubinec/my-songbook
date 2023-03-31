default: list create clean

create:
	docker-compose up --remove-orphans

list:
	find . -name "*.cho" > list.txt

clean:
	docker-compose rm -f
	rm list.txt