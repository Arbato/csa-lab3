# csa-lab3
 - Арбатова Ксения Владимировна, P3233
 - Вариант: `asm | acc | neum | hw | instr | struct | stream | mem | pstr | prob2 `
 - С упрощением

## Язык программирования

### Синтаксис

#### Форма Бэкуса-Наура

```enbf

```

#### Объяснение


#### Пример

```asm
.data
A: 5
B: 3
sum: 0

.instructions
    LD A
    ADD B
    ST sum
    HLT
```

### Семантика


## Организация памяти


```
            memory
    +-----------------+
    |   JMP TO CODE   |
    +-----------------+
    |   STATIC DATA   |
    |                 |
    |                 |
    |                 |
    +-----------------+
    |      CODE       |
    |                 |
    |                 |
    |                 |
    +-----------------+
    |      STACK      |
    |                 |
    |                 |
    +-----------------+

```


## Система команд
Без аргументов:
- HLT - завершение программы
- NOT - логическое НЕ к аккумулятору, 0 -> 1 или !0 -> 0
- NEG - изменить знак аккумулятора, N = !N
Переход:
- JMP <arg1> - безусловный переход к arg1
- JZ <arg1> - если Z = 1, переход к arg1
- JNZ <arg1> - если Z = 0, переход к arg1

- LD <arg1> - записать из arg1 в ACC
- ST <arg1> - записать из аккумулятора в arg1
- ADD <arg1> - добавить к ACC arg1
- SUB <arg1> - вычесть из ACC arg1
- MUL <arg1> - умножить ACC на arg1
- DIV <arg1> - делить ACC на arg1
- OR <arg1> - побитовое ИЛИ ACC с arg1
- AND <arg1> - побитовое И ACC с arg1
- CMP <arg1> - Проставить флаги NZ как при операции ACC - arg1

### Набор команд

| Команда | Адресная | Ветвление | Количество тактов<br/>(Включая чтение команды и операнда) | Описание                                                               |
|:--------|:---------|-----------|:----------------------------------------------------------|:-----------------------------------------------------------------------|

### Кодирование команд

 - Команды сериализуются в список JSON
 - Каждая команда представляется объектом с полями:
    - `index` - ячейка памяти
    - `opcode` - код операции. Для записи констант используется `NOP`
    - `value` - значение операнда. Для команд без операндов используется 0
    - `relative` - указывает если команда использует относительный адрес.

Пример сериализации команд:

 - Исходный код:
```asm

```
 - Сериализованный код:
```json

```

## Транслятор

Интерфейс командной строки: `translator.py <source_file> <target_file>`

Правила трансляции:
 - Одна переменная - одна строка. 
 - Одна команда - одна строка. 
 - Метки пишутся в отдельной строке. 
 - Названия секций пишутся в отдельной строке. 
 - Ссылаться можно только на существующие переменные и метки.


## Модель процессора

Интерфейс командной строки: `machine.py <code_file> <input_file>`

### DataPath

![Alt text](./image/UntitledDiagram.jpg)
Класс `data_path` реализует управление памятью и регистрами процессора.
 
### ControlUnit
Класс `control_unit` реализует управление процессором.
Особенности работы модели:

## Тестирование
 - Тестирование осуществляется при помощи golden test-ов.
 