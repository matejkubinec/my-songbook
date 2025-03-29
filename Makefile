default: list create clean

create:
	docker compose up --remove-orphans

list:
	find songs -name "*.cho" | grep -v "(WIP)" | sort > list.txt

wedding:
	grep -rl "list: wedding" ./songs | grep -v "(WIP)" | sort > list.txt
	docker run \
		--rm \
		-v ".:/workspace" \
		-w "/workspace" \
		matejkubinec/chordpro \
	    --transcode=custom \
      	--filelist=list.txt \
      	--config=./config/guitar.json \
      	--output=books/wedding.pdf
	rm list.txt

clean:
	docker compose rm -f
	rm list.txt