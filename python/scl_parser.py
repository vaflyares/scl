"""
SCL Parser Library

.scl (Structured Configuration Language).

template:
    import scl_parser
    
    # file parse
    config = scl_parser.load("config.scl")
    
    # str parse
    config = scl_parser.loads(scl_text)
    
    # save to file
    scl_parser.dump(config, "output.scl")
    
    # to str 
    scl_text = scl_parser.dumps(config)
"""

import re
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

__version__ = "1.0.0"
__author__ = "shareui"
__all__ = ["load", "loads", "dump", "dumps", "SCLParseError", "SCLSyntaxError"]


class SCLParseError(Exception):
    pass


class SCLSyntaxError(SCLParseError):
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        
        if line and column:
            super().__init__(f"Syntax error at line {line}, column {column}: {message}")
        else:
            super().__init__(f"Syntax error: {message}")


class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    DOUBLE_COLON = "::"
    BOOL = "bool"
    STR = "str"
    NUM = "num"
    FL = "fl"
    ML = "ml"
    CLASS = "class"
    LIST = "list"
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","
    STRING = "STRING"
    MULTILINE_STRING = "MULTILINE_STRING"
    NUMBER = "NUMBER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SCLSyntaxError(msg, self.line, self.column)
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() in ' \t':
            self.advance()
    
    def read_comment(self) -> Token:
        start_line = self.line
        start_col = self.column
        self.advance()
        comment = ""
        while self.peek() and self.peek() != ']':
            comment += self.advance()
        if self.peek() != ']':
            self.error("Unclosed comment")
        self.advance()
        return Token(TokenType.COMMENT, comment.strip(), start_line, start_col)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        self.advance()
        string = ""
        while self.peek() and self.peek() != '"':
            if self.peek() == '\\':
                self.advance()
                next_char = self.peek()
                if next_char is None:
                    self.error("Unexpected end of string after backslash")
                if next_char == 'n':
                    string += '\n'
                elif next_char == 't':
                    string += '\t'
                elif next_char in ('"', '\\'):
                    string += next_char
                else:
                    string += next_char
                self.advance()
            else:
                string += self.advance()
        if self.peek() != '"':
            self.error("Unclosed string")
        self.advance()
        return Token(TokenType.STRING, string, start_line, start_col)
    
    def read_multiline_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        self.advance()
        string = ""
        while self.peek() and self.peek() != '\'':
            string += self.advance()
        if self.peek() != '\'':
            self.error("Unclosed multiline string")
        self.advance()
        return Token(TokenType.MULTILINE_STRING, string, start_line, start_col)
    
    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        number = ""
        if self.peek() == '-':
            number += self.advance()
            if not self.peek() or not self.peek().isdigit():
                self.error("Expected digit after '-'")
        
        has_dot = False
        has_digits_before_dot = False
        has_digits_after_dot = False
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
                number += self.advance()
            else:
                number += self.advance()
                if has_dot:
                    has_digits_after_dot = True
                else:
                    has_digits_before_dot = True
        
        if not has_digits_before_dot and not has_digits_after_dot:
            self.error("Invalid number format")
        
        if has_dot:
            return Token(TokenType.FLOAT, float(number), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(number), start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_col = self.column
        identifier = ""
        while self.peek() and (self.peek().isalnum() or self.peek() in ('_', '-')):
            identifier += self.advance()
        
        keywords = {
            "bool": TokenType.BOOL,
            "str": TokenType.STR,
            "num": TokenType.NUM,
            "fl": TokenType.FL,
            "ml": TokenType.ML,
            "class": TokenType.CLASS,
            "list": TokenType.LIST,
        }
        boolean_values = {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
        }
        
        if identifier in keywords:
            return Token(keywords[identifier], identifier, start_line, start_col)
        elif identifier in boolean_values:
            return Token(TokenType.BOOLEAN, boolean_values[identifier], start_line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, identifier, start_line, start_col)
    
    def read_identifier_with_digits(self) -> Token:
        start_line = self.line
        start_col = self.column
        identifier = ""
        while self.peek() and (self.peek().isalnum() or self.peek() in ('_', '-')):
            identifier += self.advance()
        return Token(TokenType.IDENTIFIER, identifier, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.text):
            self.skip_whitespace()
            if self.peek() is None:
                break
            
            if self.peek() == '[':
                self.tokens.append(self.read_comment())
                continue
            
            if self.peek() == '\n':
                newline_line = self.line
                newline_col = self.column
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', newline_line, newline_col))
                continue
            
            if self.peek() == ':' and self.peek(1) == ':':
                start_col = self.column
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.DOUBLE_COLON, '::', self.line, start_col))
                continue
            
            if self.peek() in '{}(),':
                start_col = self.column
                ch = self.advance()
                ttype = {
                    '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE,
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN,
                    ',': TokenType.COMMA
                }[ch]
                self.tokens.append(Token(ttype, ch, self.line, start_col))
                continue
            
            if self.peek() == '"':
                self.tokens.append(self.read_string())
                continue
            
            if self.peek() == '\'':
                self.tokens.append(self.read_multiline_string())
                continue
            
            if self.peek() == '-' and self.peek(1) and self.peek(1).isdigit():
                self.tokens.append(self.read_number())
                continue
            
            if self.peek().isdigit():
                peek_ahead = self.pos + 1
                while peek_ahead < len(self.text) and self.text[peek_ahead].isdigit():
                    peek_ahead += 1
                if peek_ahead < len(self.text) and (self.text[peek_ahead].isalpha() or self.text[peek_ahead] == '_'):
                    self.tokens.append(self.read_identifier_with_digits())
                else:
                    self.tokens.append(self.read_number())
                continue
            
            if self.peek().isalpha() or self.peek() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            self.error(f"Unexpected character: {self.peek()}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.COMMENT)]
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        raise SCLSyntaxError(msg, token.line, token.column)
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def eat(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type.value}, got {token.type.value}")
        self.pos += 1
        return token
    
    def parse(self) -> Dict[str, Any]:
        config = {}
        while self.current_token().type != TokenType.EOF:
            name, value = self.parse_parameter()
            config[name] = value
        return config
    
    def parse_parameter(self) -> tuple:
        name_token = self.current_token()
        if name_token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            name = name_token.value
        elif name_token.type in (TokenType.BOOL, TokenType.STR, TokenType.NUM, 
                                  TokenType.FL, TokenType.ML, TokenType.CLASS, TokenType.LIST):
            self.pos += 1
            name = name_token.value
        elif name_token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            name = str(name_token.value)
        elif name_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            name = name_token.value
        else:
            self.error(f"Expected identifier or keyword, got {name_token.type.value}")
        
        self.eat(TokenType.DOUBLE_COLON)
        
        type_token = self.current_token()
        if type_token.type == TokenType.BOOL:
            self.eat(TokenType.BOOL)
            value = self.parse_bool_value()
        elif type_token.type == TokenType.STR:
            self.eat(TokenType.STR)
            value = self.parse_str_value()
        elif type_token.type == TokenType.NUM:
            self.eat(TokenType.NUM)
            value = self.parse_num_value()
        elif type_token.type == TokenType.FL:
            self.eat(TokenType.FL)
            value = self.parse_fl_value()
        elif type_token.type == TokenType.ML:
            self.eat(TokenType.ML)
            value = self.parse_ml_value()
        elif type_token.type == TokenType.CLASS:
            self.eat(TokenType.CLASS)
            value = self.parse_class_value()
        elif type_token.type == TokenType.LIST:
            self.eat(TokenType.LIST)
            value = self.parse_list_value()
        else:
            self.error(f"Unknown type: {type_token.value}")
        
        return name, value
    
    def parse_bool_value(self) -> bool:
        self.eat(TokenType.LBRACE)
        value_token = self.eat(TokenType.BOOLEAN)
        self.eat(TokenType.RBRACE)
        return value_token.value
    
    def parse_str_value(self) -> str:
        self.eat(TokenType.LBRACE)
        value_token = self.eat(TokenType.STRING)
        self.eat(TokenType.RBRACE)
        return value_token.value
    
    def parse_num_value(self) -> int:
        self.eat(TokenType.LBRACE)
        value_token = self.eat(TokenType.NUMBER)
        self.eat(TokenType.RBRACE)
        return value_token.value
    
    def parse_fl_value(self) -> float:
        self.eat(TokenType.LBRACE)
        value_token = self.current_token()
        if value_token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
        elif value_token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            value_token.value = float(value_token.value)
        else:
            self.error("Expected float or number")
        self.eat(TokenType.RBRACE)
        return value_token.value
    
    def parse_ml_value(self) -> str:
        self.eat(TokenType.LBRACE)
        value_token = self.eat(TokenType.MULTILINE_STRING)
        self.eat(TokenType.RBRACE)
        return value_token.value
    
    def parse_class_value(self) -> Dict[str, Any]:
        self.eat(TokenType.LBRACE)
        obj = {}
        while self.current_token().type != TokenType.RBRACE:
            name, value = self.parse_parameter()
            obj[name] = value
        self.eat(TokenType.RBRACE)
        return obj
    
    def parse_list_value(self) -> List[Any]:
        self.eat(TokenType.LPAREN)
        element_type = self.current_token()
        
        if element_type.type == TokenType.NUM:
            self.eat(TokenType.NUM)
            parser_func = lambda: self.eat(TokenType.NUMBER).value
        elif element_type.type == TokenType.FL:
            self.eat(TokenType.FL)
            def parse_float():
                if self.current_token().type == TokenType.FLOAT:
                    return float(self.eat(TokenType.FLOAT).value)
                else:
                    return float(self.eat(TokenType.NUMBER).value)
            parser_func = parse_float
        elif element_type.type == TokenType.BOOL:
            self.eat(TokenType.BOOL)
            parser_func = lambda: self.eat(TokenType.BOOLEAN).value
        elif element_type.type == TokenType.STR:
            self.eat(TokenType.STR)
            parser_func = lambda: self.eat(TokenType.STRING).value
        else:
            self.error(f"Unsupported list element type: {element_type.value}")
        
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        elements = []
        while self.current_token().type != TokenType.RBRACE:
            elements.append(parser_func())
            if self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            elif self.current_token().type != TokenType.RBRACE:
                self.error("Expected comma or closing brace")
        
        self.eat(TokenType.RBRACE)
        return elements


class Serializer:
    def __init__(self, indent: int = 4):
        self.indent = indent
    
    def serialize(self, data: Dict[str, Any], level: int = 0) -> str:
        lines = []
        indent_str = " " * (self.indent * level)
        
        for key, value in data.items():
            line = f"{indent_str}{key} :: "
            
            if isinstance(value, bool):
                line += f"bool {{ {'true' if value else 'false'} }}"
            elif isinstance(value, int):
                line += f"num {{ {value} }}"
            elif isinstance(value, float):
                line += f"fl {{ {value} }}"
            elif isinstance(value, str):
                if '\n' in value:
                    line += f"ml {{\n{indent_str}    '{value}'\n{indent_str}}}"
                else:
                    escaped_str = value.replace('\\', '\\\\').replace('"', '\\"')
                    line += f'str {{ "{escaped_str}" }}'
            elif isinstance(value, dict):
                line += "class {\n"
                line += self.serialize(value, level + 1)
                line += f"{indent_str}}}"
            elif isinstance(value, list):
                if not value:
                    line += "list(str) { }"
                else:
                    first = value[0]
                    
                    if isinstance(first, bool):
                        type_name = "bool"
                        if not all(isinstance(item, bool) for item in value):
                            raise SCLParseError(f"Mixed types in list for key '{key}': expected all bool")
                        items = ", ".join('true' if x else 'false' for x in value)
                    elif isinstance(first, int) and not isinstance(first, bool):
                        type_name = "num"
                        if not all(isinstance(item, int) and not isinstance(item, bool) for item in value):
                            raise SCLParseError(f"Mixed types in list for key '{key}': expected all int")
                        items = ", ".join(str(x) for x in value)
                    elif isinstance(first, float):
                        type_name = "fl"
                        valid_items = []
                        for item in value:
                            if isinstance(item, bool):
                                raise SCLParseError(f"Mixed types in list for key '{key}': bool not allowed in float list")
                            if not isinstance(item, (int, float)):
                                raise SCLParseError(f"Mixed types in list for key '{key}': expected all numeric")
                            valid_items.append(item)
                        items = ", ".join(str(x) if isinstance(x, float) else str(x) for x in valid_items)
                    elif isinstance(first, str):
                        type_name = "str"
                        if not all(isinstance(item, str) for item in value):
                            raise SCLParseError(f"Mixed types in list for key '{key}': expected all str")
                        escaped_items = [item.replace('\\', '\\\\').replace('"', '\\"') for item in value]
                        items = ", ".join(f'"{x}"' for x in escaped_items)
                    else:
                        raise SCLParseError(f"Unsupported list element type: {type(first)}")
                    
                    line += f"list({type_name}) {{ {items} }}"
            else:
                raise SCLParseError(f"Unsupported value type: {type(value)}")
            
            lines.append(line)
        
        return "\n".join(lines) + ("\n" if level == 0 else "\n")


def loads(text: str) -> Dict[str, Any]:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def load(filename: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    with open(filename, 'r', encoding=encoding) as f:
        text = f.read()
    return loads(text)


def dumps(data: Dict[str, Any], indent: int = 4) -> str:
    serializer = Serializer(indent=indent)
    return serializer.serialize(data)


def dump(data: Dict[str, Any], filename: str, indent: int = 4, encoding: str = 'utf-8'):
    text = dumps(data, indent=indent)
    with open(filename, 'w', encoding=encoding) as f:
        f.write(text)

if __name__ == "__main__":
    example_scl = """
    [ std cfg ]
    parameter :: bool { true }
    parameter2 :: str { "value2" }
    parameter3 :: num { -123 }
    parameter4 :: fl { -1.5 }
    
    desc :: ml {
        'hello
        world'
    }
    
    object1 :: class {
        objparam :: bool { true }
        objparam2 :: bool { false }
    }
    
    object2 :: class {
        obj2param :: ml { 
            'hello
            world'
        }
        obj2param2 :: bool { yes }
    }
    
    numbers :: list(num) { 1, -2, 4 }
    floats :: list(fl) { 1.5, -2.3, 4.7 }
    """
    
    try:
        print("=== Parsing SCL ===")
        config = loads(example_scl)
        print("\nParsed configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        print("\n=== Serializing back to SCL ===")
        scl_output = dumps(config)
        print(scl_output)
    except SCLSyntaxError as e:
        print(f"Syntax Error: {e}")
    except SCLParseError as e:
        print(f"Parse Error: {e}")
