let meals_by_vendors = JSON.parse(document.getElementById("meals_by_vendors").textContent)
let total_owning_by_vendors = JSON.parse(document.getElementById("total_owning_by_vendors").textContent)
let vendor_info = JSON.parse(document.getElementById("vendor_info").textContent)
let detail_order_info = JSON.parse(document.getElementById("detail_order_info").textContent)

function populateOrderSummary() {
    let orderVendorSummary = document.getElementById("orderVendorSummary")

    for (var vendor in meals_by_vendors) {
        first_time = true;
        for (var meal in meals_by_vendors[vendor]) {
            let row = document.createElement('tr')
    
            let vendor_cell = document.createElement('td')
            let meal_cell = document.createElement('td')
            let count = document.createElement('td')
            if (first_time) {
                first_time = false;
                vendor_cell.innerText = vendor;
            }

            meal_cell.innerText = meal;
            count.innerText = meals_by_vendors[vendor][meal];

            row.appendChild(vendor_cell);
            row.appendChild(meal_cell);
            row.appendChild(count);

            orderVendorSummary.appendChild(row)
        }
    }
}

function populateVendorInfo() {
    let vendorInfo = document.getElementById("vendorInfo")

    Array.from(vendor_info).forEach(element => {
        let row = document.createElement("tr")

        let vendor = document.createElement('td')
        let tel = document.createElement('td')
        let address = document.createElement('td')

        vendor.innerText = element['name']
        tel.innerText = element['tel']
        address.innerText = element['address']

        row.appendChild(vendor)
        row.appendChild(tel)
        row.appendChild(address)

        vendorInfo.appendChild(row)
    })
}

function populateVendorOwning() {
    let vendorOwning = document.getElementById("vendorOwning")
    let ownings_vendors = total_owning_by_vendors['price']

    for (var vendor in ownings_vendors) {
        let row = document.createElement("tr")

        let vendor_cell = document.createElement("td")
        let owning = document.createElement("td")

        vendor_cell.innerText = vendor
        owning.innerText = ownings_vendors[vendor]

        row.appendChild(vendor_cell)
        row.appendChild(owning)

        vendorOwning.appendChild(row)
    }
}

function populateDetailOrderInfo(detail_order_info) {
    let detailInfo = document.getElementById("detailOrderInfo")
    $("#detailOrderInfo").empty();

    Array.from(detail_order_info).forEach(element => {
        let row = document.createElement("tr")
        row.setAttribute("data-order_pk", element['pk'])

        let checkbox_cell = document.createElement('td')
        let checkbox = document.createElement('input')
        checkbox.setAttribute('type', 'checkbox')
        checkbox_cell.appendChild(checkbox)

        let vendor_cell = document.createElement("td")
        let meal_cell = document.createElement("td")
        let price_cell = document.createElement("td")
        let customer_cell = document.createElement("td")
        let ordered_cell = document.createElement("td")
        let notes_cell = document.createElement("td")
        let timestamp_cell = document.createElement("td")

        vendor_cell.innerText = element['vendor']
        meal_cell.innerText = element['meal']
        price_cell.innerText = element['price']
        customer_cell.innerText = element['customer']
        notes_cell.innerText = element['notes']
        timestamp_cell.innerText = formatTimestamp(element['timestamp'])

        if (element['ordered'] == 'True') {
            ordered_cell.setAttribute('bgcolor', '#5cb85c')
            ordered_cell.innerText = "True"
        } else {
            if (element["order_failed_reason"]) {
                ordered_cell.setAttribute('bgcolor', "#f0ad4e ")
                ordered_cell.innerText = element["order_failed_reason"]
            } else {
                ordered_cell.setAttribute('bgcolor', "#d9534f")
                ordered_cell.innerText = "False"
            }
        }

        row.appendChild(checkbox_cell)
        row.appendChild(vendor_cell)
        row.appendChild(meal_cell)
        row.appendChild(price_cell)
        row.appendChild(customer_cell)
        row.appendChild(ordered_cell)
        row.appendChild(notes_cell)
        row.appendChild(timestamp_cell)

        detailInfo.appendChild(row)
    })

}

function queryTodayOrders() {
    $("#activeOrder-select-all").prop('checked', false)
    location.reload(true);
}

function queryPastOrders() {
    let startDate = $("#startDate").val()
    let endDate = $("#endDate").val()
    if (startDate == "") {
        alert("Please enter start date to query")
    } else {        
        let send_data = JSON.stringify({'start_date': startDate,
        'end_date': endDate, 'action':'fetch_past_orders'});
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            data: send_data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function(result) {
                populateDetailOrderInfo(result['order_history']);
            },
            contentType:'application/json'
        });
    }
}

function downloadPastOrders() {
    let startDate = $("#startDate").val()
    let endDate = $("#endDate").val()
    if (startDate == "") {
        alert("Please enter start date to start download")
    } else {        
        if (endDate == "") {
            let ms = new Date(). getTime() + 86400000;
            endDate = parseDate(new Date(ms));
        }
        window.open(`/main/manager/export_csv/${startDate}/${endDate}/`)
    }
}

function parseDate(date) {
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    return `${year}-${month}-${day}`

}

function placeOrder() {
    let meals = $("#detailOrderInfo input[type='checkbox']:checked")
    let meals_pk = []
    for (var i=0; i<meals.length; i++) {
        meals_pk.push(meals[i].closest("tr").dataset.order_pk)
    }
    
    let send_data = JSON.stringify({'meals_pk':meals_pk, 'action':'place_meal_order'});
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(result) {
            queryTodayOrders()
        },
        contentType:'application/json'
    });
}

populateOrderSummary();
populateVendorInfo();
populateVendorOwning();
populateDetailOrderInfo(detail_order_info);