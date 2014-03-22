deploy:
	sudo service pkujishi reload
run:
	python run.py
dep:
	sudo pip install -r requirements.txt
clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
depclean: clean
	-@sudo rm -rf whoosh
	-@rm -rf app/static/uploads
