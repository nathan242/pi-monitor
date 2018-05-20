<?php
    require_once 'include/main.php';

    $camera = (file_exists($run_dir.'/mon-ctl/camera')) ? true : false;
    $led_bri = (file_exists($run_dir.'/mon-ctl/led-bri')) ? true : false;
    $led_ir = (file_exists($run_dir.'/mon-ctl/led-ir')) ? true : false;

    echo '<h3>CAMERA <input type="checkbox" id="camera" onchange="control(this);"'.(($camera) ? ' checked' : '').'></h3>';
    echo '<h3>LIGHT <input type="checkbox" id="led-bri" onchange="control(this);"'.(($led_bri) ? ' checked' : '').'></h3>';
    echo '<h3>IR LIGHT <input type="checkbox" id="led-ir" onchange="control(this);"'.(($led_ir) ? ' checked' : '').'></h3>';
?>
