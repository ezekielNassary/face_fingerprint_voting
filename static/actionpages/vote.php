<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
    require_once "config.php"; 
    $ccm = mysqli_real_escape_string($link, $_POST['ccm']);
    $cdm = mysqli_real_escape_string($link, $_POST['cdm']);
    $act = mysqli_real_escape_string($link, $_POST['act']);
    $fingerId = mysqli_real_escape_string($link, $_POST['fingerId']);
    $faceId = mysqli_real_escape_string($link, $_POST['faceId']);
$check=false;
$sql="CREATE TABLE IF NOT EXISTS `votes` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`CCM` varchar(50) NOT NULL,
`CHADEMA` varchar(50),
`ACT` varchar(50),
`fingerId` varchar(50),
`faceId` varchar(50) ,


CONSTRAINT UC_votes UNIQUE (id)
);";
if (mysqli_query($link, $sql)) {
//echo "table created";
} else {
//echo "Error: " . mysqli_error($link);
}

$sql="SELECT * FROM voters where fingerid='$fingerId'";
    $result = mysqli_query($link,$sql);
if($row = mysqli_fetch_array($result)) {
     $check=true;
    } 
if($check) {
  
$sql = "INSERT INTO votes (CCM,CHADEMA,ACT,Fingerid,Faceid)
VALUES ('".$ccm."','".$cdm."','".$act."','".$fingerId."','".$faceId."')";

if (mysqli_query($link, $sql)) {
	echo ("success");
	} 
	else {
	echo ("error: ".mysqli_error($link));
	}
    }else{
        echo "Voter not registered";
    }


?>