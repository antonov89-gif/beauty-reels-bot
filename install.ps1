# Установка и запуск UGC Beauty Reels Bot на Windows.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1            # установка
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Mode Run  # запуск
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Mode Install -Launch
param(
  [ValidateSet("Install", "Run")]
  [string]$Mode = "Install",
  [switch]$Launch
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$VenvDir = Join-Path $Root ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$EnvFile = Join-Path $Root ".env"
$Script = Join-Path $Root "reels_mvp.py"

# Переменные, которые читает reels_mvp.py. Обязателен только токен Telegram.
$Settings = @(
  @{ Name = "TELEGRAM_BOT_TOKEN"; Required = $true; Prompt = "Токен Telegram-бота (от @BotFather)" },
  @{ Name = "OPENAI_API_KEY"; Required = $false; Prompt = "OpenAI API key (Enter — пропустить)" },
  @{ Name = "INSTAGRAM_BUSINESS_ACCOUNT_ID"; Required = $false; Prompt = "Instagram Business Account ID (Enter — пропустить)" },
  @{ Name = "INSTAGRAM_ACCESS_TOKEN"; Required = $false; Prompt = "Instagram Access Token (Enter — пропустить)" }
)

function Write-Step([string]$Text) { Write-Host "==> $Text" -ForegroundColor Cyan }

function Find-Python {
  foreach ($candidate in @(@("py", "-3"), @("python"), @("python3"))) {
    if (-not (Get-Command $candidate[0] -ErrorAction SilentlyContinue)) { continue }
    $extra = @($candidate | Select-Object -Skip 1)
    $version = & $candidate[0] @extra -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
    if ($LASTEXITCODE -eq 0 -and [version]$version -ge [version]"3.10") { return ,$candidate }
  }
  throw "Не найден Python 3.10+. Установите его с https://www.python.org/downloads/ (галочка 'Add python.exe to PATH') и запустите скрипт снова."
}

function Read-EnvFile {
  $values = [ordered]@{}
  if (Test-Path -LiteralPath $EnvFile) {
    foreach ($line in Get-Content -LiteralPath $EnvFile -Encoding UTF8) {
      if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$') { $values[$Matches[1]] = $Matches[2].Trim() }
    }
  }
  return $values
}

function Write-EnvFile($Values) {
  $lines = foreach ($key in $Values.Keys) { "$key=$($Values[$key])" }
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [IO.File]::WriteAllLines($EnvFile, [string[]]$lines, $utf8NoBom)
}

function Install-Bot {
  Write-Step "Поиск Python"
  $python = Find-Python
  $pyArgs = @($python | Select-Object -Skip 1)

  if (-not (Test-Path -LiteralPath $VenvPython)) {
    Write-Step "Создание виртуального окружения в .venv"
    & $python[0] @pyArgs -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { throw "Не удалось создать виртуальное окружение." }
  }

  Write-Step "Установка зависимостей из requirements.txt"
  & $VenvPython -m pip install --upgrade pip --quiet
  & $VenvPython -m pip install -r (Join-Path $Root "requirements.txt")
  if ($LASTEXITCODE -ne 0) { throw "Не удалось установить зависимости." }

  Write-Step "Настройка ключей (сохраняются в .env рядом со скриптом)"
  $values = Read-EnvFile
  foreach ($setting in $Settings) {
    $current = $values[$setting.Name]
    $hint = if ($current) { " [Enter — оставить текущее]" } else { "" }
    $answer = ([string](Read-Host "$($setting.Prompt)$hint")).Trim()
    if ($answer) { $values[$setting.Name] = $answer }
    elseif ($setting.Required -and -not $current) { throw "$($setting.Name) обязателен. Ничего не сохранено." }
  }
  Write-EnvFile $values

  Write-Host "[OK] Установка завершена. Запуск: .\install.ps1 -Mode Run" -ForegroundColor Green
}

function Start-Bot {
  if (-not (Test-Path -LiteralPath $VenvPython)) { throw "Окружение не установлено. Сначала выполните .\install.ps1" }
  $values = Read-EnvFile
  if (-not $values["TELEGRAM_BOT_TOKEN"]) { throw "В .env нет TELEGRAM_BOT_TOKEN. Выполните .\install.ps1 ещё раз." }
  foreach ($key in $values.Keys) { Set-Item -Path "Env:$key" -Value $values[$key] }
  $env:PYTHONUTF8 = "1"

  Write-Step "Запуск бота (Ctrl+C — остановить)"
  Push-Location $Root
  try { & $VenvPython $Script } finally { Pop-Location }
}

try {
  switch ($Mode) {
    "Install" { Install-Bot; if ($Launch) { Start-Bot } }
    "Run" { Start-Bot }
  }
} catch {
  Write-Host "[ОШИБКА] $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}
