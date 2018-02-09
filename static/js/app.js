//populate select element with datasets
namesUrl = "/names";
Plotly.d3.json(namesUrl, function (error, response) {
    if (error) console.log(error);
    namesList = response;
    console.log(namesList);
    $datasetSelectList = document.getElementById("datasetSelect");
    for (var i = 0; i < namesList.length; i++) {
        var $option = document.createElement("option");
        $option.value = namesList[i];
        $option.text = namesList[i];
        $datasetSelectList.appendChild($option);
    }
    optionChanged(namesList[0]);
});

function optionChanged(datasetToPlot) {
    var samplesUrl = `/samples/${datasetToPlot}`;
    var wfreqUrl = `/wfreq/${datasetToPlot}`;
    var otuUrl = `/otu/${datasetToPlot}`;
    var metadataUrl = `/metadata/${datasetToPlot}`

    //set up empty metadata dictionary
    var metadataDict = {
        "SAMPLEID": "",
        "ETHNICITY": "",
        "GENDER": "",
        "AGE": 0,
        "BBTYPE": "",
        "LOCATION": ""
    };
    Plotly.d3.json(metadataUrl, function (error, response) {
        metadataDict.SAMPLEID = response.SAMPLEID;
        metadataDict.ETHNICITY = response.ETHNICITY;
        metadataDict.GENDER = response.GENDER;
        metadataDict.AGE = response.AGE;
        metadataDict.BBTYPE = response.BBTYPE;
        metadataDict.LOCATION = response.LOCATION;
    });
    console.log(metadataDict);
    addMetadata(metadataDict);

    //initialize wfreq
    var wfreq = 0;


    //addMetadata(metadataUrl);
    //renderPieChart(samplesURL,otuUrl);
    //renderGauge(wfreqUrl);
    //renderBubbleChart(samplesUrl,otuUrl);
}

function addMetadata(metadataDict) {
    $metadata_card = document.getElementById("metadata_card");
    $metadata_card.innerHTML = `<p>Age: ${metadataDict.AGE}<br> </p>`;
}

/*function renderPieChart(samplesUrl,otuUrl){

}

function renderGauge(wfreqUrl){

}

function renderBubbleChart(samplesUrl,otuUrl){

}*/