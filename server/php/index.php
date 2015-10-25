<?php
/*
 * jQuery File Upload Plugin PHP Example
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */
$options = array(
    // This option will disable creating thumbnail images and will not create that extra folder.
    // However, due to this, the images preview will not be displayed after upload
    'image_versions' => array()
);  

error_reporting(E_ALL | E_STRICT);
require('UploadHandler.php');
#$upload_handler = new UploadHandler();
$upload_handler = new UploadHandler($options);
