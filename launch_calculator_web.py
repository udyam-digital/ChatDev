#!/usr/bin/env python3
"""
Web-based Simple Calculator
This version uses a web browser to display the calculator GUI,
avoiding Tkinter compatibility issues on macOS.
"""

import webbrowser
import http.server
import socketserver
import threading
import os
import sys

# HTML/CSS/JavaScript for the calculator
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .calculator {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 30px;
            width: 400px;
            max-width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
            font-size: 24px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        
        button {
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        button.operation {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        button.operation:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button.operation:active {
            transform: translateY(0);
        }
        
        button.clear {
            background: #ff6b6b;
            color: white;
            grid-column: span 2;
        }
        
        button.clear:hover {
            background: #ff5252;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .result {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-top: 20px;
        }
        
        .result-label {
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }
        
        .result-value {
            color: #667eea;
            font-size: 32px;
            font-weight: bold;
        }
        
        .error {
            background: #ffe0e0;
            color: #d32f2f;
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
            display: none;
        }
        
        .info {
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>🧮 Simple Calculator</h1>
        
        <div class="input-group">
            <label for="firstNumber">First Number</label>
            <input type="number" id="firstNumber" placeholder="Enter first number" step="any">
        </div>
        
        <div class="input-group">
            <label for="secondNumber">Second Number</label>
            <input type="number" id="secondNumber" placeholder="Enter second number" step="any">
        </div>
        
        <div class="button-grid">
            <button class="operation" onclick="calculate('add')">Add</button>
            <button class="operation" onclick="calculate('subtract')">Subtract</button>
            <button class="operation" onclick="calculate('multiply')">Multiply</button>
            <button class="operation" onclick="calculate('divide')">Divide</button>
            <button class="clear" onclick="clearAll()">Clear</button>
        </div>
        
        <div class="result">
            <div class="result-label">Result</div>
            <div class="result-value" id="result">-</div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="info">
            Web-based Calculator | Close this browser tab to exit
        </div>
    </div>
    
    <script>
        function getNumbers() {
            const first = parseFloat(document.getElementById('firstNumber').value);
            const second = parseFloat(document.getElementById('secondNumber').value);
            
            if (isNaN(first) || isNaN(second)) {
                showError('Please enter valid numbers');
                return null;
            }
            
            return { first, second };
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 3000);
        }
        
        function calculate(operation) {
            const numbers = getNumbers();
            if (!numbers) return;
            
            let result;
            switch(operation) {
                case 'add':
                    result = numbers.first + numbers.second;
                    break;
                case 'subtract':
                    result = numbers.first - numbers.second;
                    break;
                case 'multiply':
                    result = numbers.first * numbers.second;
                    break;
                case 'divide':
                    if (numbers.second === 0) {
                        showError('Cannot divide by zero');
                        return;
                    }
                    result = numbers.first / numbers.second;
                    break;
            }
            
            document.getElementById('result').textContent = result.toFixed(2);
        }
        
        function clearAll() {
            document.getElementById('firstNumber').value = '';
            document.getElementById('secondNumber').value = '';
            document.getElementById('result').textContent = '-';
        }
        
        // Allow Enter key to add numbers
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                calculate('add');
            }
        });
    </script>
</body>
</html>
"""

def create_calculator_html():
    """Create the calculator HTML file."""
    calc_dir = os.path.expanduser("~/udyam/external/chatdev/WareHouse/SimpleCalc_DefaultOrganization_20251110004427")
    html_path = os.path.join(calc_dir, "calculator.html")
    
    with open(html_path, 'w') as f:
        f.write(CALCULATOR_HTML)
    
    return html_path

def start_server(port=8000):
    """Start a simple HTTP server."""
    calc_dir = os.path.expanduser("~/udyam/external/chatdev/WareHouse/SimpleCalc_DefaultOrganization_20251110004427")
    os.chdir(calc_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"✅ Server started at http://localhost:{port}")
    httpd.serve_forever()

def main():
    """Main function to launch the web-based calculator."""
    print("=" * 60)
    print("🧮 Web-Based Simple Calculator Launcher")
    print("=" * 60)
    print()
    
    # Create the HTML file
    print("Creating calculator HTML...")
    html_path = create_calculator_html()
    print(f"✅ Calculator HTML created at: {html_path}")
    print()
    
    # Find an available port
    port = 8000
    while True:
        try:
            # Test if port is available
            test_socket = socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler)
            test_socket.server_close()
            break
        except OSError:
            port += 1
            if port > 8100:
                print("❌ Could not find an available port")
                sys.exit(1)
    
    # Start the server in a background thread
    print(f"Starting web server on port {port}...")
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()
    
    # Give the server a moment to start
    import time
    time.sleep(1)
    
    # Open the calculator in the default browser
    url = f"http://localhost:{port}/calculator.html"
    print(f"\n🚀 Opening calculator in browser: {url}")
    print()
    print("=" * 60)
    print("✅ Calculator is now running in your browser!")
    print("=" * 60)
    print()
    print("Instructions:")
    print("  • Enter two numbers in the input fields")
    print("  • Click an operation button (Add, Subtract, Multiply, Divide)")
    print("  • Press 'Clear' to reset")
    print("  • Close the browser tab when done")
    print()
    print("Press Ctrl+C to shut down the server")
    print("=" * 60)
    
    webbrowser.open(url)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✅ Calculator server shut down. Goodbye!")

if __name__ == "__main__":
    main()
