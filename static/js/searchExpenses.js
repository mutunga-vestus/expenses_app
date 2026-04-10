const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const pagination = document.querySelector('.pagination-container');

tableOutput.style.display = 'none';

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value.trim();
    if (searchValue.length === 0) {
        tableOutput.style.display = 'none';
        appTable.style.display = 'block';
        pagination.style.display = 'block';
        return;
    }
    pagination.style.display = 'none';

    fetch('/search-expenses', {
        body: JSON.stringify({ searchText: searchValue }),
        method: 'POST',
    })
    .then(res => res.json())
    .then(data => {
        appTable.style.display = 'none';
        tableOutput.style.display = 'block';

        if (data.length === 0) {
            tableOutput.innerHTML = '<p class="text-center mt-3">No results found</p>';
            return;
        }

        let html = '';

        data.forEach(item => {
            html += `
                <tr>
                    <td>${item.amount}</td>
                    <td>${item.category}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td>
                    <td>
                        <a href="/edit-expense/${item.id}" class="btn btn-secondary btn-sm">
                            Edit
                        </a>
                    </td>
                </tr>
            `;
        });

        document.querySelector('.table-body').innerHTML = html;
    });
});