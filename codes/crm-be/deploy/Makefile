deploy:
	rm -rf ../tuoen/model/migrations/**
	python3 ../manage.py makemigrations --empty model
	python3 ../manage.py makemigrations
	python3 ../manage.py migrate
	python3 ../support/init_manager.py
	python3 ../support/test_data.py
