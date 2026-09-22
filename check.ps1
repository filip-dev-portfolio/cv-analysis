# ============================================================
# CV Matcher - Windows Dependency Check
#
# This script ONLY checks whether required dependencies exist.
# It does NOT download or install anything.
#
# Required:
#   - Python
#   - Docker
#   - Ollama
#   - Qwen3 8B
#
# Usage:
#   Set-ExecutionPolicy -Scope Process Bypass
#   .\check.ps1
# ============================================================

$ErrorActionPreference = "SilentlyContinue"

$OLLAMA_MODEL = "qwen3:8b"

# Official websites
$PYTHON_URL = "https://www.python.org/downloads/"
$DOCKER_URL = "https://www.docker.com/products/docker-desktop/"
$OLLAMA_URL = "https://ollama.com/download"


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

function Command-Exists {
    param (
        [string]$Command
    )

    return $null -ne (
        Get-Command $Command -ErrorAction SilentlyContinue
    )
}


function Write-Installed {
    param (
        [string]$Name
    )

    Write-Host "[OK]      $Name" -ForegroundColor Green
}


function Write-Missing {
    param (
        [string]$Name,
        [string]$Url
    )

    Write-Host "[MISSING] $Name" -ForegroundColor Red
    Write-Host "          Download: $Url" -ForegroundColor DarkGray
}


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "       CV Matcher - Dependency Check" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script only checks your system." -ForegroundColor Gray
Write-Host "It will not download or install anything." -ForegroundColor Gray
Write-Host ""


# ============================================================
# Python
# ============================================================

Write-Host "Checking Python..." -ForegroundColor Yellow

if (Command-Exists "python") {

    try {
        $pythonVersion = python --version 2>&1
        Write-Installed "Python ($pythonVersion)"
    }
    catch {
        Write-Installed "Python"
    }

}
elseif (Command-Exists "py") {

    try {
        $pythonVersion = py --version 2>&1
        Write-Installed "Python ($pythonVersion)"
    }
    catch {
        Write-Installed "Python"
    }

}
else {

    Write-Missing "Python" $PYTHON_URL
}


# ============================================================
# Docker
# ============================================================

Write-Host ""
Write-Host "Checking Docker..." -ForegroundColor Yellow

if (Command-Exists "docker") {

    try {
        $dockerVersion = docker --version 2>&1
        Write-Installed "Docker ($dockerVersion)"
    }
    catch {
        Write-Installed "Docker"
    }

}
else {

    Write-Missing "Docker Desktop" $DOCKER_URL
}


# ============================================================
# Ollama
# ============================================================

Write-Host ""
Write-Host "Checking Ollama..." -ForegroundColor Yellow

$ollamaInstalled = Command-Exists "ollama"
$ollamaRunning = $false
$modelInstalled = $false

if ($ollamaInstalled) {

    # Check whether the Ollama service is actually running.
    # Ollama normally listens on localhost:11434.

    try {

        $ollamaConnection = Test-NetConnection `
            -ComputerName "localhost" `
            -Port 11434 `
            -WarningAction SilentlyContinue

        $ollamaRunning = $ollamaConnection.TcpTestSucceeded

    }
    catch {

        $ollamaRunning = $false
    }


    # --------------------------------------------------------
    # Ollama installed AND running
    # --------------------------------------------------------

    if ($ollamaRunning) {

        try {

            $ollamaVersion = ollama --version 2>&1

            Write-Installed "Ollama ($ollamaVersion)"

        }
        catch {

            Write-Installed "Ollama"
        }

    }

    # --------------------------------------------------------
    # Ollama installed BUT not running
    # --------------------------------------------------------

    else {

        Write-Host "[WARNING] Ollama is installed but not running." `
            -ForegroundColor Yellow

        Write-Host "          Start Ollama and run this check again." `
            -ForegroundColor DarkGray
    }

}
else {

    Write-Missing "Ollama" $OLLAMA_URL
}


# ============================================================
# Qwen3 8B
# ============================================================

Write-Host ""
Write-Host "Checking Ollama model..." -ForegroundColor Yellow

if (-not $ollamaInstalled) {

    Write-Host "[SKIPPED] $OLLAMA_MODEL" -ForegroundColor DarkYellow
    Write-Host "          Install Ollama first." -ForegroundColor DarkGray

}
elseif (-not $ollamaRunning) {

    Write-Host "[SKIPPED] $OLLAMA_MODEL" -ForegroundColor DarkYellow
    Write-Host "          Start Ollama first." -ForegroundColor DarkGray

}
else {

    try {

        $models = ollama list 2>$null

        if ($models -match [regex]::Escape($OLLAMA_MODEL)) {

            $modelInstalled = $true

            Write-Installed $OLLAMA_MODEL

        }
        else {

            Write-Host "[MISSING] $OLLAMA_MODEL" -ForegroundColor Red
            Write-Host ""
            Write-Host "          Ollama is running, but the model is missing." `
                -ForegroundColor DarkGray

            Write-Host "          Run:" -ForegroundColor DarkGray
            Write-Host "          ollama pull $OLLAMA_MODEL" `
                -ForegroundColor White
        }

    }
    catch {

        Write-Host "[ERROR]   Could not check Ollama models." `
            -ForegroundColor Red
    }
}


# ============================================================
# Summary
# ============================================================

Write-Host ""
Write-Host "==============================================" `
    -ForegroundColor Cyan

Write-Host "                 Summary" `
    -ForegroundColor Cyan

Write-Host "==============================================" `
    -ForegroundColor Cyan

Write-Host ""

$allInstalled = (
    (
        (Command-Exists "python") -or
        (Command-Exists "py")
    ) -and
    (Command-Exists "docker") -and
    $ollamaInstalled -and
    $ollamaRunning -and
    $modelInstalled
)


if ($allInstalled) {

    Write-Host "All dependencies are installed." `
        -ForegroundColor Green

    Write-Host ""
    Write-Host "You should be ready to run CV Matcher." `
        -ForegroundColor Green

}
else {

    Write-Host "One or more dependencies are missing." `
        -ForegroundColor Yellow

    Write-Host ""
    Write-Host "Install the missing dependencies using" `
        -ForegroundColor Yellow

    Write-Host "the official websites shown above." `
        -ForegroundColor Yellow
}

Write-Host ""
