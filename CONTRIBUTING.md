# Contributing to UA Bypass Bot

First off, thank you for considering contributing to this project! Your help is greatly appreciated.

This document provides guidelines for contributing to the project. Please feel free to propose changes to this document in a pull request.

## How Can I Contribute?

-   **Reporting Bugs**: If you find a bug, please open an issue and provide as much detail as possible, including steps to reproduce it.
-   **Suggesting Enhancements**: If you have an idea for a new feature or an improvement, open an issue to discuss it.
-   **Pull Requests**: If you've fixed a bug or implemented a new feature, we'd love to see your pull request.

## Development Setup

To get your development environment set up, please follow the instructions in the `README.md` for the "Local Development Setup". A quick summary:

1.  **Fork & Clone**: Fork the repository and clone your fork locally.
2.  **Create a branch**: `git checkout -b your-feature-name`
3.  **Set up environment**: Create a virtual environment (`venv`).
4.  **Install dependencies**:
    ```bash
    pip install -r requirements-dev.txt
    ```
5.  **Install browsers**:
    ```bash
    playwright install chromium
    ```

## Code Style

-   Please follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
-   Use clear and descriptive variable and function names.
-   Add comments to explain complex or non-obvious parts of your code.

## Commit Message Guidelines

We follow the **Conventional Commits** specification. This helps us maintain a clean and descriptive git history. Each commit message should consist of a **type**, an optional **scope**, and a **subject**.
