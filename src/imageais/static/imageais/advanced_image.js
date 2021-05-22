document.addEventListener('DOMContentLoaded', function() {
    get_img_analysis();
});

// For Django CSRF requests to not fail we must send the token with every request
// This is then made a global variable for all methods to use
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function get_img_analysis(event) {
    const img_id = window.location.href.split("/")[3];
    const request = new Request(
        '/get_img_analysis',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    var personAnalysis = true;
    var objectAnalysis = true;

    var jsonRequest = {
        "person_analysis": personAnalysis,
        "object_analysis": objectAnalysis,
        "img_id": img_id
    }

    fetch(request, {
        method: 'POST',
        body: JSON.stringify(jsonRequest)
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (personAnalysis == true) {
            display_img_analysis(result, "person")
        }
        if (objectAnalysis == true) {
            display_img_analysis(result, "object")
        }
    });
}

function display_img_analysis(image_analysis, image_analysis_type) {
    if (image_analysis_type == "person") {
        image_analysis = image_analysis.img_analysis_result.detect_faces_result
    }
    if (image_analysis_type == "object") {
        image_analysis = image_analysis.img_analysis_result.detect_labels_result
    }
    var table = document.createElement("table")
    table.setAttribute('id','results-table');
    var table_row = table.insertRow()
    var excluded_column_names = ['id', 'additional_info', 'faces_detected_count','image']
    var excluded_column_locations = []
    var column_keys = []
    console.log(`Image analysis length ${image_analysis.length}`)

    for (var k in image_analysis[0]) {
        {
            var table_header = document.createElement("th");
            table_header.setAttribute("class","table-th-td");
            column_keys.push(k);
            table_header.innerHTML = (k.charAt(0).toUpperCase() + k.slice(1)).replace('_', ' ');
            table_row.appendChild(table_header);
        }
    }

    for(var analysis = 0; analysis < image_analysis.length; analysis++) {
        table_row = table.insertRow()
        table_row.setAttribute("class","table-th-td");
        for (var v = 0; v < column_keys.length; v++) {
            //console.log(`Looking at analysis ${x} and key index ${y}`)
            //console.log(`Adding this info: ${image_analysis[x][columns[y]]}`)
            var cell = table_row.insertCell();
            if (column_keys[v].includes("confidence")) {
                result = image_analysis[analysis][column_keys[v]];
                cell.innerHTML = result.toString().slice(0,5);
            } else if (column_keys[v].includes("timestamp")) {
                result = image_analysis[analysis][column_keys[v]];
                cell.innerHTML = result.toString().slice(0,16);
            } else {
            cell.innerHTML = image_analysis[analysis][column_keys[v]];
            }
            if (v % 2 == 0) {
                cell.setAttribute("style", "font-weight: bold; background-color: rgb(200,200,200)");
            }
        }
    }
    document.querySelector('#image-analysis').appendChild(table)
}