const optionsDropdown = document.querySelector('.dropdown-content');
const options = document.querySelectorAll('.dropdown-content a');

options.forEach(option => {
    option.addEventListener('click', (event) => {
        event.preventDefault();
        document.querySelector('.dropbtn').textContent = option.textContent;
        optionsDropdown.style.display = 'none';
    });
});

document.querySelector('.dropbtn').addEventListener('click', () => {
    optionsDropdown.style.display = 'block';
});

document.addEventListener('click', (event) => {
    if (!event.target.closest('.dropdown')) {
        optionsDropdown.style.display = 'none';
    }
});

