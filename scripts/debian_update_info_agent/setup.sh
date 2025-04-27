EXISTING_KEY=$HOME/.ssh/id_rsa

if [ ! -f "$EXISTING_KEY" ]; then
	echo "No existing SSH key. Generating new key..."
	ssh-keygen -t rsa -b 4096 -f "$EXISTING_KEY" -N ""
	echo "SSH key generation successful."
	echo "Starting SSH agent..."
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_rsa
else
	echo "SSH key already exists."
fi

echo "Please authenticate to server:"

ssh-copy-id -p 922 swopec2@kb322-18.cs.wwu.edu 

mkdir rmfclient

echo "Server authentication successful."
echo "Installation complete." 
