main:
	python -m unittest test_whiskybot test_whiskydb test_scrub
bot:
	python -m unittest test_whiskybot.py

db:
	python -m unittest test_whiskydb.py

scrub:
	python -m unittest test_scrub.py
