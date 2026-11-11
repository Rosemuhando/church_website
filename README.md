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

For local environment variables, copy `.env.example` to `.env` and set your values there. The `.env` file is ignored by Git and must never be committed. Install dependencies with `python -m pip install -r requirements.txt` after changing the requirements. If `DATABASE_URL` is blank, local development uses `db.sqlite3`.

## Deploy to Render with Neon

Create a Render **Blueprint** from this repository using `render.yaml`, or set up a Web Service manually with:

- **Build command:** `bash build.sh`
- **Start command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers ${WEB_CONCURRENCY:-1} --threads ${GUNICORN_THREADS:-4}`

The Render build command is required: it installs dependencies, runs database migrations, and collects static files. If Render logs `No directory at .../staticfiles/`, verify the service's **Build Command** is `bash build.sh`, save the settings, then trigger a fresh deploy. A successful start message alone does not confirm the pages are serving successfully.

In the Render service's environment settings, add:

- `DJANGO_SECRET_KEY`: a newly generated, private Django secret key.
- `DATABASE_URL`: the connection string for the Neon database/branch this service should use.
- `CLOUDINARY_URL`: the private Cloudinary URL from your Cloudinary dashboard; required for photo and video uploads.
- Email provider settings (`DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_HOST_USER`, `DJANGO_EMAIL_HOST_PASSWORD`, and `DJANGO_EMAIL_USE_TLS`) if password-reset email should be sent.

Do not upload or commit the local `.env` file to Render. Set these values in Render's Environment settings instead; environment variables supplied by Render take precedence over values in `.env`.

Render's hostname is added automatically to Django's allowed hosts. For any custom domain, add its hostname to `DJANGO_ALLOWED_HOSTS` and its HTTPS origin to `DJANGO_CSRF_TRUSTED_ORIGINS` (for example, `https://www.example.org`).

The build command runs Django migrations before collecting static files, so the Neon database needs to be reachable during the build. Confirm that `DATABASE_URL` is set on the Render service and points to the intended Neon project and branch. Migrations create the tables but do not copy existing data from a local SQLite database; existing records must be exported and imported separately. In production, the app now fails clearly if `DATABASE_URL` is missing instead of silently writing to Render's temporary filesystem.

## Member and content-admin access

Members sign in at `/login/`. From their account page they can request content-admin access. A superadmin signs in through the same page (their login redirects to Django's `/admin/` area), opens **Content admin requests**, and approves or rejects applications. Approved content admins remain ordinary non-staff accounts, sign in at `/login/`, and are sent to `/staff-panel/`. That separate panel can publish announcements and teachings/sermons, upload church photos and videos, and update pastor photos. It does not expose user accounts, admin approvals, or superadmin controls.

The About page's pastor cards are database-backed, including Pastor Michael. Superadmins can edit all profile details in Django's admin area; approved content admins can update profile photos only from their panel.

Cloudinary provides the media upload and storage service; create an account, copy its `CLOUDINARY_URL` into Render's Environment settings, and keep it private. Panel file inputs support photos and videos selected from mobile devices as well as computers. Check Cloudinary's current plan and usage limits before uploading larger video files.

Existing uploads on a local disk are not copied to Cloudinary automatically. Re-upload those files after deployment if you migrate records that refer to local media.

Production uses SMTP for email rather than writing password-reset links to server logs. Set the email-provider variables in Render to enable email delivery.

Gunicorn starts with two workers and four threads per worker by default; `WEB_CONCURRENCY` and `GUNICORN_THREADS` can override these settings. This allows multiple requests to be handled concurrently, but it does not guarantee capacity for a particular traffic level. Capacity depends on the Render instance size, database limits, and request workload; measure it with a controlled load test against the deployed service before relying on a target number of simultaneous visitors.