# shipshape-run for Windows PowerShell: finds Git's bash and runs shipshape-run.sh with the same arguments.
#   .\tools\shipshape-run.ps1 --agent codex "add a /health endpoint"
$bash = (Get-Command bash -ErrorAction SilentlyContinue).Source
if (-not $bash) {
    $git = (Get-Command git -ErrorAction SilentlyContinue).Source
    if ($git) { $bash = Join-Path (Split-Path (Split-Path $git)) 'bin\bash.exe' }
}
if (-not $bash -or -not (Test-Path $bash)) { Write-Error 'shipshape-run needs Git for Windows (its bash). Install it from git-scm.com.'; exit 2 }
& $bash (Join-Path $PSScriptRoot 'shipshape-run.sh') @args
exit $LASTEXITCODE
