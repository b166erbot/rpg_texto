isort .
black -l 80 .
flake8 --config flake8.txt
radon cc -n b .
