<#
prepare_repo.ps1

Usage examples:
  # Copy files, init repo, commit locally
  .\prepare_repo.ps1 -RepoName "AI-Tools-Project-Unique" -Files @("C:\path\to\file.mp4", "C:\path\to\screenshot.png")

  # Copy files and push to provided remote URL
  .\prepare_repo.ps1 -RepoName "AI-Tools-Project-Unique" -RemoteUrl "https://github.com/yourname/yourrepo.git" -Files @(...) 
#>

param(
    [string]$RepoName = "AI-Tools-Project",
    [string]$RemoteUrl = "",
    [string[]]$Files = @()
)

Write-Host "Preparing repository: $RepoName"

# Create an assets folder and copy files there
$assetsDir = Join-Path -Path (Get-Location) -ChildPath "assets"
if (-not (Test-Path $assetsDir)) { New-Item -ItemType Directory -Path $assetsDir | Out-Null }

foreach ($f in $Files) {
    if (Test-Path $f) {
        try {
            Copy-Item -Path $f -Destination $assetsDir -Force
            Write-Host "Copied: $f"
        } catch {
            Write-Warning "Failed to copy $f : $_"
        }
    } else {
        Write-Warning "File not found: $f"
    }
}

# Initialize git repo if not exists
if (-not (Test-Path ".git")) {
    git init
    git checkout -b main
    Write-Host "Initialized new git repository and switched to 'main' branch."
} else {
    Write-Host "Git repository already initialized."
}

# Add files and commit
git add .
git commit -m 'Initial commit - project files and assets' || Write-Host 'No changes to commit or commit failed.'

if ($RemoteUrl -ne "") {
    try {
        git remote remove origin 2>$null
    } catch {}
    git remote add origin $RemoteUrl
    Write-Host "Added remote origin: $RemoteUrl"

    Write-Host "Pushing to remote (origin main). You may be prompted for credentials."
    git push -u origin main
}

Write-Host 'Repository preparation complete.'
