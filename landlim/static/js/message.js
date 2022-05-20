for (const element of document.querySelectorAll('.notification > .notification-li > .delete')) {
    element.addEventListener('click', e => {
        e.target.parentElement.classList.add('is-hidden');
    });
}