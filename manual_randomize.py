#!/usr/bin/env
from app import create_app
import weekly

app = create_app()
app.app_context().push()

weekly.randomize_weekly(app)
