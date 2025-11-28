# Publishing Guide

This guide covers how to publish the **AI Agentic Framework** documentation and package.

## 📚 Publishing Documentation

We use **GitHub Pages** to host the documentation. A GitHub Action is configured to automatically build and deploy the docs whenever you push to the `main` branch.

### Automated Deployment
1.  Ensure the `.github/workflows/deploy_docs.yml` file exists in your repository.
2.  Go to your GitHub repository settings: **Settings > Pages**.
3.  Under **Build and deployment**, select **Source** as `Deploy from a branch`.
4.  Select `gh-pages` branch and `/ (root)` folder (this branch is created automatically by the action).
5.  Push changes to `main`. The action will run `pdoc`, build the site, and deploy it.

### Manual Build
To build the documentation locally:
```bash
# Generate API docs
uv run pdoc -o docs/api src/agentic_framework

# The docs are now available in docs/
# You can serve them locally with a simple HTTP server
python -m http.server -d docs
```

## 📦 Publishing Package to PyPI

To publish the package to the Python Package Index (PyPI), follow these steps.

### Prerequisites
- A PyPI account.
- `uv` installed.

### Steps

1.  **Build the Package**
    ```bash
    uv build
    ```
    This will create `dist/*.whl` and `dist/*.tar.gz` files.

2.  **Publish to PyPI**
    You can use `uv` to publish (if configured) or `twine`.
    
    Using `uv`:
    ```bash
    uv publish
    ```
    
    Using `twine` (standard method):
    ```bash
    pip install twine
    twine upload dist/*
    ```

3.  **Enter Credentials**
    When prompted, enter your PyPI username (`__token__`) and your API token as the password.

### Versioning
Remember to update the `version` in `pyproject.toml` before publishing a new release.
