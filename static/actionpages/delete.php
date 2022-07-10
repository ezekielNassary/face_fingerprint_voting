<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
require_once "config.php"; 
// sql to delete a record
$sql = "DELETE FROM voters";

if (mysqli_query($link, $sql)) {
    echo "Deleted";
} else {
    echo "Error deleting record: " . mysqli_error($link);
}

mysqli_close($link);

?>