## Table of Contents

- [Installation](#installation)

## Installation

Ensure you have the following prerequisites installed:

1. **PHP**: You need to have PHP installed on your system. You can download and install PHP from [php.net](https://www.php.net/downloads.php).

2. **cURL extension (optional)**: If you want to use the script that uses cURL for HTTP requests, ensure that the cURL extension is enabled in your PHP configuration. Most PHP installations come with cURL enabled by default.

3. **PHPExcel library (optional)**: If you want to save data in Excel format using the `PHPExcel` library, you need to install it.
   - Download the PHPExcel library from [GitHub](https://github.com/PHPOffice/PHPExcel).
   - Extract the downloaded ZIP file to a directory accessible by your PHP scripts.
   - You can require the PHPExcel library in your script like this:
     ```php
     require_once 'path/to/PHPExcel/Classes/PHPExcel.php';
     ```
