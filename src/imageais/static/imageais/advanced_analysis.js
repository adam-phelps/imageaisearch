document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-analysis-submit').addEventListener('click', submit_new_analysis);
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

function submit_new_analysis(event) {
    upload_image(event);
}

function hide_upload_form() {
    var upload_form_form = document.getElementById('upload-form-form')
    var upload_form_div = document.getElementById('new-analysis-submit')
    //upload_form_form.style.visibility = "hidden"
    upload_form_form.parentNode.removeChild(upload_form_form)
    upload_form_div.parentNode.removeChild(upload_form_div)
}

function update_uploaded_image(img_location) {
    var doc = document.querySelector('#uploaded-image')
    if (doc.childElementCount== 0) {
        var img = new Image();
        img.src = img_location;
        img.style = "max-height:300px; max-width:300px"
        document.querySelector('#uploaded-image').appendChild(img);
        console.log(img);
    }
}

function update_image_analysis(person_analysis) {
    if (person_analysis != undefined) {
        document.querySelector('#image-analysis').innerHTML = `Person analysis returned ${person_analysis}`
    }
}

function upload_image(event) {

    const request = new Request(
        '/upload_image',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    var formData = new FormData()
    console.log(document.querySelector('#id_file').files[0])
    formData.append("file", document.querySelector('#id_file').files[0])
    console.log(formData)

    fetch(request, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        display_image(event, result.image_id)
        request_img_analysis(event, result.image_id);
        console.log(result.image_id)
        hide_upload_form();
    });
}

function request_img_analysis(event, img_id) {

    const request = new Request(
        '/request_img_analysis',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    var personAnalysis = document.querySelector('#person-analysis-toggle').checked
    var objectAnalysis = document.querySelector('#object-analysis-toggle').checked
    console.log(jsonRequest)

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
        //update_image_analysis(result)
        if (personAnalysis == true) {
            display_img_analysis(result, "person")
        }
        if (objectAnalysis == true) {
            display_img_analysis(result, "object")
        }
    });
}

function display_image(event, img_id) {

    const request = new Request(
        `/get_image/${img_id}`, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
        }
    );

    fetch(request)
    .then(response => response.json())
    .then(result => {
        console.log("The image location I recevied is...")
        update_uploaded_image(result.img_location)
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