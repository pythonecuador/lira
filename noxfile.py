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
    session.install("coverage", "pytest", "pytest-asyncio")
    session.install("-e", ".")
    session.run("coverage", "run", "-m", "pytest", "tests", *session.posargs)


@nox.session
def coverage(session):
    session.install("coverage")
    session.run("coverage", "report", "--fail-under", "83")
    session.run("coverage", "html")


@nox.session
def lint(session):
    session.install("black", "flake8", "isort", "pydocstyle")
    session.run("flake8", *files)
    session.run("black", "--check", *files)
    session.run("isort", "--check", *files)
    session.run("pydocstyle", *files)


@nox.session
def format(session):
    session.install("black", "isort")
    session.run("black", *files)
    session.run("isort", *files)


@nox.session
def docs(session):
    session.install("-e", ".[docs]")
    live_update = session.posargs and session.posargs[0] == "--live"
    if live_update:
        session.install("sphinx-autobuild")

    session.cd("docs")
    if live_update:
        session.run("sphinx-autobuild", ".", "_build/html")
    else:
        session.run("sphinx-build", "-b", "html", "-W", ".", "_build/html")
