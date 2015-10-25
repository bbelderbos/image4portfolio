<?php
$dir = 'server/php/files';
$files = scandir($dir);
$images = array();
foreach($files as $fi){
  if(substr($fi, 0, 4 ) === "resi"){
    $fullPath = $dir . "/" . $fi;
    array_push($images, "<li><a href='download.php?file=$fullPath'>$fi</a></li>");
  }
}
?>
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Portfolio image preparation</title>
<link rel="stylesheet" href="css/reset.css" type="text/css">
<link rel="stylesheet" href="css/base.css" type="text/css">
</head>
<body>
<h1>Portfolio image preparation | Converted images</h1>
<?php
if(count($images) == 0){
  echo "<p>There are no images yet.</p>";
} else {
  echo "<ul>";
  foreach($images as $im){
    echo "$im\n";
  }
  echo "</ul>";
}
?>
</body> 
</html>
