# Sit-Too-Long - PowerShell Installation Script
# Function: Auto-create virtual environment and install dependencies

param(
    [switch]$NoVenv = $false,
    [switch]$Quiet = $false,
    [switch]$Help = $false
)

# Parameter help
if ($Help) {
    Write-Host @"
Usage: .\install.ps1 [Options]

Options:
  -NoVenv     : Skip virtual environment creation, install to global Python
  -Quiet      : Quiet mode, reduce output messages
  -Help       : Show this help message

Examples:
  .\install.ps1                # Full installation (recommended)
  .\install.ps1 -Quiet         # Quiet mode
  .\install.ps1 -NoVenv        # Without virtual environment
"@
    exit 0
}

function Write-Info {
    param([string]$Message)
    if (-not $Quiet) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
}

function Write-Success {
    param([string]$Message)
    if (-not $Quiet) { Write-Host "[OK]  $Message" -ForegroundColor Green }
}

function Write-Error_ {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Warning_ {
    param([string]$Message)
    if (-not $Quiet) { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
}

# Check Python
if (-not $Quiet) {
    Write-Host "`n" + "="*50
    Write-Host "Sit-Too-Long - Installation" -ForegroundColor Green
    Write-Host "="*50 + "`n"
}

Write-Info "Checking Python environment..."

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Error_ "Python not found!"
    Write-Info "Please download and install Python 3.7+ (https://www.python.org)"
    exit 1
}

$pythonVersion = & $pythonCmd --version 2>&1
Write-Success "$pythonVersion"

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $scriptDir "venv"
$requirementsPath = Join-Path $scriptDir "requirements.txt"

# Check requirements.txt
if (-not (Test-Path $requirementsPath)) {
    Write-Error_ "requirements.txt not found!"
    exit 1
}

if ($NoVenv) {
    Write-Warning_ "Using global Python environment (not recommended)"
    Write-Info "Installing dependencies..."
    & $pythonCmd -m pip install -r $requirementsPath --user
} else {
    # Create virtual environment
    if (Test-Path $venvPath) {
        Write-Info "Virtual environment exists, skipping creation"
    } else {
        Write-Info "[1/3] Creating virtual environment..."
        & $pythonCmd -m venv $venvPath
        if ($LASTEXITCODE -ne 0) {
            Write-Error_ "Failed to create virtual environment!"
            exit 1
        }
        Write-Success "Virtual environment created successfully"
    }
    
    # Activate virtual environment
    Write-Info "[2/3] Activating virtual environment..."
    $activateCmd = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
    
    if (-not (Test-Path $activateCmd)) {
        Write-Error_ "Virtual environment activation script not found!"
        exit 1
    }
    
    & $activateCmd
    Write-Success "Virtual environment activated"
    
    # Install dependencies
    Write-Info "[3/3] Installing dependencies..."
    & $pythonCmd -m pip install -r $requirementsPath
}

if ($LASTEXITCODE -eq 0) {
    Write-Success "Dependencies installed successfully"
    if (-not $Quiet) {
        Write-Host "`n" + "="*50
        Write-Host "[OK] Installation complete!" -ForegroundColor Green
        Write-Host "="*50 + "`n"
        Write-Host "You can now run:"
        Write-Host "  python sit-too-long.py" -ForegroundColor Cyan
        Write-Host "  or double-click sit-too-long.bat`n" -ForegroundColor Cyan
    }
} else {
    Write-Error_ "Failed to install dependencies!"
    exit 1
}