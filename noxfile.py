import nox


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
    
    session.run("mv", "ottbot/config.py", "./config.py", external=True)
    session.run("mypy", "--install-types")
    session.run("mypy", "ottbot")
    session.run("mv", "config.py", "ottbot/config.py", external=True)
    
    session.run("pyright", "ottbot")
 