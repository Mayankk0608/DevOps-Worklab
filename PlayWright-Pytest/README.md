# 🎭 Playwright‑Pytest Automation Suite

A browser‑testing framework built with **Playwright**, **pytest**, and **Python** to validate a containerised Django application. This project is part of my self‑taught Cloud/DevOps journey – proving that automation, clean code, and CI/CD practices apply just as much to testing as they do to infrastructure.

## 🧰 Tools & Technologies

| Category       | Tool / Library                                          |
|:---------------|:--------------------------------------------------------|
| Automation     | [Playwright](https://playwright.dev/python/)            |
| Test Runner    | [pytest](https://docs.pytest.org/)                      |
| Reporting      | pytest-html, built‑in screenshots & videos              |
| Language       | Python 3.x                                              |
| Environment    | venv (Ubuntu WSL & Windows PowerShell)                  |
| Version Control| Git, GitHub, GitLab                                     |
| Containerised App Under Test | Django‑Notes‑App (Docker, Docker‑Compose) |

## 📁 Project Structure

PlayWrightCode/
├── venv/ # Python virtual environment (gitignored)
├── pages/ # Page Object Model (future extension)
├── tests/
│ └── test_google.py # Automated Google search test
├── assets/
│ └── style.css # Placeholder for custom styles
├── reports/
│ └── report1.html # HTML test report
├── utils/ # Helper utilities (future)
├── .gitignore
├── README.md
├── conftest.py # Shared pytest fixtures (browser, page)
├── OpeningBrowser.py # Standalone script to open the Django app
├── pytest.ini # Default pytest configuration
├── requirements.txt # Frozen dependencies
└── test_sample.py # Minimal sanity test (1+1=2)


## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone (https://github.com/Mayankk0608/PlayWright-Pytest.git)
   cd PlayWrightCode

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
source venv/bin/activate       # Linux/WSL
.\venv\Scripts\Activate        # Windows PowerShell

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Install Playwright browsers**
   ```bash
   playwright install

5. **Run the stand‑alone script (requires the Django app running on http://localhost:8000)** #You can clone the django app from my github and run it using docker compose
   ```bash
   python OpeningBrowser.py

6. Execute the test suite
    ```bash
    pytest

## 📜 Key Commands Used

Purpose	                             ➪                       Command
Activate venv (Linux)	             ➪               source venv/bin/activate
Activate venv (Windows)	             ➪               ./venv/Script/Activate
Install packages	                 ➪               pip install -r requirements.txt
Freeze dependencies	                 ➪               pip freeze | tee requirements.txt
Run all tests (with config)	         ➪               pytest
Run a single test file	             ➪               pytest tests/test_google.py
Run with screenshots & video	     ➪               pytest --headed --screenshot=on --video=on --html=reports/report.html
Git workflow	                     ➪               git init → git remote add origin <url> → git add . → git commit -m "..." → git push -u origin main
Undo staged files	                 ➪               git restore --staged <file>
Ignore tracked files later	         ➪               git rm -r --cached <path>
List ignored files	                 ➪               git status --ignored


## 🚀 How This Connects to Cloud/Infra & DevOps
This project isn't just about testing – it’s a building block for infrastructure reliability.

1. CI/CD Integration – The same test suite can run inside a GitLab CI pipeline after every code push, verifying that the Django app (or any web service) still works.
2. Synthetic Monitoring – Replace the manual curl with a scheduled Playwright script that logs into the app and reports broken functionality before users notice.
3. Infrastructure as Code Testing – After Terraform provisions a new VM, run this test suite against it to confirm the entire stack is healthy.
4. Containerisation – The test suite itself can be packed into a Docker image, making it portable across any cloud environment (AWS, Azure, GCP).

### Long‑term, I’ll extend this framework to:

1. Validate Nginx configurations, SELinux policies, and Kubernetes services.
2. Trigger alerts via webhook when a test fails.
3. Serve as an acceptance test for my Infrastructure as Code deployments.

## What I Learned

1. Managing Python virtual environments across different operating systems.
2. Writing reusable pytest fixtures with yield for setup/teardown.
3. Using Playwright’s sync API to automate real browser interactions.
4. Generating self‑contained HTML reports for test results.
5. Structuring a small project with .gitignore, requirements.txt, and pytest.ini.
6. The value of keeping everything in Git – the first step toward CI/CD.

## 📌 Status
Ongoing. I’m building this side‑by‑side with my Linux administration and cloud infrastructure studies. The goal is to eventually run this test suite automatically whenever I change my homelab setup, closing the loop between infrastructure and application health.