# Nova Language Guide

This document provides a basic overview of the syntax for the Nova programming language.

## 1. Basic Structure

Every Nova program must be contained within a `class`. The class acts as the main container for your code. The code written directly inside the class (not inside a function) will be executed when the program starts.

```nova
class MyProgram {
    # This is the entry point of the program
    print("Hello, World!");
}
```

## 2. Comments

Single-line comments start with a `#` symbol.

```nova
# This is a comment. The compiler will ignore this line.
let int x = 10; # This is an inline comment.
```

## 3. Variables and Data Types

Variables are declared using the `let` keyword.

```nova
let <type> <name> = <value>;
```

### Primitive Types

*   `int`: For whole numbers (e.g., `10`, `-5`).
*   `float`: For floating-point numbers (e.g., `3.14`).
*   `string`: For text (e.g., `"Hello"`).

**Example:**
```nova
let int age = 25;
let float price = 19.99;
let string name = "Nova";
```

### Arrays

Arrays are declared by adding `[]` to a type. Array literals are created with square brackets.

```nova
let int[] numbers = [1, 2, 3, 4, 5];
let string[] words = ["one", "two", "three"];

# Accessing elements
print(numbers[0]); # Prints 1

# Assigning to an element
numbers[0] = 99;
```

## 4. Structs (User-Defined Types)

You can define your own complex data types using `struct`.

```nova
struct Point {
    x: int;
    y: int;
}

# Create a new instance of a struct
let Point p = new Point(10, 20);

# Access fields using the dot (.) operator
print(p.x); # Prints 10
p.y = 30;
```

## 5. Functions

Functions are defined using the `def` keyword.

```nova
def <name>(<parameter_list>) -> <return_type> {
    # function body
    return <value>;
}
```

*   Parameters are defined as `<name>: <type>`.
*   The return type (`-> <return_type>`) is optional. If omitted, the function returns `void`.

**Example:**
```nova
def add(a: int, b: int) -> int {
    return a + b;
}

def sayHello(name: string) {
    print("Hello, " + name);
}

# Calling functions
let int result = add(5, 3);
sayHello("World");
```

## 6. Control Flow

### If-Else Statements
```nova
if (x > 10) {
    print("x is greater than 10");
} else {
    print("x is not greater than 10");
}
```

### While Loops
```nova
let int i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```

## 7. Built-in Functions

*   `print(<expression>);`: Prints a value to the console.
*   `int(input("prompt"));`: Displays a prompt, reads an integer from the user, and returns it.