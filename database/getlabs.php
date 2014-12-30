<?php
$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");
$sql="SELECT * FROM labs";

$result = mysqli_query($con,$sql);
$two = mysqli_num_rows($result);
echo "Total Number Of Labs:".$two;
echo "<br><br>";
echo "<table border='1'>";

echo "<tr><td>LAB ID</td><td>LAB NAME</td></tr>";
while($row = mysqli_fetch_array($result)) {
 
  
  echo "<tr align='left'><td>".$row['lab_id']."</td><td>" . $row['lab_name'] . "</td></tr>";

}

  echo "</table>";

mysqli_close($con);
?> 
