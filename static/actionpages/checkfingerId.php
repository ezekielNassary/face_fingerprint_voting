<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
require_once "config.php";
$fingerId = "";
if (isset($_POST['fingerId'])) {
    $fingerId = mysqli_real_escape_string($link, $_POST['fingerId']);
    $sql = "SELECT * FROM voters WHERE Fingerid='$fingerId' ";
    $result = mysqli_query($link, $sql);
    if (mysqli_num_rows($result) > 0) {
        while ($row = mysqli_fetch_array($result)) {
            $name = $row['Name'];
            $fingerid = $row['Fingerid'];
            echo $name;
        }
    } else {
        echo "Not found";
    }
} else {
    echo "id not sent";
}
