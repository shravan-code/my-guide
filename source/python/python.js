document.addEventListener('DOMContentLoaded', function() {
  const headers = document.querySelectorAll('.accordion-header');
  headers.forEach(header => header.addEventListener('click', function() {
    const section = header.closest('.accordion-section');
    const isOpen = section.classList.contains('open');
    document.querySelectorAll('.accordion-section').forEach(s => s.classList.remove('open'));
    if (!isOpen) section.classList.add('open');
  }));
});
