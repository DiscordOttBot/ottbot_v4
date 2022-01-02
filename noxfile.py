import nox
import sys


@nox.session(reuse_venv=True)
def format_code(session):
    session.install("-r", "requirements.txt")

    session.run("isort", "ottbot")
    session.run("codespell", "ottbot")
    session.run("black", "ottbot")


@nox.session(reuse_venv=True)
def lint_code(session: nox.Session):
    session.install("flake8")
    session.install("mypy")
    session.install("pyright")

    session.run("flake8", "ottbot")

    # session.run("mypy", "--install-types")
    with open("mypy.log", "r") as f:
        session.run("mypy", "ottbot", stdout=f)

    session.run("pyright", "ottbot")
