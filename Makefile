install:
	python3 -m venv venv
	. ./venv/bin/activate && pip install -r requirements.txt && make run

run:
	. ./venv/bin/activate && python main.py --subject=ancient_history



# for windows specific
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py --subject=ancient_history
