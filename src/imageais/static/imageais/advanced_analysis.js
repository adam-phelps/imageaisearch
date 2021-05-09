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
    request_img_analysis(event);
}

function update_uploaded_image(img_location) {
    var img = new Image();
    img.src = img_location;
    document.querySelector('#uploaded-image').appendChild(img);
    console.log(img);
}

function update_person_analysis(person_analysis) {
    if (person_analysis != undefined) {
        document.querySelector('#person-analysis-result').innerHTML = `Person analysis returned ${person_analysis}`
    }
}

function update_object_analysis(object_analysis) {
    if (object_analysis != undefined) {
        document.querySelector('#object-analysis-result').innerHTML = `OBJECT analysis returned ${object_analysis}`
    }
}

function upload_image(event) {

    const request = new Request(
        '/upload_image',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    var formData = new FormData()
    //formData.append("person_analysis", document.querySelector('#person-analysis-toggle').checked)
    //formData.append("object_analysis", document.querySelector('#object-analysis-toggle').checked)
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
        console.log(result.image_id)
    });
}

function request_img_analysis(event) {

    const request = new Request(
        '/request_img_analysis',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    var personAnalysis = document.querySelector('#person-analysis-toggle').checked
    var objectAnalysis = document.querySelector('#object-analysis-toggle').checked
    console.log(jsonRequest)

    var jsonRequest = {
        "person_analysis": personAnalysis,
        "object_analysis": objectAnalysis
    }

    fetch(request, {
        method: 'POST',
        body: JSON.stringify(jsonRequest)
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        update_person_analysis(result.person_analysis_response);
        update_object_analysis(result.object_analysis_response);
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