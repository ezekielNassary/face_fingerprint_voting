<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
    require_once "config.php"; 
  
    $name = mysqli_real_escape_string($link, $_POST['name']);
    $gender = mysqli_real_escape_string($link, $_POST['gender']);
    $voteId = mysqli_real_escape_string($link, $_POST['voteId']);
    $phone = mysqli_real_escape_string($link, $_POST['phone']);
    $fingerId = mysqli_real_escape_string($link, $_POST['fingerId']);
    $faceId = mysqli_real_escape_string($link, $_POST['faceId']);

$sql="CREATE TABLE IF NOT EXISTS `voters` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`Name` varchar(50) NOT NULL,
`Gender` varchar(50),
`vote_Id` varchar(50),
`Phone` varchar(50) ,
`Fingerid` varchar(50),
`Faceid` varchar(50),

CONSTRAINT UC_voters UNIQUE (id)
);";
if (mysqli_query($link, $sql)) {
//echo "table created";
} else {
//echo "Error: " . mysqli_error($link);
}

$sql="SELECT * FROM voters where fingerid='$fingerId'";
    $result = mysqli_query($link,$sql);
if($row = mysqli_fetch_array($result)) {
      echo ("registered");
    } 
else {
  
$sql = "INSERT INTO voters (Name,Gender,Vote_Id, Phone,Fingerid,Faceid)
VALUES ('".$name."','".$gender."','".$voteId."','".$phone."','".$fingerId."','".$faceId."')";

if (mysqli_query($link, $sql)) {
	echo ("success");
	} 
	else {
	echo ("error: ".mysqli_error($link));
	}
    }


?>