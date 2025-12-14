import re
import sys
import os

# --- Lexer ---
TOKENS = [
    ('CLASS', r'\bclass\b'),
    ('STRUCT', r'\bstruct\b'),
    ('DEF', r'\bdef\b'),
    ('RETURN', r'\breturn\b'),
    ('LET', r'\blet\b'),
    ('NEW', r'\bnew\b'),
    ('OR', r'\bor\b'),
    ('INT_TYPE', r'\bint\b'),
    ('FLOAT_TYPE', r'\bfloat\b'),
    ('STRING_TYPE', r'\bstring\b'),
    ('PRINT', r'\bprint\b'),
    ('INPUT', r'\binput\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),
    ('EQ', r'=='),
    ('NEQ', r'!='),
    ('LTE', r'<='),
    ('GTE', r'>='),
    ('LT', r'<'),
    ('GT', r'>'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('FLOAT', r'\d+\.\d+'),
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMI', r';'),
    ('COLON', r':'),
    ('DOT', r'\.'),
    ('ARROW', r'->'),
    ('COMMA', r','),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('STAR', r'\*'),
    ('SLASH', r'/'),
    ('COMMENT', r'#.*'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.'),
]

def lex(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_name, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_name != 'WHITESPACE' and token_name != 'COMMENT':
                    tokens.append((token_name, text))
                pos = match.end()
                break
        if not match:
            print(f"Illegal character at {pos}: {code[pos]}")
            pos += 1
    return tokens

# --- Parser & Transpiler State ---

class Node:
    pass

class ClassNode(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class StructNode(Node):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields # List of (type, name)

class FunctionNode(Node):
    def __init__(self, name, args, ret_type, body):
        self.name = name
        self.args = args
        self.ret_type = ret_type
        self.body = body

class VarDeclNode(Node):
    def __init__(self, type_name, name, value_expr):
        self.type_name = type_name
        self.name = name
        self.value_expr = value_expr

class ReturnNode(Node):
    def __init__(self, expr):
        self.expr = expr

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr

class IfNode(Node):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class AssignmentNode(Node):
    def __init__(self, name, index_expr, expr):
        self.name = name # For structs, this might be "p.x"
        self.index_expr = index_expr 
        self.expr = expr

class ExpressionNode(Node):
    def __init__(self, text):
        self.text = text

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.defined_types = {'int', 'float', 'string'} 

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, expected_type=None):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if expected_type is None:
                self.pos += 1
                return token
            # strict check if expected_type provided?
            # actually our usage pattern is: consume('TYPE') throws if not match.
            if token[0] != expected_type:
                 raise Exception(f"Expected {expected_type} but got {token[0]} '{token[1]}'")
            self.pos += 1
            return token
        raise Exception("Unexpected end of input")
        
    def parse(self):
        return self.parse_class()

    def parse_class(self):
        self.consume('CLASS')
        name = self.consume('ID')[1]
        self.consume('LBRACE')
        body = []
        while self.peek() and self.peek()[0] != 'RBRACE':
            body.append(self.parse_statement())
        self.consume('RBRACE')
        return ClassNode(name, body)

    def parse_statement(self):
        token = self.peek()
        if token[0] == 'DEF':
            return self.parse_function()
        elif token[0] == 'STRUCT':
            return self.parse_struct_def()
        elif token[0] == 'LET':
            return self.parse_var_decl()
        elif token[0] == 'RETURN':
            return self.parse_return()
        elif token[0] == 'PRINT':
            return self.parse_print()
        elif token[0] == 'IF':
            return self.parse_if()
        elif token[0] == 'WHILE':
            return self.parse_while()
        elif token[0] == 'ID':
            # Assignment check: ID = ... or ID.field = ... or ID[idx] = ...
            if self.is_assignment_start():
                return self.parse_assignment()
                
            expr = self.parse_expression()
            self.consume('SEMI')
            return ExpressionNode(expr) 
        elif token[0] in ['INT_TYPE', 'FLOAT_TYPE', 'STRING_TYPE']:
             expr = self.parse_expression()
             self.consume('SEMI')
             return ExpressionNode(expr)
        else:
             raise Exception(f"Unexpected statement start: {token}")

    def is_assignment_start(self):
        # Heuristic to check if current ID is start of assignment
        # Look ahead for = before ;
        # ID . ID = ...
        # ID [ expr ] = ...
        # ID = ...
        scan_pos = 1
        bracket_balance = 0
        while self.peek(scan_pos):
            t = self.peek(scan_pos)
            if t[0] == 'SEMI': return False
            if t[0] == 'LBRACE': return False # block start
            
            if t[0] == 'LBRACKET': bracket_balance += 1
            elif t[0] == 'RBRACKET': bracket_balance -= 1
            
            if bracket_balance == 0 and t[0] == 'ASSIGN':
                return True
            scan_pos += 1
        return False

    def parse_struct_def(self):
        self.consume('STRUCT')
        name = self.consume('ID')[1]
        self.consume('LBRACE')
        fields = []
        while self.peek() and self.peek()[0] != 'RBRACE':
            field_name = self.consume('ID')[1]
            self.consume('COLON')
            field_type = self.parse_type()
            self.consume('SEMI')
            fields.append((field_type, field_name))
        
        self.consume('RBRACE')
        self.defined_types.add(name)
        return StructNode(name, fields)
    
    def parse_single_type(self):
        t = self.consume()
        if t[0] not in ['INT_TYPE', 'FLOAT_TYPE', 'STRING_TYPE', 'ID']:
             raise Exception(f"Expected type but got {t}")
        base_type = t[1]
        
        if self.peek() and self.peek()[0] == 'LBRACKET':
            self.consume('LBRACKET')
            self.consume('RBRACKET')
            return base_type + "[]"
        return base_type

    def parse_type(self):
        # A type can be a single type or a union of types (e.g., "int or string")
        types = [self.parse_single_type()]
        
        while self.peek() and self.peek()[0] == 'OR':
            self.consume('OR')
            types.append(self.parse_single_type())
            
        if len(types) > 1:
            # We use '|' as an internal separator for our union type representation.
            # This is hidden from the user, who only sees 'or'.
            return "|".join(types)
        else:
            # It's just a single type
            return types[0]

    def parse_function(self):
        self.consume('DEF')
        name = self.consume('ID')[1]
        self.consume('LPAREN')
        args = []
        if self.peek()[0] != 'RPAREN':
            while True:
                arg_name = self.consume('ID')[1]
                self.consume('COLON')
                arg_type = self.parse_type()
                args.append((arg_type, arg_name))
                if self.peek()[0] == 'COMMA':
                    self.consume('COMMA')
                else: # Stop if no comma
                    break
        self.consume('RPAREN')
        
        # Check return type presence (ARROW)
        ret_type = "void" # Default?
        if self.peek() and self.peek()[0] == 'ARROW':
            self.consume('ARROW')
            ret_type = self.parse_type()
        
        self.consume('LBRACE')
        body = []
        while self.peek()[0] != 'RBRACE':
            body.append(self.parse_statement())
        self.consume('RBRACE')
        return FunctionNode(name, args, ret_type, body)

    def parse_var_decl(self):
        self.consume('LET')
        type_name = self.parse_type()
        name = self.consume('ID')[1]
        
        expr = None # Default to no initializer
        if self.peek() and self.peek()[0] == 'ASSIGN':
            self.consume('ASSIGN')
            expr = self.parse_expression()

        self.consume('SEMI')
        return VarDeclNode(type_name, name, expr)

    def parse_return(self):
        self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return ReturnNode(expr)

    def parse_print(self):
        self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMI')
        return PrintNode(expr)

    def parse_if(self):
        self.consume('IF')
        self.consume('LPAREN')
        condition = self.parse_expression()
        self.consume('RPAREN')
        self.consume('LBRACE')
        if_body = []
        while self.peek()[0] != 'RBRACE':
            if_body.append(self.parse_statement())
        self.consume('RBRACE')
        
        else_body = None
        if self.peek() and self.peek()[0] == 'ELSE':
            self.consume('ELSE')
            self.consume('LBRACE')
            else_body = []
            while self.peek()[0] != 'RBRACE':
                else_body.append(self.parse_statement())
            self.consume('RBRACE')
            
        return IfNode(condition, if_body, else_body)

    def parse_while(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        condition = self.parse_expression()
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = []
        while self.peek()[0] != 'RBRACE':
            body.append(self.parse_statement())
        self.consume('RBRACE')
        return WhileNode(condition, body)

    def parse_assignment(self):
        # This handles `x = ...`, `x.y = ...`, `x[i] = ...`
        # Simple parser: Consume ID, then optionally DOT ID or LBRACKET ... RBRACKET
        # This is strictly LHS parsing.
        
        lhs_parts = []
        first_id = self.consume('ID')[1]
        lhs_string = first_id
        
        while True:
            if self.peek() and self.peek()[0] == 'DOT':
                self.consume('DOT')
                nid = self.consume('ID')[1]
                lhs_string += "." + nid
            elif self.peek() and self.peek()[0] == 'LBRACKET':
                self.consume('LBRACKET')
                # Index expr
                idx_expr = self.parse_expression()
                self.consume('RBRACKET')
                lhs_string += "[" + idx_expr + "]"
            else:
                break
                
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return AssignmentNode(lhs_string, None, expr) 

    def parse_expression(self):
        expr_out = []
        balance = 0
        bracket_balance = 0
        last_was_id = False
        bracket_stack = []

        while True:
            t = self.peek()
            if not t: break
            if t[0] == 'SEMI': break
            if t[0] == 'LBRACE': break 
            if t[0] == 'RPAREN' and balance == 0: break
            if t[0] == 'RBRACKET' and bracket_balance == 0: break
            if t[0] == 'COMMA' and balance == 0 and bracket_balance == 0: break # argument list separator!

            if t[0] == 'NEW':
                # new StructName(args)
                self.consume('NEW')
                struct_name = self.consume('ID')[1]
                self.consume('LPAREN')
                
                # Parse args list
                args = []
                while self.peek()[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.peek()[0] == 'COMMA':
                        self.consume('COMMA')
                    else:
                        break
                self.consume('RPAREN')
                
                # Construct C++ constructor call
                # StructName { arg1, arg2 }
                args_joined = ", ".join(args)
                expr_out.append(f"{struct_name} {{ {args_joined} }}")
                last_was_id = False # result is value
                continue

            tok = self.consume()
            txt = tok[1]
            type_ = tok[0]
            to_append = txt

            if type_ == 'FLOAT':
                to_append = txt + 'f'
            
            if type_ == 'LPAREN':
                balance += 1
            elif type_ == 'RPAREN':
                balance -= 1
            elif type_ == 'LBRACKET':
                bracket_balance += 1
                if last_was_id or (expr_out and (expr_out[-1].endswith(']') or expr_out[-1].endswith(')'))): 
                    bracket_stack.append('index')
                else:
                    bracket_stack.append('literal')
                    to_append = "{"
            elif type_ == 'RBRACKET':
                bracket_balance -= 1
                if bracket_stack:
                    kind = bracket_stack.pop()
                    if kind == 'literal':
                        to_append = "}"
                    else:
                        to_append = "]"
            
            # DOT handling for field access
            if type_ == 'DOT':
                # C++ uses . for objects
                pass
                
            expr_out.append(to_append)
            
            if type_ == 'ID':
                last_was_id = True
            elif type_ in ['RBRACKET', 'RPAREN']:
                 last_was_id = False 
            elif type_ != 'WHITESPACE': 
                last_was_id = False
                
        return " ".join(expr_out)

# --- Generator ---

def map_type(t):
    # Handle union types (our internal representation uses '|')
    if "|" in t:
        types = t.split('|')
        mapped_types = [map_type(sub_type) for sub_type in types]
        return f"std::variant<{', '.join(mapped_types)}>"

    if t == "string": return "std::string"
    if t.endswith("[]"):
        base = t[:-2]
        return f"std::vector<{map_type(base)}>"
    return t # Assumed ID is a valid C++ struct name

def generate_cpp(node):
    if isinstance(node, ClassNode):
        structs = []
        functions = []
        main_stmts = []
        for item in node.body:
            if isinstance(item, StructNode):
                structs.append(item)
            elif isinstance(item, FunctionNode):
                functions.append(item)
            else:
                main_stmts.append(item)
        
        output = []
        output.append("#include <iostream>")
        output.append("#include <string>")
        output.append("#include <vector>")
        output.append("#include <variant>")
        output.append("using namespace std;")
        output.append("")
        output.append("// Built-in helpers")
        output.append("int _input_int(string prompt) {")
        output.append("    cout << prompt;")
        output.append("    int x;")
        output.append("    if (!(cin >> x)) { cin.clear(); cin.ignore(10000, '\\n'); return 0; }")
        output.append("    return x;")
        output.append("}")
        output.append("string _input_str(string prompt) {")
        output.append("    cout << prompt;")
        output.append("    string s;")
        output.append("    getline(cin, s);")
        output.append("    return s;")
        output.append("}")
        output.append("template<class... Ts> void _print_variant(const std::variant<Ts...>& v) {")
        output.append("    std::visit([](const auto& val) { std::cout << val; }, v);")
        output.append("    std::cout << std::endl;")
        output.append("}")
        output.append("template<typename T> void _print_simple(const T& val) {")
        output.append("    std::cout << val << std::endl;")
        output.append("}")
        output.append("")
        output.append(f"namespace {node.name} {{")
        
        # Structs first
        for s in structs:
             output.append(f"    struct {s.name} {{")
             for f_type, f_name in s.fields:
                 output.append(f"        {map_type(f_type)} {f_name};")
             output.append("    };")
             output.append("")

        for func in functions:
            output.append(generate_cpp(func))
        
        output.append("    void _main() {")
        for stmt in main_stmts:
            output.append("        " + generate_cpp(stmt))
        output.append("    }")
        output.append("}")
        output.append("")
        output.append("int main() {")
        output.append(f"    {node.name}::_main();")
        output.append("    return 0;")
        output.append("}")
        return "\n".join(output)

    elif isinstance(node, FunctionNode):
        ret_type = "void" if node.ret_type == "void" else map_type(node.ret_type)
        args_str = ", ".join([f"{map_type(typ)} {nm}" for typ, nm in node.args])
        code = f"    {ret_type} {node.name}({args_str}) {{\n"
        for stmt in node.body:
            code += "        " + generate_cpp(stmt) + "\n"
        code += "    }"
        return code

    elif isinstance(node, VarDeclNode):
        cpp_type = map_type(node.type_name)
        if node.value_expr:
            val = translate_expr(node.value_expr)
            return f"{cpp_type} {node.name} = {val};"
        else:
            return f"{cpp_type} {node.name};"

    elif isinstance(node, ReturnNode):
        val = translate_expr(node.expr)
        return f"return {val};"

    elif isinstance(node, PrintNode):
        val = translate_expr(node.expr)
        # This is a heuristic. A proper implementation would use a symbol table
        # to know the type of 'val'. For now, we assume if it's a simple variable
        # name that could be a variant, we use the variant printer.
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', val.strip()):
             return f"_print_variant({val});" # Try to print as variant
        return f"_print_simple({val});" # Print as a simple value
    elif isinstance(node, AssignmentNode):
        val = translate_expr(node.expr)
        # AssignmentNode now holds full LHS string in name
        return f"{node.name} = {val};"
    
    elif isinstance(node, ExpressionNode):
        val = translate_expr(node.text)
        return f"{val};"

    elif isinstance(node, IfNode):
        cond = translate_expr(node.condition)
        out = f"if ({cond}) {{\n"
        for stmt in node.if_body:
            out += "        " + generate_cpp(stmt) + "\n"
        out += "    }"
        if node.else_body is not None:
            out += " else {\n"
            for stmt in node.else_body:
                out += "        " + generate_cpp(stmt) + "\n"
            out += "    }"
        return out
        
    elif isinstance(node, WhileNode):
        cond = translate_expr(node.condition)
        out = f"while ({cond}) {{\n"
        for stmt in node.body:
            out += "        " + generate_cpp(stmt) + "\n"
        out += "    }"
        return out
    
    return ""

def translate_expr(expr_str):
    # Input handling
    if "input" in expr_str:
        pattern = r'int\s*\(\s*input\s*\('
        match = re.search(pattern, expr_str)
        # Case 1: int(input(...))
        if match:
            start_sub = "_input_int ("
            new_expr = re.sub(pattern, start_sub, expr_str, 1)
            stripped = new_expr.rstrip()
            if stripped.endswith(')'):
                new_expr = stripped[:-1]
            return new_expr.strip()
        
        # Case 2: input(...)
        pattern_str = r'input\s*\('
        match_str = re.search(pattern_str, expr_str)
        if match_str:
            return re.sub(pattern_str, "_input_str(", expr_str, 1)

    return expr_str

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
        
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, 'r') as f:
            code = f.read()
        tokens = lex(code)
        parser = Parser(tokens)
        ast = parser.parse()
        cpp_code = generate_cpp(ast)
        print(cpp_code)
    except Exception as e:
        print(f"Compilation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
