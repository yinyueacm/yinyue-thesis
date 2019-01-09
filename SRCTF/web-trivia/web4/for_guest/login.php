<?php
include "config.php";
$con = mysqli_connect("localhost", "sqlctf", "sqlctfwillamete", "sqlctf");
$username = mysqli_real_escape_string($con, $_POST["username"]);
$password = mysqli_real_escape_string($con, $_POST["password"]);
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($con, $query);

if (mysqli_num_rows($result) !== 1) {
    echo "<h1>Login failed.</h1>";
    echo "<a href='index.php'>back</a>";
} else {
    echo "<h1>Logged in!</h1>";
    if(!isset($_COOKIE["the_cookie"])){
        echo "<p>How about some cookies</p>";
    } else {
        $c_value = $_COOKIE["the_cookie"];
        if($c_value == "flag_on"){
            echo "<p>Your flag is: $FLAG</p>";
        } else {
            echo "<p>How about some cookies</p>";
        }
    }
    echo "<a href='index.php'>back</a>";
}
?>
