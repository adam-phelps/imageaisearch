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

function update_uploaded_image(img_location) {
    var doc = document.querySelector('#uploaded-image')
    if (doc.childElementCount== 0) {
        var img = new Image();
        img.src = img_location;
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
        display_img_analysis(result, "person")
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
    else {
        image_analysis = image_analysis.img_analysis_result.detect_labels_result
    }
    console.log(image_analysis)
    var table = document.createElement("table")
    var table_row = table.insertRow()
    var columns = []

    for (var i = 0; i < image_analysis.length; i++) {
        for (var k in image_analysis[i]) {
            if (columns.indexOf(k) === -1) {
                columns.push(k)
                console.log(`Adding this key: ${k}`)
            }
        }
    }

    for(var i = 0; i < columns.length; i++) {
        var table_header = document.createElement("th")
        table_header.innerHTML = columns[i]
        table_row.appendChild(table_header)
    }

    for(var x = 0; x < image_analysis.length; x++) {
        table_row = table.insertRow()
        for (var y = 0; y < columns.length; y++) {
            console.log(`Looking at analysis ${x} and key index ${y}`)
            console.log(`Adding this info: ${image_analysis[x][columns[y]]}`)
            var cell = table_row.insertCell()
            cell.innerHTML = image_analysis[x][columns[y]]
        }
    }
    document.querySelector('#image-analysis').appendChild(table)
}