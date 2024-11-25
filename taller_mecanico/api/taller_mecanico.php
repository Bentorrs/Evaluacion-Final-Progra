<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, PUT, DELETE");

$host = "localhost";
$user = "root";
$pass = "";
$db = "taller_mecanico";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["error" => "Conexion fallida"]);
    exit();
}

// POST: http://localhost/api/taller_mecanico.php?action=register
// Registrar un usuario
// Campos: nombre_usuario, clave, es_admin
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_GET['action'] === 'register') {
    $data = json_decode(file_get_contents("php://input"), true);
    $nombre_usuario = $data['nombre_usuario'];
    $clave = $data['clave'];
    $es_admin = $data['es_admin'] ?? 0;

    $stmt = $conn->prepare("INSERT INTO usuario (nombre_usuario, clave, es_admin) VALUES (?, ?, ?)");
    $stmt->bind_param("ssi", $nombre_usuario, $clave, $es_admin);

    if ($stmt->execute()) {
        echo json_encode(["message" => "Usuario registrado exitosamente"]);
    } else {
        http_response_code(400);
        echo json_encode(["error" => "El usuario ya existe"]);
    }
    $stmt->close();
}

// POST: http://localhost/api/taller_mecanico.php?action=login
// Inciar sesion
// Campos: nombre_usuario, clave
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_GET['action'] === 'login') {
    $data = json_decode(file_get_contents("php://input"), true);
    $nombre_usuario = $data['nombre_usuario'];
    $clave = $data['clave'];

    $stmt = $conn->prepare("SELECT clave, es_admin FROM usuario WHERE nombre_usuario = ?");
    $stmt->bind_param("s", $nombre_usuario);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($stored_clave, $es_admin);
        $stmt->fetch();

        if ($clave === $stored_clave) {
            echo json_encode([
                "message" => "Login exitoso",
                "nombre_usuario" => $nombre_usuario,
                "es_admin" => $es_admin
            ]);
        } else {
            http_response_code(401);
            echo json_encode(["error" => "Clave incorrecta"]);
        }
    } else {
        http_response_code(404);
        echo json_encode(["error" => "Usuario no encontrado"]);
    }
    $stmt->close();
}

// PUT: http://localhost/api/taller_mecanico.php?action=change
// Cambiar clave
// Campos: nombre_usuario, nueva_clave
if ($_SERVER['REQUEST_METHOD'] === 'PUT' && $_GET['action'] === 'change') {
    $data = json_decode(file_get_contents("php://input"), true);
    $nombre_usuario = $data['nombre_usuario'];
    $nueva_clave = $data['nueva_clave'];

    $stmt = $conn->prepare("UPDATE usuario SET clave = ? WHERE nombre_usuario = ?");
    $stmt->bind_param("ss", $nueva_clave, $nombre_usuario);

    if ($stmt->execute() && $stmt->affected_rows > 0) {
        echo json_encode(["message" => "Clave cambiada exitosamente"]);
    } else {
        http_response_code(400);
        echo json_encode(["error" => "No se pudo cambiar la clave"]);
    }
    $stmt->close();
}

// GET: http://localhost/api/taller_mecanico.php?action=get&nombre_usuario=admin
// Obtener un usuario
// campos: nombre_usuario
if ($_SERVER['REQUEST_METHOD'] === 'GET' && $_GET['action'] === 'get') {
    $nombre_usuario = $_GET['nombre_usuario'];

    $stmt = $conn->prepare("SELECT es_admin FROM usuario WHERE nombre_usuario = ?");
    $stmt->bind_param("s", $nombre_usuario);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($es_admin);
        $stmt->fetch();
        echo json_encode([
            "nombre_usuario" => $nombre_usuario,
            "es_admin" => $es_admin
        ]);
    } else {
        http_response_code(404);
        echo json_encode(["error" => "Usuario no encontrado"]);
    }
    $stmt->close();
}

$conn->close();
?>