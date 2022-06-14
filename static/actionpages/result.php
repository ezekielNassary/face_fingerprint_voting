
   <?php

    $res = mysqli_real_escape_string($link, $_POST['status']);
    echo 'Ezekiel';
    require_once "config.php";
    $result2 = mysqli_query($link, "SELECT  SUM(CCM),SUM(CHADEMA), SUM(ACT) FROM votes");
    while ($row = mysqli_fetch_array($result2)) {
        $ccm = $row['SUM(CCM)'];
        $cdm = $row['SUM(CHADEMA)'];
        $act = $row['SUM(ACT)'];
    }

    echo ' <table id = "myTable" class = "table table-bordered" style = "width: 100%">
    <thead class="table-success">
      <tr>
      
                <th>CCM</th>
                <th>CHADEMA</th>
                <th>ACT</th>
                            </tr>
    </thead>
    <tbody>';
    echo "<tr>";
    echo "<td>" . $ccm . "</td>";
    echo '<td> ' . $cdm . ' </td>';
    echo "<td>" . $act . "</td>";
    echo "</tr>";
    echo '</tbody>';
    echo '</table>';




    ?>