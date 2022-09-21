<?php 

    include 'dbconf.php'

    $hr_id = $_POST['hr_id'];
    $content1 = "Added Successfully!";
    $content2 = "Employee ID Matched ! Couldn't add !"
    
    $sql = "SELECT* FROM HR;";
    $result = mysqli_query($conn,$sql);
    $resultCheck = mysqli_num_rows($result);

    $unmatch = true;

    if($resultCheck > 0){
        while($row = mysqli_fetch_assoc($result)){
            if($row['hr_id'] == $hr_id){
                $unmatch = false;
            }
        }
    }

    if($unmatch){
        $first_name = $_POST['first_name'];
        $last_name = $_POST['last_name'];
        $c_address = $_POST['c_address'];
        $hp_no = $_POST['hp_no'];
        $emergency_hp = $_POST['emergency_hp'];
        $gender = $_POST['gender'];
        $department = $_POST['department'];
        $birth = $_POST['birth'];
        $keyName = $hr_id.'-'rand(1,100)

        //s3 skip first 

        $sql = "INSERT INTO hr (hr_id,first_name,last_name,c_address,hp_no,emergency_hp,gender,department,birth)
                VALUES ('$hr_id','$first_name','$last_name','$c_address','$hp_no','$emergency_hp','$gender','$department','$birth');";
        $result = mysqli_query($conn,$sql)
    }

   /* $resultdup=mysqli_query($conn, $check_duplicate );
    $countdup=mysqli_num_rows($resultdup);
    if ($countdup>0){
        $error =true;
        $errorUsernameDup = 'Username already taken';
    }

*/


?>
