document.documentElement.classList.add('has-js');

const search = document.querySelector('#appearance-search');
if (search) {
  const rows = [...document.querySelectorAll('[data-appearance]')];
  const count = document.querySelector('#appearance-count');
  const empty = document.querySelector('#no-appearances');
  search.addEventListener('input', () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    rows.forEach(row => {
      const searchable = [...row.cells].map(cell => cell.textContent).join(' ') + ' ' + (row.querySelector('time')?.dateTime || '');
      const matches = searchable.toLocaleLowerCase().includes(query);
      row.hidden = !matches;
      if (matches) visible += 1;
    });
    if (count) count.textContent = query ? visible + ' of ' + rows.length + ' episodes' : rows.length + ' full episodes';
    if (empty) empty.hidden = visible > 0;
  });
}

const copyButton = document.querySelector('[data-copy-email]');
if (copyButton && navigator.clipboard) {
  copyButton.hidden = false;
  copyButton.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(copyButton.dataset.copyEmail);
      status.textContent = 'Email address copied.';
    } catch {
      status.textContent = 'Please select the email address above to copy it.';
    }
  });
}

const galleryLinks = [...document.querySelectorAll('[data-lightbox]')];
if (galleryLinks.length && typeof HTMLDialogElement !== 'undefined') {
  const dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Travel photograph');
  const close = document.createElement('button');
  close.className = 'close';
  close.type = 'button';
  close.textContent = 'Close ×';
  const photo = document.createElement('img');
  const caption = document.createElement('p');
  caption.className = 'lightbox-caption';
  dialog.append(close, photo, caption);
  document.body.append(dialog);
  let trigger;
  galleryLinks.forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    trigger = link;
    photo.src = link.href;
    photo.alt = link.querySelector('img').alt;
    caption.textContent = link.dataset.lightbox;
    dialog.showModal();
  }));
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { if (trigger) trigger.focus(); });
}
