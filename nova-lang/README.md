# Nova Language Support for VS Code


This extension provides rich language support for the [Nova programming language](https://github.com/guentherki/nova) in Visual Studio Code.

## About Nova

Nova is a modern, general-purpose programming language designed for clarity and performance. This extension enables developers to write Nova code with proper syntax highlighting and editor support.

## Features

This extension is in its early stages. Currently, it provides:

*   **Syntax Highlighting**: Semantic and syntactic highlighting for `.nova` files.
*   **Language Configuration**: Basic support for comments and bracket matching.
*   **File Icon**: A custom icon for Nova files in the explorer.

### Syntax Highlighting Example

Here is a small example of what Nova code looks like with this extension enabled:

```nova
class ArrayTest {
    print("--- Testing Arrays ---");

    let int[] numbers = [1, 2, 3, 4, 5];
    
    print("Element at index 2:");
    print(numbers[2]); 
    
    numbers[2] = 99;
    print("Element at index 2 after modification:");
    print(numbers[2]); 
    
    print("Looping through array:");
    let int i = 0;
    while (i < 5) {
        print(numbers[i]);
        i = i + 1;
    }
}
```


## Installation

### Marketplace (Coming Soon)

Once the extension is published, you will be able to install it from the Visual Studio Code Marketplace.

1.  Open **VS Code**.
2.  Go to the **Extensions** view (`Ctrl+Shift+X`).
3.  Search for `Nova Language`.
4.  Click **Install**.

### Manual Installation

You can also install the extension manually from a `.vsix` package.

1.  Download the latest release `.vsix` file from the releases page.
2.  Open **VS Code**.
3.  Go to the **Extensions** view (`Ctrl+Shift+X`).
4.  Click the `...` menu in the top-right corner and select **Install from VSIX...**.
5.  Choose the `.vsix` file you downloaded.

## Contributing

Contributions are welcome! If you'd like to help improve the Nova language support, please feel free to fork the repository, make your changes, and submit a pull request.

## Repository

The source code for this extension and the Nova language itself is hosted on GitHub. For more details on the Nova language, please see the main repository.

*   **Language & Compiler:** [(https://github.com/guentherki/nova)]

---

*Published by the guentherKI.
