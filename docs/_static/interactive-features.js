// Inject floating kill button only on localhost (local development)
document.addEventListener('DOMContentLoaded', function() {
    // Only show kill button on localhost
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        // Create kill button
        const killButton = document.createElement('button');
        killButton.className = 'kill-server-btn';
        killButton.innerHTML = '⏹';
        killButton.title = 'Stop Local Server';
        killButton.onclick = function() {
            if (confirm('Stop the local server?')) {
                window.location.href = '/kill';
            }
        };
        
        // Add to page
        document.body.appendChild(killButton);
    }
    
    // Add code toggle functionality for Jupyter Book
    const codeInputs = document.querySelectorAll('.cell_input');
    codeInputs.forEach(function(codeInput) {
        // Create toggle button
        const toggleButton = document.createElement('button');
        toggleButton.className = 'code-toggle-button';
        toggleButton.innerHTML = '📝 Show Code';
        toggleButton.title = 'Toggle code visibility';
        
        // Add click handler
        toggleButton.onclick = function() {
            if (codeInput.style.display === 'none') {
                codeInput.style.display = 'block';
                toggleButton.innerHTML = '🙈 Hide Code';
            } else {
                codeInput.style.display = 'none';
                toggleButton.innerHTML = '📝 Show Code';
            }
        };
        
        // Insert button before the code input
        codeInput.parentNode.insertBefore(toggleButton, codeInput);
        
        // Initially hide the code
        codeInput.style.display = 'none';
    });
    
    // Add global toggle for all code cells
    const body = document.body;
    const globalToggle = document.createElement('button');
    globalToggle.className = 'global-code-toggle';
    globalToggle.innerHTML = '📝 Show All Code';
    globalToggle.title = 'Toggle all code cells';
    // On narrow screens the fixed header bar paints over top:20px, hiding the
    // button; drop it below the header there.
    const narrow = window.matchMedia('(max-width: 768px)').matches;
    globalToggle.style.cssText = `
        position: fixed;
        top: ${narrow ? '64px' : '20px'};
        right: 20px;
        z-index: 1000;
        background-color: #0057b7;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 14px;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    `;
    
    let allCodeVisible = false;
    globalToggle.onclick = function() {
        const codeInputs = document.querySelectorAll('.cell_input');
        const toggleButtons = document.querySelectorAll('.code-toggle-button');
        
        if (allCodeVisible) {
            // Hide all code
            codeInputs.forEach(function(codeInput) {
                codeInput.style.display = 'none';
            });
            toggleButtons.forEach(function(button) {
                button.innerHTML = '📝 Show Code';
            });
            globalToggle.innerHTML = '📝 Show All Code';
            allCodeVisible = false;
        } else {
            // Show all code
            codeInputs.forEach(function(codeInput) {
                codeInput.style.display = 'block';
            });
            toggleButtons.forEach(function(button) {
                button.innerHTML = '🙈 Hide Code';
            });
            globalToggle.innerHTML = '🙈 Hide All Code';
            allCodeVisible = true;
        }
    };
    
    body.appendChild(globalToggle);
}); 