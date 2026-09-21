$mongoPath = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
$dbPath = Join-Path $PSScriptRoot "data\db"

if (-not (Test-Path $dbPath)) {
    New-Item -ItemType Directory -Path $dbPath | Out-Null
}

Start-Process -FilePath $mongoPath -ArgumentList "--dbpath `"$dbPath`"" -WindowStyle Minimized
Start-Sleep -Seconds 3

& "$PSScriptRoot\.venv\Scripts\python.exe" app.py
