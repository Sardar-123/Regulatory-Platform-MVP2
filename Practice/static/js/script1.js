function handleButtonClick() {
    const dropdown = document.getElementById("myDropdown");
    const selectedValue = dropdown.textContent;  // Use textContent to get the selected value
    if (selectedValue === "▼ SEPA") {
        console.log('sardar')
        // Redirect to another webpage (e.g., "sepa.html")
        window.location.href="{{ url_for('static', filename='sepa.html') }}";
    } else {
        // Show an "Invalid input" message
        alert("Invalid input. Please select SEPA.");
    }
  }