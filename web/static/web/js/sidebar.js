document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainSectionContainer = document.getElementById('main-section-container');

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('expand');
        if (sidebar.classList.contains('expand')) {
            mainSectionContainer.style.marginLeft = '260px';
        } else {
            mainSectionContainer.style.marginLeft = '70px';
        }
    });
});
