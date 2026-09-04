param(
    [string] $CsvDir
)

$ErrorActionPreference = "Stop"

function Count-Terminators([string] $s)
{
    # Fold CRLF first so CR, LF, and CRLF each count as one terminator.
    $folded = $s.Replace("`r`n", "`n")
    return ($folded.Length - $folded.Replace("`n", "").Length) +
           ($folded.Length - $folded.Replace("`r", "").Length)
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$configuredCsvDir = if ([string]::IsNullOrWhiteSpace($CsvDir)) {
    $env:XIVL_CSV_DIR
} else {
    $CsvDir
}
if ([string]::IsNullOrWhiteSpace($configuredCsvDir))
{
    $configuredCsvDir = Join-Path $repoRoot "csv"
}
if (-not (Test-Path -LiteralPath $configuredCsvDir -PathType Container))
{
    throw "Decoded CSV folder does not exist: $configuredCsvDir"
}
$csvDir = (Resolve-Path -LiteralPath $configuredCsvDir).Path
$manifestDir = Join-Path $repoRoot "manifests"

New-Item -ItemType Directory -Path $manifestDir -Force | Out-Null

$tables = @()
$files = Get-ChildItem -Path $csvDir -File -Filter "*.csv" | Sort-Object Name

$sha256 = [System.Security.Cryptography.SHA256]::Create()
try
{
    foreach ($file in $files)
    {
        $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
        $hash = [System.BitConverter]::ToString($sha256.ComputeHash($bytes)).Replace("-", "")

        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
        # Keep lineCount aligned with the CR/LF/CRLF convention below.
        $lineCount = (Count-Terminators $text)
        $last = if ($bytes.Length -gt 0) { $bytes[$bytes.Length - 1] } else { 10 }
        $unterminated = ($last -ne 10 -and $last -ne 13)
        if ($unterminated)
        {
            $lineCount++
        }

        # Count CSV records outside quoted fields. Unbalanced quotes fail loudly.
        $segments = $text.Split('"')
        if ($segments.Length % 2 -eq 0)
        {
            throw "Unbalanced quote characters in $($file.Name); not extractor-shaped CSV."
        }
        $recordCount = 0
        for ($i = 0; $i -lt $segments.Length; $i += 2)
        {
            $recordCount += (Count-Terminators $segments[$i])
        }
        if ($unterminated)
        {
            $recordCount++
        }
        $dataRowCount = [Math]::Max(0, $recordCount - 2)

        $tables += [PSCustomObject]@{
            name = $file.Name
            relativePath = "csv/$($file.Name)"
            bytes = $file.Length
            sha256 = $hash
            lineCount = $lineCount
            dataRowCount = $dataRowCount
        }
    }
}
finally
{
    $sha256.Dispose()
}

$manifest = [PSCustomObject]@{
    version = "2012.09.19.0001"
    gameVersion = "1.23b"
    sourceType = "decoded_csv"
    sourcePath = "https://github.com/XIVLegacy/xivl-tools (first-party extraction; client game.ver 2012.09.19.0001)"
    csvPath = "csv"
    tableCount = $tables.Count
    totalBytes = ($tables | Measure-Object -Property bytes -Sum).Sum
}

$tablesJson = ($tables | ConvertTo-Json -Depth 8).Replace("`r`n", "`n")
$manifestJson = ($manifest | ConvertTo-Json -Depth 8).Replace("`r`n", "`n")

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path $manifestDir "tables.json"), $tablesJson, $utf8NoBom)
[System.IO.File]::WriteAllText((Join-Path $manifestDir "manifest.json"), $manifestJson, $utf8NoBom)

Write-Host "Built manifest for $($tables.Count) decoded CSV files."
