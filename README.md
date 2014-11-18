# PKU-JiShi
* app/  the site directory
* raw/  the static html files


## To re-create Database
* stop the web service
* python db\_drop.py
* comment line from app import views in init file
* python db\_create.py
* python db\_fake.py