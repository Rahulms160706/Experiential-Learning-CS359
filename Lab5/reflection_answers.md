# Lab 5 — Static Code Analysis: Reflection

**Note:** The supplied three-page handout describes the reflection deliverable but does not display the exact reflection questions. These responses are based on its stated learning outcomes; replace the headings if your instructor supplied different exact questions.

## 1. What is static code analysis?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, and style problems before software is deployed.

## 2. What are the purposes of Pylint, Bandit, and Flake8?

Pylint checks code quality, naming, unused variables, and possible programming errors. Bandit detects potentially unsafe security patterns. Flake8 checks Python style, indentation, whitespace, and formatting.

## 3. Which issues were identified and fixed?

The original code contained unsafe `eval()`, shell command execution, a hardcoded secret, weak MD5 hashing, insecure random PIN generation, a mutable default argument, and a broad exception handler. The code was also improved for naming, docstrings, unused names, and file handling.

## 4. How did static analysis improve the program, and how were the fixes checked?

Static analysis made code-quality and security concerns visible before deployment. After editing, Pylint, Bandit, and Flake8 should be rerun and their reports compared with the originals. The program should also be executed to check its basic behaviour. Record actual scores and remaining findings from the reports; do not assume all checks pass without running them.
