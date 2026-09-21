# CV Matcher

A local CV-to-job matching application powered by **Ollama + Qwen3 8B**.

CV Matcher runs locally using Docker and connects to a local Ollama instance running the Qwen3 8B model. It compares CVs against job descriptions and produces matching results without requiring your documents to be sent to a third-party cloud AI service.

> **Privacy note:** CV Matcher is designed for local processing. However, you should always review the application's configuration and source code before processing sensitive documents.

## Features

- 🧠 Local AI-powered CV matching with Qwen3 8B
- 🔒 CVs and job descriptions can remain on your local machine
- 🐳 Runs the application with Docker
- ⚡ Uses local Ollama for LLM inference
- 📄 Supports:
  - PDF
  - DOCX
  - TXT
  - Markdown (`.md`)
- 📁 CVs and job descriptions are stored in the local `data/` directory
- 📊 Matching results are saved locally
- 🪟 Includes a Windows dependency checker
- 🌐 No hosted AI API is required


## How It Works

The application runs inside Docker and communicates with Ollama running locally on your machine.


 ```text  Your computer
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ┌──────────────────┐                              │
│   │   CV Matcher     │                              │
│   │     Docker       │                              │
│   │                  │                              │
│   │  Parse documents │                              │
│   │        ↓         │                              │
│   │  Compare CV/job  │                              │
│   └────────┬─────────┘                              │
│            │                                        │
│            │ HTTP                                   │
│            ▼                                        │
│   ┌──────────────────┐                              │
│   │     Ollama       │                              │
│   │                  │                              │
│   │    Qwen3 8B      │                              │
│   └──────────────────┘                              │
│                                                     │
│   data/                                             │
│   ├── cvs/                                          │
│   ├── jobs/                                         │
│   └── results/                                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```


Your documents are processed by the application and sent to your local Ollama instance for matching.

The application does not require a hosted AI API.

## Requirements

You need the following installed:

- Python 3.12+
- Docker Desktop
- Ollama
- Qwen3 8B


## Windows

The repository includes a PowerShell dependency checker: `check.ps1`

The script checks whether the following dependencies are available:

- Python
- Docker
- Ollama
- Qwen3 8B

The script does not install, download, or modify these dependencies.

## Run the Dependency Checker

Open PowerShell in the project directory and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\check.ps1
```


The execution-policy change applies only to the current PowerShell process.

The checker reports missing dependencies and provides the relevant official download page.

For example:

```text
==============================================
       CV Matcher - Dependency Check
==============================================

This script only checks your system.
It will not download or install anything.

Checking Python...
[OK]      Python (Python 3.12.x)

Checking Docker...
[OK]      Docker (Docker version ...)

Checking Ollama...
[OK]      Ollama (ollama version ...)

Checking Ollama model...
[OK]      qwen3:8b

==============================================
                 Summary
==============================================

All dependencies are installed.

