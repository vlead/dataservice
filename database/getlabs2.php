<?php
$q = $_REQUEST["q"];
echo $q;
$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");
$sql ="SELECT id FROM disciplines WHERE discipline_name='$q'";
$result = mysqli_query($con,$sql);
$sql1="SELECT lab_id,lab_name FROM labs WHERE discipline_id='$result'";
$result1= mysqli_query($con,$sql1);
$two = mysqli_num_rows($result1);
    
echo "<br><br><h4>Total Number Of Labs:".$two."</h4>";
    echo "<br><br>";
    echo "<table border='2'>";

echo "<tr align='center'><td>LAB ID</td><td>LAB NAME</td></tr>";
while($row = mysqli_fetch_array($result1)) {
 
  
echo "<tr align='left'><td>".$row['lab_id']."</td><td>" . $row['lab_name'] . "</td></tr>";

}

  echo "</table>";

mysqli_close($con);
?> 
