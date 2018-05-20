<?php
    require_once 'include/main.php';

    if (!isset($_GET['key']) || !isset($_GET['value'])) { exit(); }

    switch ($_GET['key']) {
        case 'camera':
	    if ($_GET['value'] == 1) { touch($run_dir.'/mon-ctl/camera'); } else { unlink($run_dir.'/mon-ctl/camera'); }
	    break;
        case 'led-bri':
	    if ($_GET['value'] == 1) { touch($run_dir.'/mon-ctl/led-bri'); } else { unlink($run_dir.'/mon-ctl/led-bri'); }
	    break;
        case 'led-ir':
	    if ($_GET['value'] == 1) { touch($run_dir.'/mon-ctl/led-ir'); } else { unlink($run_dir.'/mon-ctl/led-ir'); }
	    break;
    }
?>
