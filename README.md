# Nova Language

Welcome to the official repository for the **Nova** programming language! Nova is a modern, general-purpose language designed for clarity, performance, and ease of use.

This repository contains the source code for:
*   The **Nova Compiler** (`/compiler`)
*   The **Visual Studio Code Extension** for syntax highlighting (`/vscode-extension`)

## Getting Started with Nova

This guide will walk you through installing the compiler and writing your first program.

### Step 1: Install Dependencies

Before you begin, ensure you have the following software installed and available in your system's PATH:

*   **Python 3.x**
*   **A C++ Compiler** (like `g++` from MinGW-w64 on Windows, or `clang++` on macOS/Linux)

### Step 2: Install the Nova Compiler

1.  Go to the **Releases** page.
2.  Download the latest `nova-compiler-windows.zip` file.
3.  Extract the ZIP file to a temporary location on your computer.
4.  Run the `install.bat` script. This will copy the compiler to a permanent location and set up your PATH.

> **Important**: After installation, you must **close and reopen** any open terminals (including the terminals in your IDE) for the `nova` command to be recognized.

### Step 3: Write and Run Your Code

1.  Create a new file named `hello.nova`.
2.  Add the following code:
    ```nova
    class HelloWorld {
        print("Hello from Nova!");
    }
    ```
3.  Open your terminal, navigate to the file's directory, and run:
    ```sh
    nova hello.nova
    ```

You should see the output `Hello from Nova!` in your terminal.

## Editor Support

### Visual Studio Code

An extension is available to provide rich syntax highlighting for `.nova` files.

For installation instructions, please see the VS Code Extension README.

## Contributing

Contributions are welcome! If you'd like to help improve the Nova language or its tools, please feel free to fork the repository, make your changes, and submit a pull request.

---

*Published by guentherKI.*