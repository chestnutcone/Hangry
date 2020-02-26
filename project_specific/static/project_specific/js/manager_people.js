let unregistered_user = JSON.parse(document.getElementById("unregistered_users").textContent)
let team_users = JSON.parse(document.getElementById("team_users").textContent)

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

    for (var i=0; i<team_users.length; i++) {
        let cur_employee = team_users[i]
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
            if (result['status'] == 'success') {
                location.reload();
            }
        },
        contentType:'application/json'
    });    

}


populateUserTable();
populateTeamUserTable();