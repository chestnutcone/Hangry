let unregistered_user = JSON.parse(document.getElementById("unregistered_users").textContent)
let team_users = JSON.parse(document.getElementById("team_users").textContent)
let recent_trans = JSON.parse(document.getElementById("recent_transactions").textContent)

function populateUserTable() {
    let userTable = document.getElementById("unregisteredUserTable")

    for (var i=0; i<unregistered_user.length; i++) {
        let cur_unreg_user = unregistered_user[i]
        let row = document.createElement("tr")
        row.setAttribute("data-user_pk", cur_unreg_user['pk'])

        let checkbox_cell = document.createElement('td')
        let checkbox = document.createElement('input')
        checkbox.setAttribute('type', 'checkbox')
        checkbox_cell.appendChild(checkbox)

        let name_cell = document.createElement("td")
        let email_cell = document.createElement("td")

        name_cell.innerText = cur_unreg_user['name']
        email_cell.innerText = cur_unreg_user['email']

        row.appendChild(checkbox_cell)
        row.appendChild(name_cell)
        row.appendChild(email_cell)

        userTable.appendChild(row)
    }
}

function populateTeamUserTable() {
    let teamTable = document.getElementById("teamUserTable")
    let team_select = document.getElementById("team_member")

    for (var i=0; i<team_users.length; i++) {
        let cur_employee = team_users[i]

        // create options for team member
        let option = document.createElement('option')
        option.innerText = `${cur_employee['name']} \$${cur_employee['balance']}`
        option.value = cur_employee['pk']
        team_select.appendChild(option)

        // make table 
        let row = document.createElement("tr")
        row.setAttribute("data-user_pk", cur_employee['pk'])

        let checkbox_cell = document.createElement('td')
        let checkbox = document.createElement('input')
        checkbox.setAttribute('type', 'checkbox')
        checkbox_cell.appendChild(checkbox)

        let name_cell = document.createElement("td")
        let balance_cell = document.createElement("td")
        let email_cell = document.createElement("td")

        name_cell.innerText = cur_employee['name']
        balance_cell.innerText = cur_employee['balance']
        email_cell.innerText = cur_employee['email']

        row.appendChild(checkbox_cell)
        row.appendChild(name_cell)
        row.appendChild(balance_cell)
        row.appendChild(email_cell)

        teamTable.appendChild(row)
    }
}

function removeUserFromTeam() {
    let removeMemebers = $("#teamUserTable input[type='checkbox']:checked")
    let member_pk = []
    for (var i=0; i<removeMemebers.length; i++) {
        member_pk.push(removeMemebers[i].closest("tr").dataset.user_pk)
    }

    let send_data = JSON.stringify({'user_pk':member_pk, 'action':'remove_user_from_team'});
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(result) {
            if (result['status'] == 'success') {
                location.reload();
            }
        },
        contentType:'application/json'
    });    
}

function addUserToTeam() {
    let addMemebers = $("#unregisteredUserTable input[type='checkbox']:checked")
    let user_pk = []
    for (var i=0; i<addMemebers.length; i++) {
        user_pk.push(addMemebers[i].closest("tr").dataset.user_pk)
    }

    let send_data = JSON.stringify({'user_pk':user_pk, 'action':'add_user_to_team'});
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        data: send_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        success: function(result) {
            if (result['status']) {
                location.reload();
            } else {
                let joined_error = result['error'].join('/n')
                alert(joined_error)
            }
        },
        contentType:'application/json'
    });    
}

function depositMoney() {
    let member_pk = $("#team_member :selected").val();
    let deposit = $("#deposit_money").val();
    
    if (deposit < 0 || deposit == "" || member_pk == null) {
        alert('Cannot deposit negative or empty or invalid amount or empty team member')
    } else {
        let send_data = JSON.stringify({'user_pk':member_pk,
        'amount': deposit, 'action':'deposit_money'});
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            data: send_data,
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function(result) {
                if (result['status']) {
                    location.reload(true);
                } else {
                    alert(result['error'])
                }
            },
            contentType:'application/json'
        });    
    }
}

function populateRecentActions() {
    let recentAction = document.getElementById('recentActions')

    Array.from(recent_trans).forEach(element => {
        let row = document.createElement("tr")

        let timestamp = document.createElement('td')
        let name = document.createElement('td')
        let amount = document.createElement('td')

        timestamp.innerText = formatTimestamp(element['timestamp'])
        name.innerText = element['name']
        amount.innerText = element['transaction_amount']

        row.appendChild(timestamp)
        row.appendChild(name)
        row.appendChild(amount)

        recentAction.appendChild(row)
    })
}


populateUserTable();
populateTeamUserTable();
populateRecentActions();