	<html>
	<head>
	<title>Retrieve data from database </title>
	</head>
	<body>
	
	<?php
	$lab_id = "";
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
   	$lab_id = test_input($_POST["lab_id"]);
   	}

	function test_input($data) {
   	$data = trim($data);
   	$data = stripslashes($data);
   	$data = htmlspecialchars($data);
  	return $data;
	}
	?>
	<form class="first" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
	Lab_id: <input type="text" class = "text-class"name="lab_id">
  	 <br><br>
	<input type="submit" name="submit" value="Submit">
	</form>
	<?php
	echo "<h2>Your Input:</h2>";
	echo $lab_id;
	?>
	<?php
	// Connect to database server
	mysql_connect("localhost", "root", "root") or die (mysql_error ());

	// Select database
	mysql_select_db("mydb") or die(mysql_error());

	// SQL query
	$strSQL = "SELECT * FROM people where lab_id ='$lab_id'";

	// Execute the query (the recordset $rs contains the result)
	$rs = mysql_query($strSQL);
	
	// Loop the recordset $rs
	// Each row will be made into an array ($row) using mysql_fetch_array
	while($row = mysql_fetch_array($rs)) {

	   // Write the value of the column FirstName (which is now in the array $row)
	  echo $row['FirstName'] . "<br />";

	  }

	// Close the database connection
	mysql_close();
	?>
	</body>
	</html>
