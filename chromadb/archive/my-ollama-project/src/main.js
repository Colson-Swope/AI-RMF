import ollama from 'ollama';
import "./style.css"



document.getElementById('fetch-button').addEventListener('click', async () => {
  const responseDiv = document.getElementById('response');
  responseDiv.textContent = 'Fetching response...';

  // Define the multi-line prompt using a template literal
  const prompt = `
  `;

  try {
    const response = await ollama.chat({
      model: 'llama3.1',
      messages: [{ role: 'user', 
        content: prompt }]
    });
    responseDiv.textContent = response.message.content;
  } catch (error) {
    console.error('Error fetching response:', error);
    responseDiv.textContent = 'An error occurred. Check the console for details.';
  }
});