<?php
$q = $_REQUEST["q"];

$con = mysqli_connect('localhost','root','root','vlabs_database');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"vlabs_database");

if ($q!=0 and $q<13)
{
   $sql="SELECT * FROM labs WHERE institute_id='$q'";
} 
else if ($q>=13)
{
 $sql="SELECT * FROM labs WHERE='$q'";            


}
else
{

$sql="SELECT * FROM labs";
}   
$result = mysqli_query($con,$sql);
    $two = mysqli_num_rows($result);
    
echo "<br><br><h4>Total Number Of Labs:".$two."</h4>";
    echo "<br><br>";
    echo "<table border='2'>";

echo "<tr align='center'><td>LAB ID</td><td>LAB NAME</td><td>INTEGRATION LEVEL</td><td>STATUS</td></tr>";
while($row = mysqli_fetch_array($result)) {
 
  
  echo "<tr align='left'><td>".$row['lab_id']."</td><td>" . $row['lab_name'] ."</td><td>" . $row['integration_level'] ."</td><td>" . $row['status'] ."</td></tr>";

}

  echo "</table>";

mysqli_close($con);
?> 
