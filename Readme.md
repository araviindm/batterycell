### Battery cell DRF

## .env file

VITE_API_URL=http://127.0.0.1:8000 Backend URL

## To run the app locally

- Create a virtual environment inside the project directory

```bash

pip install -r requirements.txt
python manage.py makemigrations # If needed
python manage.py migrate # If needed
python manage.py runserver
```

## INFO

- battery_cell - POST and GET request to add battery cell and get all battery cell.
- get_battery_cell_by_id - GET request to fetch a single battery cell by id.
- compute - POST request will call generate_plot, get_battery_health, compute_circuit_parameters to compute respective values.
