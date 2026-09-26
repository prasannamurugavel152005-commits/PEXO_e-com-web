# Pexo Market workspace notes

- Use Django templates and the existing `store` app for storefront features.
- Keep checkout changes transactional and cover inventory/order behavior with tests.
- Run `python manage.py test` and `python manage.py check` after backend changes.
- SQLite is for local development; configure environment-based secrets and hosts for deployment.