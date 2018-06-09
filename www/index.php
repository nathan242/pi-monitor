<?php
    require_once 'include/main.php';
?>
<!doctype html>
  <head>
    <title>PI-MONITOR</title>
    <link rel="stylesheet" href="include/css/style.css" />
  </head>
  <body>
    <div class="container">
      <div class="left_column">
        <div class="video_panel">
          <video src="hls/index.m3u8" width="<?php echo $video_x; ?>" height="<?php echo $video_y; ?>" controls="controls" autoplay>VIDEO</video>
        </div>
      </div>
      <div class="right_column">
        <div class="data_panel" id="data_panel">
          DATA
        </div>
        <div class="control_panel" id="control_panel">
          CONTROL
        </div>
      </div>
    </div>

  <script>
    function load_data() {
        var xhr = new XMLHttpRequest();
	xhr.open("GET", "panel_data.php", true);
	xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                document.getElementById('data_panel').innerHTML = xhr.responseText;
            }
	};
	xhr.send();
    }

    function load_controls() {
        var xhr = new XMLHttpRequest();
	xhr.open("GET", "panel_controls.php", true);
	xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                document.getElementById('control_panel').innerHTML = xhr.responseText;
            }
	};
	xhr.send();
    }

    function control(setting) {
	if ('checked' in setting) {
            var value = setting.checked ? 1 : 0;
	} else {
            var value = setting.value;
	}
        var xhr = new XMLHttpRequest();
	xhr.open("GET", "control.php?key="+setting.id+"&value="+value);
	xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                load_controls();
            }
	};
	xhr.send();
    }

    load_data();
    load_controls();

    setInterval(load_data, <?php echo $data_refresh_interval*1000 ?>);
  </script>

  </body>
</html>

