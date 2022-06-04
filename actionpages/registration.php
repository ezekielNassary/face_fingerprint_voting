<?php
    require_once "config.php"; 
  
    $name = mysqli_real_escape_string($link, $_POST['name']);
    $phone = mysqli_real_escape_string($link, $_POST['phone']);
    $pass = mysqli_real_escape_string($link, $_POST['pass']);
    $email = mysqli_real_escape_string($link, $_POST['email']);

$sql="SELECT * FROM admin_list where Email='$email'";
    $result = mysqli_query($link,$sql);
if($row = mysqli_fetch_array($result)) {
      echo ("registered");
    } 
else {
   $sql = "INSERT INTO `admin_list`( `Username`, `Password`, `Phone`, `Email`) 
	VALUES ('$name','$pass','$phone','$email')";

if (mysqli_query($link, $sql)) {
		echo ("success");
	} 
	else {
	echo ("error: ".mysql_error($link));
	}
    }


?>