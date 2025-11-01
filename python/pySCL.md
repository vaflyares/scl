# SCL - Structured Configuration Language

**[Python Documentation](#python-documentation) | [Документация Python](#документация-python)**

---

## Python Documentation

### Overview

**SCL (Structured Configuration Language)** is a simple, human-readable configuration format with strong typing. It's designed to be easy to read and write while maintaining explicit type declarations.

**Note:** Currently, only the Python library is available. Libraries for Kotlin, Java, Rust, Elixir, Ruby, and JavaScript are planned for future releases.

### Installation

```bash
pip install structcfg-parser
```

Or add to your `requirements.txt`:
```
structcfg-parser==1.0.1
```

Then import and use:

```python
import scl_parser

# Parse from file
config = scl_parser.load("config.scl")

# Parse from string
config = scl_parser.loads(scl_text)

# Save to file
scl_parser.dump(config, "output.scl")

# Convert to string
scl_text = scl_parser.dumps(config)
```

### Syntax

#### Basic Structure
```
parameter_name :: type { value }
```

#### Comments
```
[ This is a comment ]
```

#### Supported Types

**Boolean** - `bool`
```
enabled :: bool { true }
disabled :: bool { false }
active :: bool { yes }
inactive :: bool { no }
```

**String** - `str`
```
name :: str { "Hello World" }
```

**Integer** - `num`
```
count :: num { 42 }
negative :: num { -10 }
```

**Float** - `fl`
```
price :: fl { 19.99 }
temperature :: fl { -5.5 }
```

**Multiline String** - `ml`
```
description :: ml {
    'This is a
    multiline text
    with line breaks'
}
```

**Object** - `class`
```
user :: class {
    name :: str { "John" }
    age :: num { 30 }
    active :: bool { yes }
}
```

**List** - `list(type)`
```
numbers :: list(num) { 1, 2, 3, 4, 5 }
names :: list(str) { "Alice", "Bob", "Charlie" }
flags :: list(bool) { true, false, true }
prices :: list(fl) { 9.99, 19.99, 29.99 }
```

### Example Configuration

```scl
[ Application Configuration ]

app_name :: str { "MyApp" }
version :: str { "1.0.0" }
debug :: bool { true }
max_connections :: num { 100 }
timeout :: fl { 30.5 }

description :: ml {
    'This is a sample
    application configuration'
}

database :: class {
    host :: str { "localhost" }
    port :: num { 5432 }
    ssl :: bool { yes }
}

allowed_ips :: list(str) { "192.168.1.1", "10.0.0.1" }
ports :: list(num) { 80, 443, 8080 }
```

### Python Usage Examples

#### Example 1: Simple Configuration Loading
**main.py**
```python
import scl_parser

def load_cfg():
    config = scl_parser.load("path/to/cfg.scl")
    return config

config = load_cfg()
apples = config['count']['apples']
pears = config['pears']

print(apples)  # Output: 2
print(pears)   # Output: 3
```

**cfg.scl**
```
count :: class {
    apples :: num { 2 }
    watermelons :: num { 3 }
}

pears :: num { 3 }
```

#### Example 2: Working with Lists
**app.py**
```python
import scl_parser

config = scl_parser.load("settings.scl")

# Access list items
servers = config['servers']
print(f"First server: {servers[0]}")  # Output: First server: server1.com

# Iterate over list
for server in servers:
    print(f"Server: {server}")

# Access numeric lists
ports = config['network']['ports']
print(f"Available ports: {ports}")  # Output: Available ports: [80, 443, 8080]

# Access nested values
db_config = config['database']
print(f"DB Host: {db_config['host']}")  # Output: DB Host: localhost
print(f"DB Port: {db_config['port']}")  # Output: DB Port: 5432
```

**settings.scl**
```
servers :: list(str) { "server1.com", "server2.com", "server3.com" }

network :: class {
    ports :: list(num) { 80, 443, 8080 }
    ssl_enabled :: bool { yes }
}

database :: class {
    host :: str { "localhost" }
    port :: num { 5432 }
    credentials :: class {
        username :: str { "admin" }
        use_ssl :: bool { true }
    }
}
```

#### Example 3: Creating and Saving Configuration
**generate_config.py**
```python
import scl_parser

# Create configuration dictionary
config = {
    'app_name': 'MyApplication',
    'version': '2.1.0',
    'debug_mode': False,
    'max_workers': 10,
    'timeout': 30.5,
    'features': ['auth', 'api', 'admin'],
    'limits': [100, 500, 1000],
    'settings': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'log_level': 'INFO'
    }
}

# Save to file
scl_parser.dump(config, "generated_config.scl")

# Or get as string
scl_string = scl_parser.dumps(config)
print(scl_string)
```

**generated_config.scl** (output)
```
app_name :: str { "MyApplication" }
version :: str { "2.1.0" }
debug_mode :: bool { false }
max_workers :: num { 10 }
timeout :: fl { 30.5 }
features :: list(str) { "auth", "api", "admin" }
limits :: list(num) { 100, 500, 1000 }
settings :: class {
    cache_enabled :: bool { true }
    cache_ttl :: num { 3600 }
    log_level :: str { "INFO" }
}
```

#### Example 4: Multiline Strings
**readme_gen.py**
```python
import scl_parser

config = scl_parser.loads("""
project_info :: class {
    name :: str { "MyProject" }
    
    description :: ml {
        'This is a long description
        that spans multiple lines.
        It can contain detailed information
        about the project.'
    }
    
    readme :: ml {
        '# MyProject
        
        ## Installation
        pip install myproject
        
        ## Usage
        import myproject'
    }
}
""")

info = config['project_info']
print(info['name'])
print("\nDescription:")
print(info['description'])
print("\nReadme:")
print(info['readme'])
```

---

## Документация Python

### Обзор

**SCL (Structured Configuration Language)** — простой, читаемый формат конфигурации со строгой типизацией. Разработан для удобства чтения и записи с явным указанием типов данных.

**Примечание:** В настоящее время доступна только библиотека для Python. Библиотеки для Kotlin, Java, Rust, Elixir, Ruby и JavaScript планируются в будущих релизах.

### Установка

```bash
pip install structcfg-parser
```

Или добавьте в ваш `requirements.txt`:
```
structcfg-parser==1.0.1
```

Затем импортируйте и используйте:

```python
import scl_parser

# Парсинг из файла
config = scl_parser.load("config.scl")

# Парсинг из строки
config = scl_parser.loads(scl_text)

# Сохранение в файл
scl_parser.dump(config, "output.scl")

# Преобразование в строку
scl_text = scl_parser.dumps(config)
```

### Синтаксис

#### Базовая структура
```
имя_параметра :: тип { значение }
```

#### Комментарии
```
[ Это комментарий ]
```

#### Поддерживаемые типы

**Логический** - `bool`
```
enabled :: bool { true }
disabled :: bool { false }
active :: bool { yes }
inactive :: bool { no }
```

**Строка** - `str`
```
name :: str { "Hello World" }
```

**Целое число** - `num`
```
count :: num { 42 }
negative :: num { -10 }
```

**Число с плавающей точкой** - `fl`
```
price :: fl { 19.99 }
temperature :: fl { -5.5 }
```

**Многострочная строка** - `ml`
```
description :: ml {
    'This is a
    multiline text
    with line breaks'
}
```

**Объект** - `class`
```
user :: class {
    name :: str { "John" }
    age :: num { 30 }
    active :: bool { yes }
}
```

**Список** - `list(тип)`
```
numbers :: list(num) { 1, 2, 3, 4, 5 }
names :: list(str) { "Alice", "Bob", "Charlie" }
flags :: list(bool) { true, false, true }
prices :: list(fl) { 9.99, 19.99, 29.99 }
```

### Пример конфигурации

```scl
[ Application Configuration ]

app_name :: str { "MyApp" }
version :: str { "1.0.0" }
debug :: bool { true }
max_connections :: num { 100 }
timeout :: fl { 30.5 }

description :: ml {
    'This is a sample
    application configuration'
}

database :: class {
    host :: str { "localhost" }
    port :: num { 5432 }
    ssl :: bool { yes }
}

allowed_ips :: list(str) { "192.168.1.1", "10.0.0.1" }
ports :: list(num) { 80, 443, 8080 }
```

### Примеры использования в Python

#### Пример 1: Простая загрузка конфигурации
**main.py**
```python
import scl_parser

def load_cfg():
    config = scl_parser.load("path/to/cfg.scl")
    return config

config = load_cfg()
apples = config['count']['apples']
pears = config['pears']

print(apples)  # Вывод: 2
print(pears)   # Вывод: 3
```

**cfg.scl**
```
count :: class {
    apples :: num { 2 }
    watermelons :: num { 3 }
}

pears :: num { 3 }
```

#### Пример 2: Работа со списками
**app.py**
```python
import scl_parser

config = scl_parser.load("settings.scl")

# Доступ к элементам списка
servers = config['servers']
print(f"First server: {servers[0]}")  # Вывод: First server: server1.com

# Итерация по списку
for server in servers:
    print(f"Server: {server}")

# Доступ к числовым спискам
ports = config['network']['ports']
print(f"Available ports: {ports}")  # Вывод: Available ports: [80, 443, 8080]

# Доступ к вложенным значениям
db_config = config['database']
print(f"DB Host: {db_config['host']}")  # Вывод: DB Host: localhost
print(f"DB Port: {db_config['port']}")  # Вывод: DB Port: 5432
```

**settings.scl**
```
servers :: list(str) { "server1.com", "server2.com", "server3.com" }

network :: class {
    ports :: list(num) { 80, 443, 8080 }
    ssl_enabled :: bool { yes }
}

database :: class {
    host :: str { "localhost" }
    port :: num { 5432 }
    credentials :: class {
        username :: str { "admin" }
        use_ssl :: bool { true }
    }
}
```

#### Пример 3: Создание и сохранение конфигурации
**generate_config.py**
```python
import scl_parser

# Создание словаря конфигурации
config = {
    'app_name': 'MyApplication',
    'version': '2.1.0',
    'debug_mode': False,
    'max_workers': 10,
    'timeout': 30.5,
    'features': ['auth', 'api', 'admin'],
    'limits': [100, 500, 1000],
    'settings': {
        'cache_enabled': True,
        'cache_ttl': 3600,
        'log_level': 'INFO'
    }
}

# Сохранение в файл
scl_parser.dump(config, "generated_config.scl")

# Или получение в виде строки
scl_string = scl_parser.dumps(config)
print(scl_string)
```

**generated_config.scl** (результат)
```
app_name :: str { "MyApplication" }
version :: str { "2.1.0" }
debug_mode :: bool { false }
max_workers :: num { 10 }
timeout :: fl { 30.5 }
features :: list(str) { "auth", "api", "admin" }
limits :: list(num) { 100, 500, 1000 }
settings :: class {
    cache_enabled :: bool { true }
    cache_ttl :: num { 3600 }
    log_level :: str { "INFO" }
}
```

#### Пример 4: Многострочные строки
**readme_gen.py**
```python
import scl_parser

config = scl_parser.loads("""
project_info :: class {
    name :: str { "MyProject" }
    
    description :: ml {
        'This is a long description
        that spans multiple lines.
        It can contain detailed information
        about the project.'
    }
    
    readme :: ml {
        '# MyProject
        
        ## Installation
        pip install myproject
        
        ## Usage
        import myproject'
    }
}
""")

info = config['project_info']
print(info['name'])
print("\nDescription:")
print(info['description'])
print("\nReadme:")
print(info['readme'])
```

---

## License / Лицензия

MIT License - Free to use / Свободная для использования
