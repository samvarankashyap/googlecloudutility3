<html>
<head>
<!-- Latest compiled JavaScript -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script>
$( document ).ready(function() {
    console.log( "ready!" );
               $( "#show" ).click(function() {
  			console.log( "button click called." );
                        
                        var postObj = {};
                        postObj["magnitude"] = $( "#magnitude" ).val();
                        postObj["parameter1"] = $( "#parameter1" ).val();
                        postObj["location"] = $( "#location" ).val();
                        postObj["parameter2"] = $( "#parameter2" ).val();
                        console.log(postObj);
                        if ( between(parseInt(postObj["magnitude"]),1,15) ){ 
               			$.post("/querybuilder",postObj,
    				function(data, status){
        				//alert("Data: " + data + "\nStatus: " + status);
                                	//$("#content").text(data);
                                        addContent(data);
               			});
                       }
                       else {
                              $("#content").text("Invalid magnitude rage<br>");
                       }

		});
    function between(x, min, max) {
        return x >= min && x <= max;
    }
    function addContent(resp){
      var resp = JSON.parse(resp);
      html_string = "<table><th></th>";
      for (var x in resp) {
      	html_string += "<tr>";
      	for (var y in resp[x] ){
      		html_string +="<td>"+resp[x][y]+"</td>";
      	}
      	html_string += "</tr>";
      }
      html_string += "</table>";
      console.log(html_string);
      $("#content").html(html_string);
    }
});

</script>

</head>
<body>
<h1>
Welcome to the web interface of the earthquakes and maginitudes 
<h1>
<h2>Enter input:</h2>
Magnitude:<input type="text" id='magnitude'> <br>
Parameter1: <select id="parameter1">
  <option value="gt">Greater than</option>
  <option value="lt">Less than</option>
  <option value="eq"> Equal to</option>
  <option value="lte">Less than Equal to</option>
  <option value="gte">Greater than equal to </option>
</select> <br>
Parameter2 : <select id="parameter2">
  <option value="and">AND</option>
  <option value="or">OR</option>
</select> <br>
Location: <input type="text" id="location"><br>
<input type="button" id ="show" value = "Show">
<div id="content">
</div>
</body>
<html>
