<?php
    require_once "config.php"; 
  
    $name = mysqli_real_escape_string($link, $_POST['name']);
    $gender = mysqli_real_escape_string($link, $_POST['gender']);
    $voteId = mysqli_real_escape_string($link, $_POST['voteId']);
    $phone = mysqli_real_escape_string($link, $_POST['phone']);
    $fingerId = mysqli_real_escape_string($link, $_POST['fingerId']);
    $faceId = mysqli_real_escape_string($link, $_POST['faceId']);

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