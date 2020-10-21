import nox

files = [
    "lira",
    "tests",
    "setup.py",
    "noxfile.py",
    "docs/conf.py",
]


@nox.session
def tests(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "tests")


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


@nox.session
def docs(session):
    session.install("-e", ".[docs]")
    session.cd("docs")
    session.run("sphinx-build", "-b", "html", "-W", ".", "_build/html")
