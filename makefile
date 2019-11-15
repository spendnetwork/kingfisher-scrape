install:
	git clone git@github.com:spendnetwork/kingfisher-scrape.git
	cd kingfisher-scrape; pipenv install; cd ..

	git clone git@github.com:spendnetwork/kingfisher-process.git
	cd kingfisher-process; pipenv install; cd ..

run:
