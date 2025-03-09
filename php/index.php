<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = file_get_contents('php://input');
    $data = json_decode($data);

    if ($data === null || !isset($data->code)) {
        http_response_code(400);
        echo json_encode(["error" => "Invalid request"]);
        die();
    }

    $tmpFile = tempnam(sys_get_temp_dir(), 'php_exec_') . '.php';
    file_put_contents($tmpFile, "<?php\n" . $data->code . "\n?>");

    // Execute the PHP code and capture the output
    $output = shell_exec("php $tmpFile 2>&1");

    // Delete the temporary file
    unlink($tmpFile);

    // Return the output
    echo json_encode(["output" => $output]);
}
?>
