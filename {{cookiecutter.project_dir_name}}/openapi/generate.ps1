param (
    [Parameter(Mandatory = $true)]
    [string]$ServiceName
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = (Get-Item "$ScriptDir\..").FullName

$InputSpec = "openapi/$ServiceName/openapi.yaml"
# We output to root and use the relative folder as packageName to ensure correct filesystem alignment
$FullPackageName = "openapi.$ServiceName"

if (-not (Test-Path "$RootDir/$InputSpec")) {
    Write-Error "Specification not found at $RootDir/$InputSpec"
    exit 1
}

Write-Host "Generating Python FastAPI models for $ServiceName with package $FullPackageName..."

# Clean up previous generation to remove stale files (e.g. deleted APIs)
$GenDir = Join-Path (Join-Path $RootDir "openapi") $ServiceName
$DirsToClean = @("apis", "models")
foreach ($Dir in $DirsToClean) {
    $PathToClean = Join-Path $GenDir $Dir
    if (Test-Path $PathToClean) {
        Write-Host "Cleaning $PathToClean..."
        Remove-Item $PathToClean -Recurse -Force | Out-Null
    }
}

docker run --rm -v "$RootDir`:/local" openapitools/openapi-generator-cli generate `
    -i "/local/$InputSpec" `
    -g python-fastapi `
    -o "/local" `
    --global-property "apis,models,supportingFiles,apiTests=false,modelTests=false" `
    --additional-properties="packageName=$FullPackageName,sourceFolder=.,skipFormModel=false"

# Ensure all parent directories have __init__.py to be valid packages
$PathParts = @("openapi", $ServiceName)
$CurrentPath = $RootDir
foreach ($Part in $PathParts) {
    $CurrentPath = Join-Path $CurrentPath $Part
    if (-not (Test-Path $CurrentPath)) {
        New-Item -ItemType Directory -Path $CurrentPath -Force | Out-Null
    }
    if (-not (Test-Path (Join-Path $CurrentPath "__init__.py"))) {
        New-Item -ItemType File -Path (Join-Path $CurrentPath "__init__.py") -Force | Out-Null
    }
}



Write-Host "Generation complete. Access via: import $FullPackageName"
