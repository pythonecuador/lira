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
    session.install("coverage", "pytest")
    session.install("-e", ".")
    session.run("coverage", "run", "-m", "pytest", "tests")


@nox.session
def coverage(session):
    session.install("coverage")
    session.run("coverage", "report", "--fail-under", "86")
    session.run("coverage", "html")


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
