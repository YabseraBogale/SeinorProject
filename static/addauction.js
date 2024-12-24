document.querySelectorAll('.step-4-upload-box').forEach(uploadBox => {
                    uploadBox.addEventListener('click', () => {
                        const input = document.createElement('input');
                        input.type = 'file';
                        input.accept = 'image/*';
                        
                        // Trigger the file selection dialog
                        input.addEventListener('change', (event) => {
                            const file = event.target.files[0];
                            if (file) {
                                const reader = new FileReader();
                                reader.onload = (e) => {
                                    uploadBox.innerHTML = ''; // Clear previous content
                                    const img = document.createElement('img');
                                    img.src = e.target.result; // Show preview
                                    uploadBox.appendChild(img);
                                };
                                reader.onerror = () => {
                                    alert('Failed to load image. Please try again.');
                                };
                                reader.readAsDataURL(file); // Read file content
                            } else {
                                alert('No file selected.');
                            }
                        });
            
                        input.click(); // Simulate a click on the input
                    });
});
        let currentStep = 1;
        const steps = document.querySelectorAll(".steps span");
        const formContainer = document.querySelector(".form");
        const stepNumber = document.getElementById("step-number");
        const stepTitle = document.getElementById("step-title");
        const backButton = document.querySelector(".back-btn");
        const nextButton = document.querySelector(".next-btn");

        // Titles for each step
        const stepTitles = {
            1: "Create a new auction",
            2: "Add a description",
            3: "Enter address details",
            4: "Review and Submit",
            5: "Submit Form",
        };

        function loadStep(step) {
            // Load the content from the template
            const template = document.getElementById(`step-${step}`);
            if (template) {
                formContainer.innerHTML = template.innerHTML;
            }

            // Update step title and number
            stepNumber.textContent = `0${step}`;
            stepTitle.textContent = stepTitles[step] || "Step";

            // Update button visibility
            backButton.style.display = step === 1 ? "none" : "inline-block";
            nextButton.textContent = step === 5 ? "Done" : "Next";
        }

        function goToStep(stepChange) {
            // Prevent "Done" logic from being triggered when navigating
            if (currentStep === 5 && stepChange > 0) {
                alert("Form submitted successfully!");
                return; // Stop further navigation
            }

            currentStep += stepChange;

            // Clamp currentStep between 1 and 5
            if (currentStep < 1) currentStep = 1;
            if (currentStep > 5) currentStep = 5;

            // Update step navigation
            steps.forEach((step, index) => {
                if (index + 1 === currentStep) {
                    step.classList.add("active");
                } else {
                    step.classList.remove("active");
                }
            });

            // Load the current step
            loadStep(currentStep);
        }

        // Load the first step on page load
        loadStep(currentStep);