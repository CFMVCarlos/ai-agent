document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('agentForm');
    const promptInput = document.getElementById('prompt');
    const promptError = document.getElementById('promptError');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const responseArea = document.getElementById('responseArea');
    const responseText = document.getElementById('responseText');
    const verboseCheckbox = document.getElementById('verbose');

    // Simple Form Validation
    function validateForm() {
        let isValid = true;
        if (!promptInput.value.trim()) {
            promptError.classList.remove('hidden');
            promptInput.classList.add('border-red-400', 'ring-red-400/50');
            isValid = false;
        } else {
            promptError.classList.add('hidden');
            promptInput.classList.remove('border-red-400', 'ring-red-400/50');
        }
        return isValid;
    }

    // Handle Input change for validation clearance
    promptInput.addEventListener('input', () => {
        if (promptInput.value.trim()) {
            promptError.classList.add('hidden');
            promptInput.classList.remove('border-red-400', 'ring-red-400/50');
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateForm()) return;

        // UI Loading State
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        btnText.textContent = 'Running...';
        btnLoader.classList.remove('hidden');
        responseArea.classList.add('hidden');
        responseText.textContent = '';

        const payload = {
            prompt: promptInput.value.trim(),
            verbose: verboseCheckbox.checked
        };

        try {
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok || data.status === 'error') {
                throw new Error(data.message || 'An error occurred while running the agent.');
            }

            // Success State
            responseText.textContent = data.message;
            responseArea.classList.remove('hidden');
            responseArea.classList.add('fade-in');

            Toastify({
                text: "Agent completed successfully!",
                duration: 3000,
                close: true,
                gravity: "bottom", 
                position: "right", 
                style: {
                    background: "linear-gradient(to right, #10b981, #059669)",
                    borderRadius: "10px",
                    fontFamily: "sans-serif",
                    fontSize: "14px"
                },
            }).showToast();

        } catch (error) {
            // Error State
            console.error('Error:', error);
            
            Toastify({
                text: error.message || "Something went wrong.",
                duration: 4000,
                close: true,
                gravity: "bottom", 
                position: "right", 
                style: {
                    background: "linear-gradient(to right, #ef4444, #dc2626)",
                    borderRadius: "10px",
                    fontFamily: "sans-serif",
                    fontSize: "14px"
                },
            }).showToast();

        } finally {
            // Restore UI
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            btnText.textContent = 'Run Agent';
            btnLoader.classList.add('hidden');
        }
    });
});