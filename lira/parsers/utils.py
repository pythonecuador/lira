_languages = {
    "python": ".py",
    "c": ".c",
    "cpp": ".cpp",
    "java": ".java",
    "javascript": ".js",
    "rust": ".rs",
    "rst": ".rst",
    "markdown": ".md",
}


def guess_extension(language):
    language = language or ""
    return _languages.get(language.strip().lower(), ".txt")
