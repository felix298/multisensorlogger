const url= "http://localhost:5555/"


const get_settings = obj => {
    if (obj === undefined) throw new Error("Failed to update settings")

    document.getElementById("participant").value = obj["participant_id"]
    _update_settings_button_text(obj["participant_id"], obj["group"])
    
    // get select option
    const select = document.querySelector('#group');
    const options = Array.from(select.options);
    const optionToSelect = options.find(item => item.text === obj["group"]);
    optionToSelect.selected = true;

    console.log(obj["study_path"])
    if (!(obj["study_path"] === undefined)) {
        document.getElementById("study_path").value = obj["study_path"]
    }
    if (!(obj["labrecorder_path"] === undefined)) {
        document.getElementById("labrecorder_path").value = obj["labrecorder_path"]
    }
    if (!(obj["tobii_manager_path"] === undefined)) {
        document.getElementById("tobii_manager_path").value = obj["tobii_manager_path"]
    }
}

const show_status_label = (message, success = false) => {
    red = getComputedStyle(document.documentElement).getPropertyValue('--error'); 
    green = getComputedStyle(document.documentElement).getPropertyValue('--success'); 
    label = document.getElementById("error-message")
    label.innerHTML = message
    if (label.innerHTML.startsWith("Error:")) {label.innerHTML = label.innerHTML.slice("Error:".length)}
    document.getElementById("status").style.display = "flex"
    document.getElementById("status").style.backgroundColor = success ? green : red

}

function close_error() {
    document.getElementById("status").style.display = "none"
}

let show = true
function toggle_settings() {
    if (show) {
        document.getElementById("settings").style.display = "flex"
    } else {
        document.getElementById("settings").style.display = "none"
    }
    show = !show
}

const _update_settings_button_text = (participant_id, group) => {
    document.getElementById("settings-button-text").textContent = `${group} ${participant_id}`
}

function set_settings(event) {
    event.preventDefault();
    _set_settings()
}

function _set_settings() {
    let participant_id = document.getElementById("participant").value
    let group = 'A'
    if (participant_id % 2 == 0) group = 'B'

    const select = document.querySelector('#group');
    const options = Array.from(select.options);
    const optionToSelect = options.find(item => item.text === group);
    optionToSelect.selected = true;

    fetch(url + "config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "participant_id": participant_id,
            "study_path": document.getElementById("study_path").value,
            "labrecorder_path": document.getElementById("labrecorder_path").value,
            "tobii_manager_path": document.getElementById("tobii_manager_path").value
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(errorText => {
                throw new Error(errorText);
            });
        }
        _update_settings_button_text(document.getElementById("participant").value, document.getElementById("group").value)
        show_status_label('<h1 style="margin-bottom: 0px">Saved successfully</h1>', true)
        toggle_settings()
    })
    .catch(error => show_status_label(error))
}

function init() {
    fetch(url + "config")
        .then(response => {
            if (!response.ok) {
                return response.text().then(errorText => {
                    throw new Error(errorText);
                });
            }
            return response.json()
        })
        .then(data => get_settings(data))
        .catch(error => show_status_label(error))
}

function call(route) {
    icon = document.getElementById(route)
    icon.src = "icons/loading.svg"
    icon.style.display = "block"
    fetch(url + route)
    .then(response => {
        if (!response.ok) {
            return response.text().then(errorText => {
                throw new Error(errorText);
            });
        }
        document.getElementById(route).src = "icons/okay.svg"
        return response.json()
    })
    .then(data => {
        try {
            if (data.includes("Polar")) {
                show_status_label(`<h1>Device found!</h1><p>${data}</p>`, true)
            }
        }
        catch {
            // do nothing
        }
    })
    .catch(error => {
        icon.style.display = "none"
            show_status_label(error)
        })
}

function reset() {
    participant_id = Number(document.getElementById("participant").value)
    document.getElementById("participant").value = participant_id + 1
    _set_settings()
}