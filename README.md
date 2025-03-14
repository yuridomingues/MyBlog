# Blog API

This project is a simple blog article API built with **FastAPI** and **SQLAlchemy** using the SQLite database.

## Summary

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
    - [Initializing the server](#initializing-the-server)
    - [Testing the API](#testing-the-api)
- [Folder Structure](#folder-structure)
- [Main Routes](#main-routes)
---

## Overview

This project exemplifies the implementation of a CRUD (Create, Read, Update, Delete) for blog articles in Python.

- **FastAPI** provides the framework for quickly and intuitively creating routes.
- **SQLAlchemy** handles the object-relational mapping (ORM), allowing you to interact with the SQLite database in a simple way.

In the end, you will have endpoints to create, list, search, update, and delete articles.

---

## Features

- **Creation** of articles with title, content, and publication status.
- **Listing** of all articles, with an optional filter to display only published or unpublished articles.
- **Search** for a specific article by ID.
- **Update** of existing articles.
- **Deletion** of articles by ID.

---

## Prerequisites

- **Python 3.7+** installed on your system (check with `python --version` or `python3 --version`).
- **pip** (Python package manager) installed.
- (Optional) **virtualenv** or `python -m venv` to create an isolated virtual environment.

---

## Installation

1. **Clone** or **download** this repository:

     ```bash
     git clone https://github.com/yuridomingues/MyBlog.git
     cd myblog

