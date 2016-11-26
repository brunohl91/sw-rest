#!/usr/bin/php
<?php

$props = array (
  "cod" => "9767",
  "titulo" => "Mudança de Rota",
  "data" => "2016-06-17",
  "hora" => "16:50:42",
  "status" => "98",
  "descricao" => "UNIJUÍ FIDENE"
);

$title = "Novo Ticket";
$msg = "Há um novo ticket no sistema, titulo: {titulo}";

echo replaceVars($title, $props);
echo replaceVars($msg, $props);

function replaceVars ( $subject, $vars ) {
  foreach ($vars as $key => $var) {
    $key = "{" . $key . "}";
    $subject = str_ireplace($key, $var, $subject);
  }
  return $subject;
}