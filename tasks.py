import os
from invoke import task


@task
def dev(ctx):
    ctx.run(
        "flask --app app.web run --debug --port 8000",
        pty=os.name != "nt",
        env={"APP_ENV": "development"},
    )

@task
def prod(ctx):
    ctx.run(
        "gunicorn --bind 0.0.0.0:8000 app.web:app",
        pty=os.name != "nt",
        env={"APP_ENV": "production"},
    )