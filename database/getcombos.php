<?php
$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");
$sql="SELECT * FROM institutes";
$sql1="SELECT * FROM disciplines";
$result1 = mysqli_query($con,$sql1);
$result = mysqli_query($con,$sql);

echo "Select Institute Name :";

echo "<select>";
while($row = mysqli_fetch_array($result)) {
 
  
  echo "<option>" . $row['institute_name'] . "</option>";

}

  echo "</select>";echo "<br><br>";	
echo "Select Discipline Name : ";
echo "<select>";
while($row = mysqli_fetch_array($result1)) {
 
  
  echo "<option>" . $row['discipline_name'] . "</option>";

}
  echo "</select>";

mysqli_close($con);
?> 
