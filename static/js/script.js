document.addEventListener('DOMContentLoaded', function() {
    const itemSelect = document.getElementById('item-select');
    const quantityInput = document.getElementById('quantity');
    const billForm = document.getElementById('bill-form');
    const billTableBody = document.querySelector('#bill-table tbody');
    const grandTotalElement = document.getElementById('grand-total');
    const printButton = document.getElementById('print-bill-btn');
    const addNewForm = document.getElementById('add-new-form');

    let billItems = [];

    async function fetchItems() {
        try {
            const response = await fetch('/items');
            if (!response.ok) throw new Error('Failed to fetch items');
            const items = await response.json();
            populateDropdown(items);
        } catch (error) {
            console.error('Error fetching items:', error);
            alert('Could not load items from the server.');
        }
    }

    function populateDropdown(items) {
        itemSelect.innerHTML = '';
        if (items.length === 0) {
            const option = document.createElement('option');
            option.textContent = 'No items available';
            itemSelect.appendChild(option);
            return;
        }
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = JSON.stringify(item);
            option.textContent = `${item.name} (₹${item.price.toFixed(2)})`;
            itemSelect.appendChild(option);
        });
    }

    function calculateTotal() {
        const total = billItems.reduce((sum, item) => sum + item.total, 0);
        grandTotalElement.textContent = `₹${total.toFixed(2)}`;
    }

    function renderBillTable() {
        billTableBody.innerHTML = '';
        billItems.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.name}</td>
                <td>₹${item.price.toFixed(2)}</td>
                <td>${item.quantity}</td>
                <td>₹${item.total.toFixed(2)}</td>
            `;
            billTableBody.appendChild(row);
        });
    }

    billForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        if (!itemSelect.value) {
            alert('Please select an item.');
            return;
        }

        const selectedItem = JSON.parse(itemSelect.value);
        const quantity = parseInt(quantityInput.value);
        
        if (isNaN(quantity) || quantity <= 0) {
            alert('Please enter a valid quantity.');
            return;
        }
        
        const existingItem = billItems.find(item => item.id === selectedItem.id);
        
        if (existingItem) {
            existingItem.quantity += quantity;
            existingItem.total = existingItem.quantity * existingItem.price;
        } else {
            billItems.push({
                ...selectedItem,
                quantity: quantity,
                total: selectedItem.price * quantity
            });
        }
        
        renderBillTable();
        calculateTotal();
        quantityInput.value = 1;
    });

    addNewForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const itemName = document.getElementById('new-item-name').value;
        const itemPrice = parseFloat(document.getElementById('new-item-price').value);

        if (!itemName || isNaN(itemPrice) || itemPrice <= 0) {
            alert('Please enter a valid item name and price.');
            return;
        }

        try {
            const response = await fetch('/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: itemName, price: itemPrice })
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                addNewForm.reset();
                fetchItems();
            } else {
                alert(result.error || 'Failed to add item.');
            }
        } catch (error) {
            console.error('Error adding new item:', error);
            alert('An error occurred while adding the item.');
        }
    });

    printButton.addEventListener('click', async function() {
        if (billItems.length === 0) {
            alert('Please add items to the bill first.');
            return;
        }

        try {
            const response = await fetch('/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(billItems)
            });

            if (response.ok) {
                const pdfBlob = await response.blob();
                const url = URL.createObjectURL(pdfBlob);
                
                const a = document.createElement('a');
                a.href = url;
                a.download = 'bill.pdf';
                document.body.appendChild(a);
                a.click();
                
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } else {
                alert('Failed to generate PDF. Please try again.');
            }
        } catch (error) {
            console.error('Error generating PDF:', error);
            alert('An error occurred while generating the PDF.');
        }
    });

    fetchItems();
});