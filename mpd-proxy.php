<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/dash+xml');

// Get fresh MPD URL from output.php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://mpdchecker.webiptv.site/output.php?url=https%3A%2F%2Fwebiptv.site%2Fskynz.php%3Fid%3D219026");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Referer: https://webiptv.site/",
    "User-Agent: Mozilla/5.0",
    "Origin: https://webiptv.site"
]);

$mpdUrl = curl_exec($ch);
curl_close($ch);

// Fetch the actual MPD
$mpdContent = file_get_contents(trim($mpdUrl));
echo $mpdContent;
?>
