#!/bin/sh

gunicorn \
  --bind=0.0.0.0:8000 \
  --workers=2 \
  --timeout=120 \
  --chdir ai-api \
  app:app