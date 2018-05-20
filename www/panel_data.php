<?php
    require_once 'include/main.php';

    $temperature = file_get_contents($run_dir.'/mon-out/temp');
    if ($temperature === false) {
        $temperature = "ERROR";
    } else {
	$temperature = (string)round($temperature, 1);
        $temperature .= " &deg;C";
    }

    echo '<h3>TEMPERATURE: '.$temperature.'</h3>';
?>
