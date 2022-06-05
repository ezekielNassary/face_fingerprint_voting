<?php
$db_user = "root";
$db_pass = "";
$db_server = "localhost";
$conn = mysqli_connect($db_server,$db_user,$db_pass);
if(!$conn){
	//echo  "connection error";
}
else{
//echo  "connection succesful ";
}
$sql = "CREATE DATABASE voting_system";
	 $result = mysqli_query($conn,$sql);
if($result){
	  // echo "Database created successfully";
	} else {
	   // echo "Error creating database: " . $conn->error;
	}
	mysqli_close($conn);
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "voting_system";
$link = new mysqli($servername, $username, $password, $dbname);

if (!$link) {
    die("Connection failed: " . mysqli_connect_error());
}


?>