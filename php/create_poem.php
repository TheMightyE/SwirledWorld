<?php 
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$q = $_GET["q"];
if (empty($q)){
    echo "{'error':'Empty input'}";
    die();
}
$command = escapeshellcmd("python3 ../py/create_poem.py -q '$q'");
// $command = escapeshellcmd("python3 ../py/create_poem.py -q love");

$output = shell_exec($command);
echo $output;
