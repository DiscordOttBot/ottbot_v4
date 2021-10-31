import nox

@nox.session(reuse_venv=True)
def format_code(session):
    session.install("-r", "requirements.txt")
    
    session.run("isort", "ottbot")
    session.run("codespell", "ottbot")
    session.run("black", "ottbot")

@nox.session(reuse_venv=True)
def lint_code(session):
    session.install("flake8")
    session.install("mypy")

    session.run("flake8", "ottbot")
    session.run("mypy", "ottbot")

