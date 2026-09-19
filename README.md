# News API

A Python automation tool that fetches news from [NewsAPI](https://newsapi.org/) and sends selected news to an email address.

## Features

* Fetch news from NewsAPI
* Filter news by keyword
* Send news results via email
* Load sensitive configuration from environment variables
* Manage dependencies with `uv`

## Requirements

* Python 3.12+
* A [NewsAPI](https://newsapi.org/) API key
* An email account that supports SMTP authentication

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/IIliyaII/News-API.git
cd News-API
```

### 2. Install dependencies

This project uses `uv` for dependency management.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_news_api_key
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_password
```

> Do not commit your `.env` file to Git. It contains sensitive credentials.

### 4. Run the application

```bash
uv run news_api
```

## Project Structure

```text
News-API/
├── src/
│   └── news_api/
│       └── ...
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Configuration

The application uses environment variables to keep sensitive information outside the source code.

| Variable         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `NEWS_API_KEY`   | API key used to access NewsAPI                        |
| `EMAIL_ADDRESS`  | Email address used to send notifications              |
| `EMAIL_PASSWORD` | Password or app password used for SMTP authentication |

## Development

To run the project through the Python module directly:

```bash
uv run python -m news_api
```

The project also provides a command-line entry point:

```bash
uv run news_api
```

## Security

Never commit API keys, passwords, tokens, or other secrets to Git.

The `.env` file is excluded through `.gitignore`.

If a secret is accidentally committed, simply deleting it from the latest commit is not enough. The exposed credential should be revoked and replaced.

## License

This project is available under the MIT License.

