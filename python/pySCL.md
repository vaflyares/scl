# SCL - Structured Configuration Language

**[Python Documentation](#python-documentation) | [Документация Python](#документация-python)**

---

## Python Documentation

### Overview

**SCL (Structured Configuration Language)** is a simple, human-readable configuration format with strong typing. It's designed to be easy to read and write while maintaining explicit type declarations.

**Note:** Currently, only the Python library is available. Libraries for Kotlin, Java, Rust, Elixir, Ruby, and JavaScript are planned for future releases.

### Installation

1. Download `scl_parser.py` and add it to your project directory
2. Import and use:

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

---

## Документация Python

### Обзор

**SCL (Structured Configuration Language)** — простой, читаемый формат конфигурации со строгой типизацией. Разработан для удобства чтения и записи с явным указанием типов данных.

**Примечание:** В настоящее время доступна только библиотека для Python. Библиотеки для Kotlin, Java, Rust, Elixir, Ruby и JavaScript планируются в будущих релизах.

### Установка

1. Скачайте `scl_parser.py` и добавьте его в директорию вашего проекта
2. Импортируйте и используйте:

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
включено :: bool { true }
выключено :: bool { false }
активно :: bool { yes }
неактивно :: bool { no }
```

**Строка** - `str`
```
имя :: str { "Привет Мир" }
```

**Целое число** - `num`
```
количество :: num { 42 }
отрицательное :: num { -10 }
```

**Число с плавающей точкой** - `fl`
```
цена :: fl { 19.99 }
температура :: fl { -5.5 }
```

**Многострочная строка** - `ml`
```
описание :: ml {
    'Это многострочный
    текст с переносами
    строк'
}
```

**Объект** - `class`
```
пользователь :: class {
    имя :: str { "Иван" }
    возраст :: num { 30 }
    активен :: bool { yes }
}
```

**Список** - `list(тип)`
```
числа :: list(num) { 1, 2, 3, 4, 5 }
имена :: list(str) { "Алиса", "Боб", "Чарли" }
флаги :: list(bool) { true, false, true }
цены :: list(fl) { 9.99, 19.99, 29.99 }
```

### Пример конфигурации

```scl
[ Конфигурация приложения ]

название_приложения :: str { "МоёПриложение" }
версия :: str { "1.0.0" }
отладка :: bool { true }
макс_соединений :: num { 100 }
таймаут :: fl { 30.5 }

описание :: ml {
    'Это пример
    конфигурации приложения'
}

база_данных :: class {
    хост :: str { "localhost" }
    порт :: num { 5432 }
    ssl :: bool { yes }
}

разрешенные_ip :: list(str) { "192.168.1.1", "10.0.0.1" }
порты :: list(num) { 80, 443, 8080 }
```

---

## License / Лицензия

MIT License - Free to use / Свободная для использования