import subprocess

import nox


@nox.session(reuse_venv=True)
def format_code(session):
    session.install("-r", "requirements.txt")

    session.run("isort", "ottbot")
    session.run("codespell", "ottbot", "--ignore-regex", "(nd|swith)")
    session.run("black", "ottbot")


@nox.session(reuse_venv=True)
def lint_code(session: nox.Session):

    session.install("flake8")
    session.install("mypy==0.930")
    session.install("pyright")
    session.install("-r", "requirements.txt")

    session.run("flake8", "ottbot")

    session.run("mypy", "--install-types")
    with open("mypy.log", "w") as f:
        session.run("mypy", "ottbot", "--pretty", stdout=f)

    session.run("pyright", "ottbot")
