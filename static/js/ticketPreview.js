const form = document.getElementById('ticketForm');
const pdfPreview = document.getElementById('pdfPreview');
const downloadBtn = document.getElementById('downloadBtn');

form.addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = new FormData(form);
  fetch('/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'  // AJAX detect for preview
    }
  })
  .then(res => res.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    pdfPreview.src = url;
    pdfPreview.style.display = 'block';
  })
  .catch(err => console.error(err));
});

downloadBtn.addEventListener('click', function() {
  // Temporarily disable AJAX by submitting normal form
  form.removeEventListener('submit', previewHandler);
  form.submit();
});
