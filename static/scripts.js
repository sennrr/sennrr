// Voorbeeld van een simpele hamburgermenu toggle functie
const menuToggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('.menu');
menuToggle.addEventListener('click', () => {
    menu.classList.toggle('active');
});
