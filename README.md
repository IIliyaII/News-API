# News API Mailer

A small Python script that fetches the latest news about a topic from [NewsAPI](https://newsapi.org/) and emails the top article (title + description) to you via Gmail SMTP.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- A NewsAPI key
- A Gmail account with 2-Step Verification and an App Password

## Setup

```bash
git clone <your-repo-url>
cd news_api
uv sync
```

Create a `.env` file in the **project root** (see below), then run:

```bash
uv run python path/to/main.py   # adjust to your entry file
```

## Environment variables

The script reads its configuration from a `.env` file in the project root. All four variables are **required**; the script exits with an error if any is missing or empty.

| Variable   | Description                                             | Example                    |
|------------|---------------------------------------------------------|----------------------------|
| `api_key`  | Your NewsAPI key                                        | `0123456789abcdef...`      |
| `email`    | Gmail address used to **send** the email                | `you@gmail.com`            |
| `password` | Gmail **App Password** (not your normal password)       | `abcd efgh ijkl mnop`      |
| `mail`     | Address that **receives** the email                     | `recipient@example.com`    |

### Example `.env`

```env
api_key=your_newsapi_key_here
email=you@gmail.com
password=your_gmail_app_password
mail=recipient@example.com
```

Do not wrap values in quotes and do not put spaces around `=`.

### Where to get the values

**`api_key`**
1. Register at <https://newsapi.org/register>.
2. Copy the key from your account dashboard.

Note: the free Developer plan limits requests per day and only returns articles from roughly the last month. Check your plan's limits on the NewsAPI site.

**`password` (Gmail App Password)**
1. Enable 2-Step Verification on your Google account.
2. Go to <https://myaccount.google.com/apppasswords>.
3. Create an app password and copy the 16-character code.

Your regular Gmail password will **not** work; Google rejects it for SMTP logins.

## Security

- `.env` contains secrets. Make sure it is listed in `.gitignore` **before** your first commit:

  ```gitignore
  .env
  .venv/
  ```

- If `.env` was ever committed, it stays in git history. Revoke and regenerate both the NewsAPI key and the Gmail App Password.
- Never paste your `.env` contents into issues, screenshots, or chats.

## Troubleshooting

| Symptom                               | Likely cause                                                        |
|---------------------------------------|---------------------------------------------------------------------|
| `.env file not found`                 | `.env` is not in the expected location (project root)               |
| `Missing required env var: ...`       | Variable is not defined in `.env` or has a different name           |
| `NewsAPI error 401`                   | Invalid `api_key`                                                   |
| `NewsAPI error 429`                   | Daily request limit reached                                         |
| `NewsAPI error 400/426` or no articles| Date range outside your plan's limit, or the query returned nothing |
| `SMTP login failed`                   | Using your normal password instead of an App Password, or a typo    |

## Project structure

```
news_api/
├── pyproject.toml
├── uv.lock
├── .env            # not committed
├── .gitignore
└── src/news_api/
    └── main.py
```

Adjust this section to match your actual layout.