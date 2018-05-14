#/bin/bash

prep=0

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1


if [ $prep -eq 1 ]; then
	echo
	echo
	echo "Start preprocessing for making dictionary!"
	python preprocessing.py
	echo "=========================================="
fi
python main.py

