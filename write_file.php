<?php
$path =  $_SERVER['DOCUMENT_ROOT'] . 'molecularListLogic/uploads/' . $_POST['file_name'];
$output = fopen($path, 'w') or die("Unable to open file!");
fwrite($output,$_POST["results"]);

$path =  $_SERVER['DOCUMENT_ROOT'] . 'molecularListLogic/LOGFILE.txt';
$output = fopen($path, 'a') or die("Unable to open logfile!");
fwrite($output,$_POST['date'] . " Boolean operation: " . $_POST['operator']. "\n");
?>