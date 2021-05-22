export function display_img_analysis(image_analysis, image_analysis_type) {
    if (image_analysis_type == "person") {
        image_analysis = image_analysis.img_analysis_result.detect_faces_result
    }
    if (image_analysis_type == "object") {
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