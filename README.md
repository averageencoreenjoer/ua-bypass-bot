# UA Bypass Bot

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)![Playwright](https://img.shields.io/badge/Playwright-Automated-green?style=for-the-badge&logo=playwright)![Pytest](https://img.shields.io/badge/Pytest-Tested-green?style=for-the-badge&logo=pytest)![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker&logoColor=white)

A sophisticated bot designed to emulate mobile browsers, bypass anti-bot measures, and perform automated searches on engines like Google. It leverages a powerful stack including Playwright for browser automation, proxy rotation for anonymity, and 2Captcha integration for solving CAPTCHAs.

## ✨ Features

-   **📱 Mobile Emulation**: Simulates an iPhone 12 to present a legitimate mobile user agent and viewport.
-   **🔄 Proxy Rotation**: Automatically cycles through a list of proxies to prevent IP-based blocking.
-   **🤖 CAPTCHA Solving**: Integrates with the 2Captcha service to solve reCAPTCHA challenges when detected.
-   **✌️ Dual Modes**:
    -   **`fixture` mode**: Runs offline using a saved HTML file for fast, consistent parsing tests.
    -   **`live` mode**: Performs real-time searches on Google.
-   **📊 Data Export**: Saves search results in both JSON and CSV formats.
-   **📸 Debugging**: Captures screenshots and saves HTML content of live runs for easy debugging.
-   **🐳 Dockerized**: Fully containerized for easy, cross-platform deployment and execution.

## 🚀 Getting Started: Local Development

This guide will walk you through setting up and running the application on your local machine.

### Prerequisites

-   Python 3.11 or newer
-   Git

### 1. Clone the Repository

```bash
git clone https://github.com/averageencoreenjoer/ua-bypass-bot.git
cd ua-bypass-bot
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

This command downloads the browser binaries (Chromium) that Playwright needs to operate.

```bash
playwright install chromium
```

### 5. Configuration

Before running the bot, you need to configure a few things:

**A) Create a Proxy List**

Create a file at `src/proxy.txt`. Add your proxies to this file, one per line, in the format `http://user:pass@host:port`. The bot will not start if this file is empty and `--use-proxy` is enabled.

**B) Set up Environment Variables** (Optional)

For CAPTCHA solving, you need to provide a 2Captcha API key. Create a `.env` file in the project's root directory:

**.env file**
```
TWO_CAPTCHA_API_KEY="YOUR_2CAPTCHA_API_KEY_HERE"
```
The application will automatically load this key.

### 6. Run the Application

Now you are ready to run the bot from your terminal.

#### Fixture Mode (Offline)

This mode is useful for testing the HTML parsing logic without making any live web requests. It uses a pre-saved `google_sample.html` file.

```bash
python -m src.main --mode fixture --keyword "test" --target-domain "example.com"
```

#### Live Mode (Online)

This mode performs a real-time search on Google.

**Example 1: Simple Live Search (No Proxy)**

Runs in headless mode (no browser window will open).

```bash
python -m src.main --mode live --keyword "best vpn" --target-domain "expressvpn.com" --headless
```

**Example 2: Live Search with Proxy Rotation**

Runs in headless mode and cycles through the proxies defined in `proxies.txt`.

```bash
python -m src.main --mode live --keyword "buy sneakers" --target-domain "nike.com" --use-proxy --headless
```
---

## 🐳 Alternative Usage: Docker

For ultimate portability and to avoid local setup, you can run the application inside a Docker container. This is the ideal method for deployment or sharing with others.

### Prerequisites

-   [Docker](https://www.docker.com/get-started) must be installed and running.

### 1. Build the Docker Image

From the project's root directory, run this command to build the image:

```bash
docker build -t ua-bypass-bot .
```

### 2. Run the Container

Once built, you can run the bot with a single command.

**A) Run in Default `fixture` Mode**

```bash
docker run --rm -it -v "$(pwd)/results:/app/results" ua-bypass-bot
```

**B) Full `live` Run with Proxy and CAPTCHA Solving**

This command runs a live search, mounts the local `results` folder to save the output, and securely provides the 2Captcha API key.

```bash
docker run --rm -it \
  -e TWO_CAPTCHA_API_KEY="YOUR_2CAPTCHA_API_KEY_HERE" \
  -v "$(pwd)/results:/app/results" \
  ua-bypass-bot \
  --mode live \
  --keyword "web scraping best practices" \
  --target-domain "github.com" \
  --headless \
  --use-proxy
```

> **Note on Docker:** When using Docker, the `proxy.txt` file is copied into the image during the build process. If you change your proxies, you will need to rebuild the image.

## 🧪 Running Tests

To ensure all components are working as expected, run the test suite using `pytest`.

```bash
python -m pytest
```

## 📂 Project Structure

```
ua-bypass-bot/
├── Dockerfile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   ├── captcha.py
│   ├── emulator.py
│   ├── proxy.py
│   ├── search.py
│   └── ...
└── tests/
    └── ...
```

## 📄 License

This project is licensed under the MIT License.
