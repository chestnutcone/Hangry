let order_history = JSON.parse(document.getElementById("order_history").textContent)
let active_order = JSON.parse(document.getElementById("active_order").textContent)
let vendors = JSON.parse(document.getElementById("vendors").textContent)
let team = JSON.parse(document.getElementById("team").textContent)

function populateTeamName() {
    let team_header = document.getElementById('team_name')
    team_header.innerText = `Team ${team}`
}

function populateActiveOrders() {
    let orderTable = document.getElementById("activeOrderTable")

    Array.from(active_order).forEach(element => {
        let row = document.createElement('tr')
        row.setAttribute("data-order_pk", element['pk'])

        let checkbox_cell = document.createElement('td')
        let checkbox = document.createElement('input')
        checkbox.setAttribute('type', 'checkbox')
        checkbox_cell.appendChild(checkbox)

        let timestamp = document.createElement('td')
        let vendor = document.createElement('td')
        let meal = document.createElement('td')
        let price = document.createElement('td')

        timestamp.innerText = formatTimestamp(element['timestamp'])
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


function orderMeal() {
    let selected_meal_pk = $("#meal :selected").val();
    let notes = $("#additional-notes").val();
    let send_data = JSON.stringify({'meal_pk': selected_meal_pk,
    'notes':notes,
'action':'order_meal'});
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(ordered_meal) {
            console.log(ordered_meal);
            location.reload();
        },
        contentType:'application/json'
    });
}

function cancelOrder() {
    let orders = $("#activeOrderTable input[type='checkbox']:checked")
    let orders_pk = []
    for (var i=0; i<orders.length; i++) {
        orders_pk.push(orders[i].closest("tr").dataset.order_pk)
    }
    
    let send_data = JSON.stringify({'orders_pk':orders_pk, 'action':'cancel_order'});
    let csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(result) {
            location.reload()
        },
        contentType:'application/json'
    });

}

populateTeamName();
populateActiveOrders();
populateVendors();
