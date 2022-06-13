<!doctype html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Voting System</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
    <script>
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }
    </script>
</head>

<body class="bg-light text-dark">
    <div class="container ">
        <div class="row ">
            <div class="col-md-3"></div>
            <div class="col-md-6 shadow-sm p-3 mb-5 bg-white rounded">
                <h3 class="text-center p-3">ELECTRONIC VOTING</h3>

                <div class="mb-3 mt-3 p-3 bg-success">
                    <div class="row">
                        <div class="col-md-12 ">
                            <div class="card">
                                <div class="card-body">
                                    <button type="button" class="btn btn-success w-100" id="train">RESULT PAGE</button>
                                </div>
                            </div>
                            <div class="card p-2">

                                <?php
                                require_once "actionpages/config.php";
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


                            </div>


                        </div>
                        <div class="col-md-3"></div>
                    </div>
                </div>


                <script>
                    var socket = new WebSocket('ws:localhost:5555/ws');
                    var server_status = document.getElementById('serverStatus');
                    var finger_status = document.getElementById('finger-print-status');
                    //var sendId = document.getElementById('sendId');
                    var finger_Id = "";
                    socket.onopen = function() {
                        console.log('Connected to server');
                        $('#serverStatus').html('Server Connected');
                    };
                    socket.onmessage = function(event) {
                        var data = JSON.parse(event.data);
                        var res = data.command;
                        var msg = data.msg;
                        finger_Id = data.id;
                        //res = res.replace(/\s/g, '');

                        //$('#fingerid').html(finger_Id);
                        $('#placeFinger').html(res);
                        $('#face_status').html(msg);

                    }

                    // sendId.addEventListener('click', function () {
                    // $('#sendId').prop('disabled', true);
                    // socket.send("e");
                    // $('#placeFinger').html("wait..");
                    //});

                    $('#start-fingerprint').click(function(e) {
                        socket.send("e");
                    });

                    $('#train-modal').click(function(e) {
                        socket.send("m");
                    });
                    $('#start-face').click(function(e) {
                        var name = $("#name").val();
                        if (name === "") {
                            alert('Provide Voters Name');
                            return;
                        } else {
                            socket.send("t");
                            socket.send(name);

                        }

                    });
                    $('#submit-btn').click(function(e) {
                        e.preventDefault();
                        var name = $("#name").val();
                        var genders = document.getElementsByName('gender');
                        var phone = $("#phone").val();
                        var voteId = $("#voteId").val();
                        var gender = '';
                        var fingerId = finger_Id
                        var faceId = "";
                        for (var i = 0, length = genders.length; i < length; i++) {
                            if (genders[i].checked) {
                                gender = genders[i].value;
                                break;
                            }
                        }
                        if (name === "") {
                            alert('Provide Voters Name');
                            return;
                        }
                        $.ajax({
                            type: "POST",
                            url: "http://192.168.36.191/face_fingerprint_voting/static/actionpages/registration.php",
                            data: {
                                name: name,
                                gender: gender,
                                voteId: voteId,
                                phone: phone,
                                fingerId: fingerId,
                                faceId: faceId
                            },
                            cache: false,
                            success: function(data) {
                                alert(data);
                                if (data == "success") {
                                    $('#register-form').trigger("reset");
                                } else {
                                    $("#error").show();
                                    $('#error').html('Error Occured');
                                }
                            },
                            error: function(xhr, status, error) {
                                // alert(error);
                            }
                        });
                    });

                    socket.onclose = function() {
                        console.log('Network Disconneted');
                        $('#serverStatus').html('Server Disconneted');
                    };
                </script>
</body>

</html>