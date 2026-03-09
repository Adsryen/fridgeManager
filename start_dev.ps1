# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Starting Development Environment" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check backend dependencies
Write-Host "[1/4] Checking backend environment..." -ForegroundColor Yellow
$pythonCmd = "python"
if (Test-Path "venv/Scripts/python.exe") {
    $pythonCmd = "venv/Scripts/python.exe"
    Write-Host "  Using virtual environment" -ForegroundColor Green
} else {
    Write-Host "  Using system Python" -ForegroundColor Green
}

# Check frontend dependencies
Write-Host "[2/4] Checking frontend environment..." -ForegroundColor Yellow
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "  Warning: node_modules not found, installing..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

Write-Host ""
Write-Host "[3/4] Starting backend server (Flask)..." -ForegroundColor Yellow

# Start backend process
$backendProcess = Start-Process -FilePath $pythonCmd -ArgumentList "run.py" -PassThru -NoNewWindow -RedirectStandardOutput "backend.log" -RedirectStandardError "backend.err.log"

Start-Sleep -Seconds 2

Write-Host "[4/4] Starting frontend server (Vite)..." -ForegroundColor Yellow

# Start frontend process (use npm.cmd on Windows)
$npmCmd = "npm.cmd"
if (-not (Get-Command $npmCmd -ErrorAction SilentlyContinue)) {
    $npmCmd = "npm"
}
$frontendProcess = Start-Process -FilePath $npmCmd -ArgumentList "run", "dev" -WorkingDirectory "frontend" -PassThru -NoNewWindow -RedirectStandardOutput "frontend.log" -RedirectStandardError "frontend.err.log"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Services Started Successfully!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:  http://localhost:8080" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "  Press Ctrl+C to stop all services" -ForegroundColor Gray
Write-Host ""

# Track log files
$backendLogPath = Join-Path $PWD "backend.log"
$frontendLogPath = Join-Path $PWD "frontend.log"
$backendErrPath = Join-Path $PWD "backend.err.log"
$frontendErrPath = Join-Path $PWD "frontend.err.log"

# Initialize file positions
$backendPos = 0
$frontendPos = 0
$backendErrPos = 0
$frontendErrPos = 0

# Display logs in real-time
try {
    while ($true) {
        # Check if processes are still running
        if ($backendProcess.HasExited) {
            Write-Host ""
            Write-Host "Warning: Backend process exited unexpectedly (Exit Code: $($backendProcess.ExitCode))" -ForegroundColor Red
            break
        }
        if ($frontendProcess.HasExited) {
            Write-Host ""
            Write-Host "Warning: Frontend process exited unexpectedly (Exit Code: $($frontendProcess.ExitCode))" -ForegroundColor Red
            break
        }

        # Read backend logs
        if (Test-Path $backendLogPath) {
            $content = Get-Content $backendLogPath -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Length -gt $backendPos) {
                $newContent = $content.Substring($backendPos)
                $backendPos = $content.Length
                $newContent -split "`n" | Where-Object { $_ } | ForEach-Object {
                    Write-Host "[Backend] $_" -ForegroundColor Blue
                }
            }
        }

        # Read frontend logs
        if (Test-Path $frontendLogPath) {
            $content = Get-Content $frontendLogPath -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Length -gt $frontendPos) {
                $newContent = $content.Substring($frontendPos)
                $frontendPos = $content.Length
                $newContent -split "`n" | Where-Object { $_ } | ForEach-Object {
                    Write-Host "[Frontend] $_" -ForegroundColor Magenta
                }
            }
        }

        # Read backend error logs
        if (Test-Path $backendErrPath) {
            $content = Get-Content $backendErrPath -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Length -gt $backendErrPos) {
                $newContent = $content.Substring($backendErrPos)
                $backendErrPos = $content.Length
                $newContent -split "`n" | Where-Object { $_ } | ForEach-Object {
                    Write-Host "[Backend Error] $_" -ForegroundColor Red
                }
            }
        }

        # Read frontend error logs
        if (Test-Path $frontendErrPath) {
            $content = Get-Content $frontendErrPath -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Length -gt $frontendErrPos) {
                $newContent = $content.Substring($frontendErrPos)
                $frontendErrPos = $content.Length
                $newContent -split "`n" | Where-Object { $_ } | ForEach-Object {
                    Write-Host "[Frontend Error] $_" -ForegroundColor Red
                }
            }
        }

        Start-Sleep -Milliseconds 200
    }
}
finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    
    # Kill processes and their child processes
    if (-not $backendProcess.HasExited) {
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "  Backend stopped" -ForegroundColor Gray
    }
    
    if (-not $frontendProcess.HasExited) {
        # Kill npm and its child processes (node/vite)
        Get-Process | Where-Object { $_.ProcessName -match "node|vite|npm" } | Stop-Process -Force -ErrorAction SilentlyContinue
        Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "  Frontend stopped" -ForegroundColor Gray
    }
    
    # Clean up log files
    Start-Sleep -Seconds 1
    Remove-Item "backend.log" -ErrorAction SilentlyContinue
    Remove-Item "frontend.log" -ErrorAction SilentlyContinue
    Remove-Item "backend.err.log" -ErrorAction SilentlyContinue
    Remove-Item "frontend.err.log" -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "All services stopped" -ForegroundColor Green
}
