<?php
$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");
$sql="SELECT * FROM institutes";

$result = mysqli_query($con,$sql);
$two = mysqli_num_rows($result);
echo "Total Number Of Institutes:".$two;
echo "<br><br>";
echo "<table border='1'>";

echo "<tr><td>INSTITUTE NAME</td></tr>";
while($row = mysqli_fetch_array($result)) {
 
  
  echo "<tr align='left'><td>". $row['institute_name'] . "</td></tr>";

}

  echo "</table>";

mysqli_close($con);
?> 
