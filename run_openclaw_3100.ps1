$ErrorActionPreference = 'Stop'

Write-Output '== OpenClaw Gateway (Port 3100) =='

$cfgPath = Join-Path $env:USERPROFILE '.openclaw\openclaw.json'
if (!(Test-Path $cfgPath)) {
    Write-Output "MISSING_CONFIG $cfgPath"
    exit 1
}

$cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
$token = $cfg.gateway.auth.token
if (-not $token) {
    Write-Output 'MISSING_GATEWAY_TOKEN'
    exit 1
}

$cmd = "$env:OPENCLAW_GATEWAY_PORT='3100'; openclaw gateway run --bind loopback"
$proc = Start-Process -FilePath 'powershell' -ArgumentList '-NoProfile', '-Command', $cmd -PassThru

Start-Sleep -Seconds 3

$env:OPENCLAW_GATEWAY_PORT='3100'
$health = openclaw health --json

Write-Output $health
Write-Output ('PID ' + $proc.Id)
Write-Output '== OpenClaw Gateway launch attempted on ws://127.0.0.1:3100 =='
