# Full Gospel Churches of Kenya - Njiru

A Django website for Full Gospel Churches of Kenya - Njiru.

## Run locally on Windows

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The development secret key is provided as a local fallback. Set `DJANGO_SECRET_KEY` to a private value before deploying the site.