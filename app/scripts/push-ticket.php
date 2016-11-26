#!/usr/bin/php
<?php

/**
 * Para esse script devem ser instalados e habilitados JSON e cURL
 * JSON:
 *   zypper in php5-json
 * cURL:
 *   zypper in php5-curl
 * Reiniciar apache
 *   rcapache2 restart
 */

date_default_timezone_set('America/Sao_Paulo');

msg("Começando envio com Pushbullet");

if (isset ($argv) && is_array($argv) && count($argv) > 3) {

  // $key = "o.16maZ4R1qNVi2k23vbEy7vZubAbkqQMf";
  $key = $argv[1];
  $request = array (
    "type" => "note",
    "title" => $argv[2],
    "body" => $argv[3],
    "url" => ""
  );
  $ch = curl_init("https://api.pushbullet.com/v2/pushes");
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
  curl_setopt($ch, CURLOPT_HEADER, FALSE);
  curl_setopt($ch, CURLOPT_POST, TRUE);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
  curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($request) );
  curl_setopt($ch, CURLOPT_HTTPHEADER, array( "Content-Type: application/json", "Authorization: Bearer {$key}", "Accept: application/json" ));
  $output = curl_exec($ch);
  curl_close($ch);

  msg($output);
  msg("Finalizando envio com Pushbullet");

}

function msg( $msg ) {
  error_log( date('d/m/y H:i:s') . " " . $msg . PHP_EOL , 3, '/tmp/push.log');
}

exit();