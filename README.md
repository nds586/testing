# LuminaClean (Django Marketplace)

LuminaClean is a Django-based cleaning marketplace prototype with customer booking flows, provider assignment/reassignment logic, KYC upload support, and a multi-page front-end "Vibe" experience.

## Tech Stack

- Python 3.11+
- Django 5.x
- SQLite (default for local development)
- Pillow (for `ImageField` uploads)

## 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd testing
```

## 2) Create and activate a virtual environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3) Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Run migrations

```bash
python manage.py migrate
```

## 5) Create an admin user

```bash
python manage.py createsuperuser
```

## 6) Start the development server

```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## 7) Seed minimum data (recommended for first run)

To use booking and provider matching flows immediately, create these records in Django Admin:

1. **Service categories** (`services.ServiceCategory`) with:
   - `name`
   - `icon`
   - `basePrice`
2. **Users** with different `user_type` values (`CUSTOMER`, `PROVIDER`, `ADMIN`).
3. **Customer** profiles linked to customer users.
4. **ServiceProvider** profiles linked to provider users.

> Provider assignment logic only considers verified providers (`isVerified=True`).

## Development Notes

- Static files are authored in:
  - `static/css/main.css`
  - `static/js/vibe.js`
- Templates are in:
  - `templates/base.html`
  - `templates/vibe/`
- Media uploads (such as KYC `idProof` and category icons) are stored under `media/` in local dev.

## Common Commands

```bash
python manage.py check
python manage.py test
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'django'`**
  - Ensure your virtual environment is activated.
  - Re-run `pip install -r requirements.txt`.

- **Image upload errors**
  - Confirm `Pillow` is installed (`pip show Pillow`).

- **No providers visible in discovery/assignment**
  - Ensure provider profiles exist and have `isVerified=True`.
