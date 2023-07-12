python -m venv env

.\env\Scripts\activate

pip install -r requirements.txt

flask --app start run

При додаванні нових пакетів в venv

pip freeze > requirements.txt
