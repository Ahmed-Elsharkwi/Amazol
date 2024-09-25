function createCustomWindowAndFetch(fetchUrl) {
    // Create a new window
    const newWindow = window.open('', '_blank', 'width=400,height=300');
  
    if (newWindow) {
      // Create the HTML content
      const htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Custom Window</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
              margin: 0;
              background-color: #f0f0f0;
            }
            .container {
              text-align: center;
              padding: 20px;
              background-color: white;
              border-radius: 8px;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
              color: #333;
            }
            #status {
              margin-top: 20px;
              font-style: italic;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>Custom Window</h1>
            <p>This window was created dynamically.</p>
            <div id="status">Loading...</div>
          </div>
          <script>
            window.addEventListener('load', function() {
              fetch('${fetchUrl}')
                .then(response => response.json())
                .then(data => {
                  document.getElementById('status').textContent = 'Fetch completed successfully!';
                  console.log('Fetch request successful:', data);
                  // You can do something with the data here
                })
                .catch(error => {
                  document.getElementById('status').textContent = 'Error in fetch request.';
                  console.error('Error in fetch request:', error);
                });
            });
          </script>
        </body>
        </html>
      `;
  
      // Write the HTML content to the new window
      newWindow.document.write(htmlContent);
      newWindow.document.close();
  
      console.log('New window created with custom HTML and CSS.');
    } else {
      console.error('Failed to open new window. Pop-up might be blocked.');
    }
  }
  
  // Usage example (this won't actually run in the Node.js environment, it's just for demonstration)
  // createCustomWindowAndFetch('https://api.example.com/data');
  
  // Simulating the function call for demonstration purposes
  console.log("Simulating function call: createCustomWindowAndFetch('https://api.example.com/data')");
  console.log("A new window would be created with custom HTML and CSS");
  console.log("After window load, a fetch request would be sent to https://api.example.com/data");