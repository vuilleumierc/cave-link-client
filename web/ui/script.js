document.getElementById('fetchBtn').addEventListener('click', () => {
  const variable = document.getElementById('variable').value;
  const start = document.getElementById('start').value;
  const end   = document.getElementById('end').value;

  const url = '/cave-link-proxy/';

  fetch(url, {
    method: 'GET',
  })
    .then(res => res.json())
    .then(json => {
      renderTable(json.data);
    })
    .catch(err => {
      console.error(err);
      alert('Error fetching data');
    });
});

function renderTable(data) {
  if (!data || data.length === 0) {
    document.getElementById('tableContainer').innerHTML = '<p>No data found.</p>';
    return;
  }

  let html = '<table border="1"><thead><tr>';

  // Generate table headers using keys of first object
  Object.keys(data[0]).forEach(col => {
    html += `<th>${col}</th>`;
  });

  html += '</tr></thead><tbody>';

  data.forEach(row => {
    html += '<tr>';
    Object.values(row).forEach(val => {
      html += `<td>${val}</td>`;
    });
    html += '</tr>';
  });

  html += '</tbody></table>';

  document.getElementById('tableContainer').innerHTML = html;
}