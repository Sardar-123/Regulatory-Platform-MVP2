const optionsDropdown = document.querySelector('.dropdown-content1');
const options = document.querySelectorAll('.dropdown-content1 a');

options.forEach(option => {
    option.addEventListener('click', (event) => {
        event.preventDefault();
        document.querySelector('.dropbtn1').textContent = option.textContent;
        optionsDropdown.style.display = 'none';
    });
});

document.querySelector('.dropbtn1').addEventListener('click', () => {
    optionsDropdown.style.display = 'block';
});

document.addEventListener('click', (event) => {
    if (!event.target.closest('.dropdown1')) {
        optionsDropdown.style.display = 'none';
    }
});