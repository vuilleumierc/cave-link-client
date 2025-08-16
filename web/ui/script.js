document.getElementById('fetchBtn').addEventListener('click', () => {
  const station = document.getElementById('station').value;
  const variable = document.getElementById('variable').value;
  const start = document.getElementById('start').value;
  const end   = document.getElementById('end').value;

  const params = new URLSearchParams({
      station: station,
      variable: variable,
      start: start,
      end: end
    });

  const url = '/cave-link-proxy?';

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
    document.getElementById('table-container').innerHTML = '<p>No data found.</p>';
    return;
  }

  document.getElementById('table-metadata').innerHTML = `<p>${json.metadata.join('</p><p>')}</p>`;

  // Get data keys (= column headers)
  const dataKeys = Object.keys(data);

  // Create a table element
  const table = document.createElement('table');
  table.border = '1';
  table.style.backgroundColor = '#ffdd99';
  table.style.borderColor = '#553311';

  // Create table header row
  const headerRow = document.createElement('tr');
  headerRow.style.backgroundColor = '#ff8800';
  dataKeys.forEach(key => {
    const th = document.createElement('th');
    th.textContent = key;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Create data rows
  const numRows = data[dataKeys[0]].length;
  for (let i = 0; i < numRows; i++) {
    const row = document.createElement('tr');
    row.style.backgroundColor = i % 2 === 0 ? '#8df59b' : '#9dd5ff';
    dataKeys.forEach(key => {
      const td = document.createElement('td');
      td.textContent = data[key][i];
      row.appendChild(td);
    });
    table.appendChild(row);
  }

  // Insert the table into the page
  const container = document.getElementById('table-container');
  container.innerHTML = '';
  container.appendChild(table);
}

const dateInput = document.getElementById("start");
dateInput.valueAsDate = new Date();