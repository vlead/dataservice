<?php
$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");
$sql="SELECT * FROM disciplines";

$result = mysqli_query($con,$sql);
$two = mysqli_num_rows($result);
echo "Total Number Of Disciplines:".$two;
echo "<br><br>";
echo "<table border='1'>";

echo "<tr><td>DISCIPLINE NAME</td></tr>";
while($row = mysqli_fetch_array($result)) {
 
  
  echo "<tr align='left'><td>". $row['discipline_name'] . "</td></tr>";

}

  echo "</table>";

mysqli_close($con);
?> 
