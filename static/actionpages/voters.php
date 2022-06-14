<?php
 header("Access-Control-Allow-Origin: *");
 header("Access-Control-Allow-Headers: *");
require_once "config.php";
echo ' <table id = "myTable" class = "table table-bordered" style = "width: 100%">
    <thead class="table-success">
      <tr>
        <th>S/N</th>
        <th>Name</th>
                <th>Gender</th>
                <th>Phone</th>
                <th>Vote ID</th>
                <th>Action</th> 
             </tr>
    </thead>
    <tbody>';

$sql = "SELECT * FROM voters";
$result = mysqli_query($link, $sql);
$count = 0;
while ($row = mysqli_fetch_array($result)) {
    $name = $row['Name'];
    $gender = $row['Gender'];
    $phone = $row['Phone'];
    $voteid = $row['vote_Id'];
    $fingerid = $row['Fingerid'];
    $faceid = $row['Faceid'];

    $count++;
    echo "<tr>";
    echo "<td>" . $count . "</td>";
    echo "<td>" . $name . "</td>";
    echo '<td> ' . $gender . ' </td>';
    echo "<td>" . $phone . "</td>";
    echo "<td>" . $voteid . "</td>";
    // echo "<td>" . $fingerid . "</td>";
    // echo "<td>" . $faceid . "</td>";
    echo  " <td><button type='button' class='btn btn-warning w-100' id='train'>DELETE</button></td>";
    echo "</tr>";
}
echo '</tbody>';
echo '</table>';
