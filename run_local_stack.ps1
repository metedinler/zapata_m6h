$ErrorActionPreference = 'Stop'

Write-Output '== Zapata Local Stack Boot =='

$processes = @()

function Start-BackgroundProcess {
    param(
        [string]$Name,
        [string]$Command
    )

    Write-Output ("Starting: " + $Name)
    $proc = Start-Process -FilePath "powershell" -ArgumentList "-NoProfile", "-Command", $Command -PassThru
    return $proc
}

$processes += Start-BackgroundProcess -Name 'Ollama Serve' -Command 'ollama serve'
$processes += Start-BackgroundProcess -Name 'Retrieve API' -Command 'conda run --live-stream --name zapata_m6h python retrieve_api.py'
$processes += Start-BackgroundProcess -Name 'Zapata REST API' -Command 'conda run --live-stream --name zapata_m6h python rest_api.py'

Start-Sleep -Seconds 4

$targets = @(
    'http://127.0.0.1:11434/api/tags',
    'http://127.0.0.1:8000/status',
    'http://127.0.0.1:5000/status'
)

foreach ($url in $targets) {
    $code = curl.exe -s -o NUL -w "%{http_code}" $url
    if ($code -eq '000') {
        Write-Output ("DOWN " + $url)
    } else {
        Write-Output ("UP " + $url + " " + $code)
    }
}

Write-Output '== Stack start attempted. Use Stop-Process for listed PIDs if needed =='
$processes | ForEach-Object { Write-Output ("PID " + $_.Id) }
