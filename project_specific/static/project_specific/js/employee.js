let order_history = JSON.parse(document.getElementById("order_history").textContent)
let active_order = JSON.parse(document.getElementById("active_order").textContent)
let vendors = JSON.parse(document.getElementById("vendors").textContent)

function populateActiveOrders() {
    let orderTable = document.getElementById("activeOrderTable")

    Array.from(active_order).forEach(element => {
        let row = document.createElement('tr')
        let checkbox_cell = document.createElement('td')
        let checkbox = document.createElement('input')
        checkbox.setAttribute('type', 'checkbox')
        checkbox_cell.appendChild(checkbox)

        let timestamp = document.createElement('td')
        let vendor = document.createElement('td')
        let meal = document.createElement('td')
        let price = document.createElement('td')

        timestamp.innerText = element['timestamp']
        vendor.innerText = element['vendor']
        meal.innerText = element['meal']
        price.innerText = element['price']

        row.appendChild(checkbox_cell)
        row.appendChild(timestamp)
        row.appendChild(vendor)
        row.appendChild(meal)
        row.appendChild(price)

        orderTable.appendChild(row)
    });
}

function populateVendors() {
    let vendor_option = document.getElementById("vendor")
    Array.from(vendors).forEach(element => {
        let option = document.createElement("option")
        option.innerText = element['name'];
        option.value = element['pk'];
        vendor_option.appendChild(option);
    });

    populateMeal();
}

function populateMeal() {
    // get the vender option
    // selected_vendor_pk
    let selected_vendor_pk = $("#vendor :selected").val()
    let send_data = JSON.stringify({'vendor_pk': selected_vendor_pk,
'action':'request_meal'});
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(meal_list) {
            $("#meal").empty();
            Array.from(meal_list).forEach(element => { 
                let meal_option = document.createElement("option");
                meal_option.innerText = element['name']+" $"+element['price'];
                meal_option.value = element['pk'];
                $("#meal").append(meal_option);
            });
        },
        contentType:'application/json'
    });
}

function searchTable(param, access_id) {

}

function taskActionButton() {

}

function saveChanges() {

}

function addTasks() {

}

populateActiveOrders();
populateVendors();
