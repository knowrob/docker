function moduleChange(val) {
    alert("The input value has changed.is: " + val.value);
}

function updateOptions(vals, obj) { 
  while(obj.options.length > 0) {
      obj.remove(0);
  }
  for (var i = 0; i < vals.length; i++)     {                
      opt = document.createElement("option");
      opt.value = vals[i];
      opt.text = vals[i];
      obj.appendChild(opt);
  }
  obj.value = opt.value;
}

function uploadFile() {
  alert("uploadFile: ");
  $.ajax({  
    type: "GET",
    url: $SCRIPT_ROOT + "/prac/updateUploadedFiles/",
    contentType: "application/json; charset=utf-8",
    data: {},
    success: function(data) {
          updateOptions(data.mlnlist, document.getElementById('mln_dd'));
          updateOptions(data.evidencelist, document.getElementById('evidence_dd'));
          updateMLN(document.getElementById('mln_dd'));
          updateEvidence(document.getElementById('evidence_dd'));
    }

  }); 
}

function updateModule(fld, infer) { 
  $.ajax({  
    type: "GET",
    url: $SCRIPT_ROOT + "/prac/updateModule/",
    contentType: "application/json; charset=utf-8",
    data: { moduleName: fld.value },
    success: function(data) {
        // alert("The input value has changed. The new value is: " + fld.value);
        if (infer) {
          updateOptions(data.kblist, document.getElementById('kb'));
          updateOptions(data.mlnlist, document.getElementById('mln_dd'));
          updateOptions(data.evidencelist, document.getElementById('evidence_dd'));
          updateKB(document.getElementById('kb'));
          updateEvidence(document.getElementById('evidence_dd'));
        } else {
          updateOptions(data.mlnlist, document.getElementById('mln_dd'));
          updateOptions(data.evidencelist, document.getElementById('evidence_dd'));
          updateMLN(document.getElementById('mln_dd'));        
          updateEvidence(document.getElementById('evidence_dd'));        
        }
    }

  });     
}

function updateMLN(fld) {
  // alert("The input value has changed.is: " + fld.value);
  $.ajax({  
    type: "GET",
    url: $SCRIPT_ROOT + "/prac/updateText/",
    contentType: "application/json; charset=utf-8",
    data: { fName: fld.value, module: document.getElementById('module').value, field: 'mln' },
    success: function(data) {
        // alert("The input value has changed. The new value is: " + fld.value);
        var mlnTextField = document.getElementById('mln');
        mlnTextField.value = data.text;
    }

  }); 
}


function updateEvidence(fld) {
  $.ajax({  
    type: "GET",
    url: $SCRIPT_ROOT + "/prac/updateText/",
    contentType: "application/json; charset=utf-8",
    data: { fName: fld.value, module: document.getElementById('module').value, field: 'db' },
    success: function(data) {
        // alert("The input value has changed. The new value is: " + fld.value);
        var evidenceTextField = document.getElementById('evidence');
        evidenceTextField.value = data.text;
    }

  }); 
}


function updateKB(fld) {
  $.ajax({  
    type: "GET",
    url: $SCRIPT_ROOT + "/prac/updateKB/",
    contentType: "application/json; charset=utf-8",
    data: { kb: fld.value , module: document.getElementById('module').value },
    success: function(data) {
        document.getElementById('queries').value = (data.queries ? data.queries : '');
        document.getElementById('method').value = data.method;
        document.getElementById('cwPreds').value = (data.cwPreds ? data.cwPreds : '');
        document.getElementById('closedWorld').checked = (data.closedWorld ? true : false);
        document.getElementById('useMultiCPU').checked = (data.useMultiCPU ? true : false);
        document.getElementById('mln').value = (data.mln ? data.mln : '');
        document.getElementById('logic').value = data.logic;
    }

  }); 
}

function updateDescr(fld) {
  // alert("The input value has changed.is: " + fld.value);
  var allElements = document.querySelectorAll("input, select, textarea");
  for (var i=0, max=allElements.length; i < max; i++) {
    if (allElements[i].id == 'description' | allElements[i].id == 'submit') continue;
    if (fld.value != '') {
      allElements[i].disabled = true;
    } else {
      allElements[i].disabled = false;
    }
  }
}

function updateTrainedMLN(res){
  alert("The input value has changed.is: " + res);  
  document.getElementById('trainedMLN').value = res.value;
}

function mlnFileName() {
  var fileName = prompt("Please enter a file name", "trained_mln");
  var res = document.getElementById('result').value;

  if (/[^a-z0-9\.\s\-\_]/gi.test(fileName)) {
    alert("File name not suitable");
  } else {
    $.ajax({  
      type: "POST",
      url: $SCRIPT_ROOT + "/prac/saveMLN/",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({ fName: fileName, content: document.getElementById('result').value }),
      success: function(data) {
          alert("The trained MLN has been saved to: " + data.path);  
      }
    }); 
  }
}
