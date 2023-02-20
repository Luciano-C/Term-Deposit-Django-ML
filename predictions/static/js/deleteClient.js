const deleteButton = document.querySelector('#deleteButton');
deleteButton.addEventListener('click', () => {
    if (confirm('Are you sure you want to delete this client')) {
        const methodInput = document.querySelector('#methodChanger');
        methodInput.setAttribute('value', 'DELETE');
        form = document.querySelector('#clientForm');
        form.submit();
    }
})