You should be ready to run CV Matcher.
```

If something is missing, the checker displays the relevant official website or command needed to resolve the issue.

After installing the missing dependencies, run the checker again:

```powershell
.\check.ps1
```

## Installing the Dependencies

If the dependency checker reports a missing dependency, install it from the relevant official source.

### Python

**Download Python from:**

https://www.python.org/downloads/

Python 3.12 or newer is recommended.

### Docker Desktop

**Download Docker Desktop from:**

https://www.docker.com/products/docker-desktop/

Make sure Docker Desktop is running before starting CV Matcher.

> Docker Desktop is a separate third-party product and is subject to Docker's own licensing and terms.

### Ollama

**Download Ollama from:**

https://ollama.com/download

After installing Ollama, download the Qwen3 8B model:

```bash
ollama pull qwen3:8b
```


Verify that the model is available:

```bash
ollama list
```

You should see:

```bash
qwen3:8b
```

## Running the Application
1. **Start Ollama**

Make sure Ollama is running and that Qwen3 8B is available:

```bash
ollama list
```

If necessary:

```bash
ollama pull qwen3:8b
```

2. **Start Docker**

Make sure Docker Desktop is running.

3. **Start CV Matcher**

From the project directory, run:

```bash
docker compose up --build
```

Docker will build the application and start the CV Matcher container.

4. **Open the Application**

Once the container is running, open the address configured by docker-compose.yml in your browser.

For example:

http://localhost:8000


If your docker-compose.yml uses a different port, use that port instead.

Documents

CV Matcher currently supports:

.pdf
.docx
.txt
.md

CVs

Place CVs in:

data/cvs/

Job Descriptions

Place job descriptions in:

data/jobs/

Matching Results

Matching results are stored in:

data/results/


Example:

data/
├── cvs/
│   ├── john-doe.pdf
│   └── jane-doe.docx
│
├── jobs/
│   ├── software-engineer.txt
│   └── data-scientist.md
│
└── results/
    └── ...

Local AI

CV Matcher uses Ollama as the local LLM runtime.

The default model is:

qwen3:8b


The application communicates with Ollama rather than using a hosted AI API.

This allows CVs and job descriptions to remain on the local machine rather than being uploaded to an external AI provider by the application.

However, local processing should not automatically be interpreted as a security guarantee. Review the application's configuration and network settings before processing sensitive information.

Docker and Ollama

The CV Matcher application runs inside Docker, while Ollama runs on the host machine.

The Docker container therefore needs to be able to reach the Ollama service running on the host.

The exact Ollama host address is configured in the project's Docker and application configuration.

On Docker Desktop, this commonly involves:

host.docker.internal


Check:

docker-compose.yml


and:

app/config.py


if you need to change the Ollama connection.

Configuration

Application configuration is handled in:

app/config.py


The Ollama client is implemented in:

app/ollama_client.py


Document parsing is handled in:

app/document_parser.py


Matching logic is handled in:

app/matcher.py


Prompt configuration is located in:

app/prompts/matching.py

Project Structure
cv-matcher/
│
├── check.ps1
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── config.py
│   ├── ollama_client.py
│   ├── document_parser.py
│   ├── matcher.py
│   │
│   ├── prompts/
│   │   └── matching.py
│   │
│   └── templates/
│       └── index.html
│
└── data/
    ├── cvs/
    │   └── .gitkeep
    ├── jobs/
    │   └── .gitkeep
    └── results/
        └── .gitkeep

Data and Privacy

CV Matcher is designed to run locally.

Your documents are stored under:

data/


The application does not require uploading CVs or job descriptions to a hosted AI service.

However, you should review the application's configuration and source code before using it with sensitive documents, particularly if you modify the Ollama connection or add external services.

Do Not Commit Personal Documents

The data/ directory is intended for local files.

Avoid committing:

CVs containing personal information

Job descriptions containing confidential information

Generated matching results containing personal data

Other sensitive documents

Consider adding the following to .gitignore:

data/cvs/*
data/jobs/*
data/results/*


You can keep the directories in Git by adding .gitkeep files:

data/
├── cvs/
│   └── .gitkeep
├── jobs/
│   └── .gitkeep
└── results/
    └── .gitkeep

Third-Party Software and Models

CV Matcher uses third-party software, libraries, and models.

These components are separate from the CV Matcher application code and remain subject to their own licenses and terms.

Qwen3

CV Matcher uses the Qwen3 8B open-weight model through Ollama.

Qwen3 is released under the Apache License 2.0. Refer to the official Qwen3 repository for the applicable license and model information:

https://github.com/QwenLM/Qwen3

The Qwen3 model is not included in this repository.

Users download the model separately through Ollama:

ollama pull qwen3:8b


Users are responsible for complying with the applicable terms when downloading, using, modifying, or redistributing the model.

Ollama

CV Matcher uses Ollama as the local model runtime.

Ollama is a separate third-party project. This repository does not include the Ollama software itself.

Official website:

https://ollama.com/

Docker

CV Matcher uses Docker to run the application.

Docker and Docker Engine are separate third-party software components and are subject to their respective licenses and terms.

Official website:

https://www.docker.com/

Docker Desktop

Docker Desktop is used as part of the recommended Windows development/runtime environment.

Docker Desktop is a separate third-party product and is subject to Docker's licensing, subscription, and usage terms.

Official information:

https://www.docker.com/products/docker-desktop/

Python Dependencies

CV Matcher uses Python packages listed in:

requirements.txt


These packages are separate third-party components and may have their own licenses.

Users and redistributors should review the licenses of the dependencies listed in requirements.txt.

Troubleshooting
Ollama Is Not Detected

Check that Ollama is installed:

ollama --version


Then check the installed models:

ollama list


Make sure Qwen3 8B is installed:

ollama pull qwen3:8b

Docker Cannot Connect to Ollama

Make sure:

Ollama is running on the host.

Qwen3 8B is installed.

Docker Desktop is running.

The Ollama URL in the application configuration points to the correct host.

The Docker container can reach the Ollama service.

On Docker Desktop, the host is commonly accessible as:

host.docker.internal

Qwen3 Is Missing

Run:

ollama pull qwen3:8b


Then verify:

ollama list

Docker Container Does Not Start

Try rebuilding the container:

docker compose down
docker compose build --no-cache
docker compose up

Stopping the Application

Press Ctrl+C in the terminal running Docker Compose.

You can also run:

docker compose down

Disclaimer

CV Matcher is a tool for assisting with CV and job-description comparison.

Matching results are generated by an AI model and should be reviewed by a human. They should not be treated as definitive assessments of a candidate's qualifications, suitability, or employment prospects.

The application is not intended to make employment decisions automatically.

Users are responsible for reviewing AI-generated results and ensuring that their use of the application complies with applicable laws, regulations, privacy requirements, and organizational policies.