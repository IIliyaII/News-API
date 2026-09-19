import requests
import smtplib
import os
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parents[2].joinpath('.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("api_key")

username = os.getenv("email")
password = os.environ.get("password")

url = f"https://newsapi.org/v2/everything?q=tesla&from=2026-08-16&sortBy=publishedAt&apiKey={api_key}"

response = requests.get(url)
news = response.json()
title = news["articles"][0]["title"]


smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login(username, password)

msg = MIMEText(news["articles"][0]["description"])
msg["Subject"] =  title
msg["From"] = username
msg["To"] = os.getenv("mail")

smtp.sendmail(msg["From"], msg["To"], msg.as_string())
smtp.quit()



def load_env_file():
    env_path = Path(__file__).resolve().parents[2].joinpath('.env')
    if not env_path.is_file():
        raise FileNotFoundError(f".env file not found at: {env_path}")
    load_dotenv(dotenv_path=env_path)
    return env_path


def get_required_env(var_name: str) -> str:
    try:
        value = os.environ[var_name]
    except KeyError:
        raise EnvironmentError(f"Missing required env var: {var_name}")
    if value is None or value.strip() == "":
        raise EnvironmentError(f"Env var is empty: {var_name}")
    return value


def fetch_top_news(api_key: str, query: str = "tesla", from_date: str = "2026-08-16") -> dict:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.Timeout:
        raise RuntimeError("NewsAPI request timed out")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("NewsAPI connection failed (network/DNS issue)")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"NewsAPI request failed: {e}")

    if response.status_code == 200:
        data = response.json()
        if not data.get("articles"):
            raise RuntimeError("NewsAPI returned 200 but no articles found")
        return data
    elif response.status_code == 401:
        raise RuntimeError("NewsAPI error 401: invalid API key")
    elif response.status_code == 403:
        raise RuntimeError("NewsAPI error 403: forbidden (key may lack permission or plan limit)")
    elif response.status_code == 429:
        raise RuntimeError("NewsAPI error 429: rate limit exceeded")
    else:
        try:
            message = response.json().get("message", "no message")
        except ValueError:
            message = response.text[:200]
        raise RuntimeError(f"NewsAPI error {response.status_code}: {message}")


def send_email(username: str, app_password: str, to_addr: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to_addr

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        smtp.starttls()
    except (smtplib.SMTPException, OSError) as e:
        raise RuntimeError(f"SMTP connection/TLS failed: {e}")

    try:
        smtp.login(username, app_password)
    except smtplib.SMTPAuthenticationError:
        smtp.quit()
        raise RuntimeError("SMTP login failed: check app password / username")
    except smtplib.SMTPException as e:
        smtp.quit()
        raise RuntimeError(f"SMTP login failed: {e}")

    try:
        smtp.sendmail(msg["From"], msg["To"], msg.as_string())
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")
    finally:
        smtp.quit()


def main():
    try:
        load_env_file()

        api_key = get_required_env("api_key")
        username = get_required_env("email")
        password = get_required_env("password")
        to_addr = get_required_env("mail")

        news = fetch_top_news(api_key)
        article = news["articles"][0]
        title = article.get("title") or "No title"
        description = article.get("description") or "No description available"

        send_email(username, password, to_addr, title, description)
        print("Email sent successfully.")

    except (FileNotFoundError, EnvironmentError, RuntimeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

