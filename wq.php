<?php
    $dbServername="localhost";
    $dbusername="admin";
    $dbPassword = "main-password";
    $dbname = "hr";

    $conn = mysqli_connect($dbServername,$dbusername,$dbPassword,$dbname);

    $sql = "Show Tables Like 'hr'";
    $result = mysqli_query($conn,$sql);
    $resultCheck = mysqli_num_rows($result);
    if($resultCheck == 0){
        $sql = " CREATE TABLE hr(
        hr_ID INT(4) NOT NULL,
        first_name VARCHAR(200) NOT NULL, 
        last_name VARCHAR(200) NOT NULL,
        c_address VARCHAR(200) NOT NULL,
        hp_no VARCHAR(200) NOT NULL, 
        emergency_hp VARCHAR(200) NOT NULL,
        gender VARCHAR(200) NOT NULL,
        department VARCHAR(200) NOT NULL,
        birth DATE NOT NULL,
        PRIMARY KEY (hr_id)
        );";
        $result = mysqli_query($conn,$sql);
    }
    $sql="SELECT * FROM hr;"
    $result = mysqli_query($conn,$sql);
?>