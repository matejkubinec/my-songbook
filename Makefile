default: list create clean

create:
	docker-compose up --remove-orphans

list:
	find songs -name "*.cho" | grep -v "(WIP)" | sort > list.txt

clean:
	docker-compose rm -f
	rm list.txt