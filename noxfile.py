import nox

files = [
    "lira",
    "tests",
    "setup.py",
    "noxfile.py",
]


@nox.session
def lint(session):
    session.install("black", "flake8", "isort")
    session.run("black", "--check", *files)
    session.run("isort", "--check", *files)
    session.run("flake8", *files)


@nox.session
def format(session):
    session.install("black", "isort")
    session.run("black", *files)
    session.run("isort", *files)
