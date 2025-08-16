document.getElementById('fetchBtn').addEventListener('click', () => {
  const station = document.getElementById('station').value;
  const variable = document.getElementById('variable').value;
  const start = document.getElementById('start').value;
  const end   = document.getElementById('end').value;

  const params = new URLSearchParams({
      station: station,
      variable: variable,
    });

  const url = '/cave-link-proxy/data?';

  fetch(url + params, {
    method: 'GET',
  })
    .then(res => res.json())
    .then(json => {
      renderTable(json);
    })
    .catch(err => {
      console.error(err);
      alert('Error fetching data');
    });
});

function renderTable(json) {
  const data = json.data;
  if (!data || data.length === 0) {
    document.getElementById('tableContainer').innerHTML = '<p>No data found.</p>';
    return;
  }

  document.getElementById('tableMetadata').innerHTML = `<p>${json.metadata.join('</p><p>')}</p>`;

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