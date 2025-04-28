# Name: Project AI RMF Tool
# Description: Collects patch info from Windows 11 systems and sends to a central server



if (-not (Test-Path "$HOME\.ssh\id_ed25519" -PathType Leaf)) {

    Write-Host "No existing SSH key. Generating new key..."
    ssh-keygen 
    Write-Host "SSH key generation successful."
    Write-Host "Starting SSH agent..."
    Start-Service ssh-agent
    Get-Service ssh-agent | Set-Service -StartupType Automatic
    ssh-add ~\.ssh\id_ed25519

}
else {
    Write-Host "SSH key already exists"
}

# Write-Host "Please authenticate to server:"

type ~\.ssh\id_ed25519.pub | ssh swopec2@kb322-18.cs.wwu.edu "cat >> .ssh/authorized_keys"
#ssh-copy-id -p 922 swopec2@kb322-18.cs.wwu.edu

Write-Host "Server authentication successful."
Write-Host "Installation complete." 