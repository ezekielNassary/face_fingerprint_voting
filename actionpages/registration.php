<?php
    require_once "config.php"; 
  
    $name = mysqli_real_escape_string($link, $_POST['name']);
    $gender = mysqli_real_escape_string($link, $_POST['gender']);
    $voteId = mysqli_real_escape_string($link, $_POST['voteId']);
    $phone = mysqli_real_escape_string($link, $_POST['phone']);
    $fingerId = mysqli_real_escape_string($link, $_POST['fingerId']);
    $faceId = mysqli_real_escape_string($link, $_POST['faceId']);

$sql="CREATE TABLE IF NOT EXISTS `voters` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(50) NOT NULL,
`gender` varchar(50),
`voteid` varchar(50),
`phone` varchar(50) ,
`fingerid` varchar(50),
`faceid` varchar(50),

CONSTRAINT UC_voters UNIQUE (id)
);";
if (mysqli_query($con, $sql)) {
echo "table created";
} else {
echo "Error: " . mysqli_error($con);
}

$sql="SELECT * FROM voters where fingerid='$fingerId'";
    $result = mysqli_query($link,$sql);
if($row = mysqli_fetch_array($result)) {
      echo ("registered");
    } 
else {
   $sql = "INSERT INTO `voters`( `name`, `gender`, `voteid`, `phone`,'fingerid','faceid') 
	VALUES ('$name','$gender','$voteId','$phone','$fingerId','$faceId')";

if (mysqli_query($link, $sql)) {
		echo ("success");
	} 
	else {
	echo ("error: ".mysql_error($link));
	}
    }


?>