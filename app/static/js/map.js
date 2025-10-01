const map = L.map('map').setView([51.9194, 19.1451], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const markersLayer = L.layerGroup().addTo(map);

async function loadPins() {
  const response = await fetch('/pins');
  if (!response.ok) {
    console.error('Failed to load pins');
    return;
  }
  const pins = await response.json();
  markersLayer.clearLayers();
  pins.forEach((pin) => {
    const marker = L.marker([pin.latitude, pin.longitude]).addTo(markersLayer);
    const description = pin.description ? `<p>${pin.description}</p>` : '';
    marker.bindPopup(`
      <article class="pin-popup">
        <h3>${pin.title}</h3>
        ${description}
        <p class="pin-meta">Pinned by ${pin.owner.username} on ${new Date(pin.created_at).toLocaleString()}</p>
      </article>
    `);
  });
}

loadPins();

const dialog = document.getElementById('pin-dialog');
const pinForm = document.getElementById('pin-form');
const pinLocation = document.getElementById('pin-location');

let pendingCoordinates = null;

map.on('click', (event) => {
  pendingCoordinates = event.latlng;
  pinLocation.textContent = `Latitude: ${pendingCoordinates.lat.toFixed(5)}, Longitude: ${pendingCoordinates.lng.toFixed(5)}`;
  pinForm.reset();
  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  }
});

pinForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!pendingCoordinates) {
    return;
  }

  const formData = new FormData(pinForm);
  const payload = {
    title: formData.get('title'),
    description: formData.get('description'),
    latitude: pendingCoordinates.lat,
    longitude: pendingCoordinates.lng,
  };

  const response = await fetch('/pins', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (response.ok) {
    dialog.close();
    pendingCoordinates = null;
    await loadPins();
  } else {
    const result = await response.json();
    alert(result.errors?.join('\n') ?? 'Something went wrong while saving the pin.');
  }
});

if (!('showModal' in HTMLDialogElement.prototype)) {
  dialog.classList.add('dialog-fallback');
  dialog.open = false;
  dialog.style.display = 'none';
}
