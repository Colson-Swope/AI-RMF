# Name: Project AI RMF Tool
# Description: Collects patch info from Windows 11 systems and sends to a central server

# Instructions:
# Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
# Install-Module PSWindowsUpdate -Force -Scope CurrentUser
# Import-Module PSWindowsUpdate
# Run: .\collect_patch_info.ps1

# Import PSWINDOWSUPDATE
Import-Module PSWindowsUpdate
# Define file path
$REPORT_FILE = "windows_patch_report.txt"

# Get system info
$DATE = Get-Date -Format "MM-dd-yyyy"
$TIME = Get-Date -Format "HH:mm:ss"
$OS_NAME = (Get-CimInstance Win32_OperatingSystem).Caption
$OS_VERSION = (Get-CimInstance Win32_OperatingSystem).Version
$COMPUTER_NAME = $env:COMPUTERNAME
# $IP_ADDR = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notmatch "Loopback"} | Select-Object -ExpandProperty IPAddress | Select-Object -First 1)

$systemInfo = @"
Date: $DATE
Time: $TIME
Operating System: $OS_NAME
OS Version: $OS_VERSION
Computer Name: $COMPUTER_NAME
IP Address: $IP_ADDR

"@

# Force a scan for updates if possible
if (Get-Command Invoke-WUScan -ErrorAction SilentlyContinue) {
    Invoke-WUScan | Out-Null
}

# Get pending Windows updates
$pendingUpdates = Get-WindowsUpdate -AcceptAll -IgnoreReboot -Verbose
if ($pendingUpdates) {
    $patchInfo = "Pending Updates:`n"
    foreach ($update in $pendingUpdates) {
        $title = $update.Title
        $kbArray = @($update.KBArticleIDs)
        $kb = if ($kbArray.Count -gt 0) { $kbArray -join ", " } else { "N/A" }
        $size = $update.Size
        $patchInfo += "Title: $title`nKB: $kb`nSize: $size`n`n"
    }
} else {
    $patchInfo = "No pending updates.`n"
}

# Check for pending reboot
if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired") {
    $patchInfo += "`nSystem pending reboot. Some updates may require a restart.`n"
}

# Collect installed patches
$installedPatches = Get-HotFix | Select-Object HotFixID, Description, InstalledOn
$patchInfo += "`nInstalled Patches:`n"
$installedPatches | ForEach-Object {
    $patchInfo += "ID: $($_.HotFixID)`nDescription: $($_.Description)`nInstalled On: $($_.InstalledOn)`n`n"
}

# Combine system info and patch info into one file
$allInfo = $systemInfo + $patchInfo
$allInfo | Set-Content -Path $REPORT_FILE
