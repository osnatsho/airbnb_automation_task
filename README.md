# Airbnb Automation Task

## Overview

This is a test automation project built with [Playwright](https://playwright.dev/python/) and [Pytest](https://docs.pytest.org/), implementing the **Page Object Model (POM)** design pattern.

The project performs automated testing on the Airbnb site and includes assertions, structured page objects, and proper locator usage.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/airbnb_automation_task.git
cd airbnb_automation_task

#create the environment

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

## install the dependencies

pip install -r requirements.txt
playwright install

##how to run?

pytest tests/test_airbnb.py --headed

