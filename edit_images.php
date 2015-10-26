<?php
$thumbWidth = $_POST['thumbWidth'];
$fullWidth = $_POST['fullWidth'];
$watermarkText = $_POST['watermarkText'];
if(!is_numeric($thumbWidth) || !is_numeric($fullWidth)){
  echo "<span class='err'>Both thumb and full widths need to be numeric values</span>";
  exit;
} elseif(!preg_match('/^\(C\)[a-z0-9 .\- ]+$/i', $watermarkText)) {
  echo "<span class='err'>Watermark text needs to be of format '(C) textual string'</span>";
  exit;
}
exec("./portfolio.py $thumbWidth $fullWidth '$watermarkText'", $output);
foreach($output as $o){
  if(strpos($o, "ERROR") !== false){
    echo "$o<br>\n";
  } else {
    $fullPath = $o;
    $fname = basename($o);
    echo "<li><a href='download.php?file=$fullPath'>$fname</a></li>\n";
  }
}
?>
