# Aplikace pro správu objednávek

## Co to je?
Školní projekt který slouží ke správě objednávek, můžeme zde:
1. Zobrazit všechny zákazniky uložené v databázi
2. Zobrazit všechny produkty uložené v databázi
3. Zobrazit všechny objednávky uložene v databázi
4. Vložit novou objednávku do databáze
5. Upravit existující objednávku zda už byla zpracována
6. Smazat existující objednávku z databáze
7. Vygenerovat souhrný report kde můžeme vidět všechny objednávky zákazníku (konkretně můžeme videt kolik zákazník si udělal objednávek, kolik nakoupil produktů a jeho celkovou útratu)
8. Importovat data do databáze zákazníků a produktů

## Jak spustit program?
### Nejdříve budeme muset importovat Databázi
1. Otevřete si `MySQL Workbench`  a `Local instance` 
2. Klikněte na `Server` poté na `Data import`
3. Zaklikněte `Import from Self-Contained File` a vyberte soubor `EXPORT_DB.sql` který se nachází ve složce `pythonIota\SQL DATABAZE`
4. Pak kliknetě na `Import Progress` a spustě import databáze pomocí `Start Import`

## Nastavení Config souboru
1. Rozklikněte si config.json který se nacházi v `pythonIota\config.json`
2. Doplňte vaše heslo do lokální databáze

## Spuštění aplikace
#### Ve skole je treba ucinit pred instalaci nasleudujici pripravu:
1. V OS window vypněte proxy server (Tlačítko start, pak tlačítko ozubeného kola a do vyhledávání napsat proxy. Následně vypnout proxy, která tam je nastavena)
#### Poté můžeme pokračovat
1. Stáhněte `pythonIota.zip` a extrahujte soubor
2. Rozklikněte `pythonIota` měli by jste vidět soubor `main.py` 
3. Rozklikněte lištu kde je soubor umístěný a napiště do ní `cmd`
4. Napište `.venv\Scripts\activate`
#### Je potřeba stáhnout moduly
1. napište `pip install sqlalchemy`
2. napište `pip install pymysql`
3. Jako závěr spustíme program `py main.py`

## Knihovny třetích stran
- **`SQLAlchemy`**: ORM knihovna pro práci s databázemi (instalace: `pip install sqlalchemy`).
- **`pymysql`**: MySQL client pro připojení k MySQL databázím (instalace: `pip install pymysql`).


## Architektura aplikace
## Dokumentace E-R modelu databáze
### Tabulka: `customers`
Tabulka obsahuje informace o zákaznících.

| Název sloupce  | Datový typ      | Popis                                             |
|----------------|-----------------|---------------------------------------------------|
| `ID`           | `INT`           | Primární klíč, automaticky inkrementovaný.        |
| `first_name`   | `VARCHAR(50)`    | Křestní jméno zákazníka.                           |
| `last_name`    | `VARCHAR(50)`    | Příjmení zákazníka.                                |
| `email`        | `VARCHAR(100)`   | E-mailová adresa zákazníka (unikátní).             |
| `created_at`   | `DATETIME`       | Datum a čas vytvoření záznamu (výchozí hodnota: aktuální čas). |

### Tabulka: `products`
Tabulka obsahuje informace o produktech.

| Název sloupce  | Datový typ      | Popis                                             |
|----------------|-----------------|---------------------------------------------------|
| `ID`           | `INT`           | Primární klíč, automaticky inkrementovaný.        |
| `name`         | `VARCHAR(100)`   | Název produktu.                                   |
| `description`  | `VARCHAR(150)`   | Popis produktu.                                   |
| `price`        | `FLOAT`         | Cena produktu.                                    |
| `Stock`        | `INT`           | Počet dostupných kusů na skladě.                  |
| `category`     | `ENUM`          | Kategorii produktu (možnosti: `Electronics`, `Clothing`, `Books`, `Other`). |

### Tabulka: `orders`
Tabulka obsahuje informace o objednávkách.

| Název sloupce  | Datový typ      | Popis                                             |
|----------------|-----------------|---------------------------------------------------|
| `ID`           | `INT`           | Primární klíč, automaticky inkrementovaný.        |
| `customer_id`  | `INT`           | Cizí klíč odkazující na tabulku `customers`.      |
| `employee_id`  | `INT`           | Cizí klíč odkazující na tabulku `employees`.      |
| `order_date`   | `DATETIME`      | Datum a čas objednávky (výchozí hodnota: aktuální čas). |
| `total_price`  | `FLOAT`         | Celková cena objednávky.                          |
| `is_processed` | `BOOL`          | Stav objednávky (výchozí hodnota: `FALSE`).       |


### Tabulka: `order_items`
Tabulka propojuje produkty s objednávkami (M:N vztah).

| Název sloupce   | Datový typ      | Popis                                             |
|-----------------|-----------------|---------------------------------------------------|
| `ID`            | `INT`           | Primární klíč, automaticky inkrementovaný.        |
| `order_id`      | `INT`           | Cizí klíč odkazující na tabulku `orders`.         |
| `product_id`    | `INT`           | Cizí klíč odkazující na tabulku `products`.       |
| `quantity`      | `INT`           | Množství objednaného produktu.                    |
| `price_per_unit`| `FLOAT`         | Cena za jednotku produktu.                        |
| `total_price`   | `FLOAT`         | Celková cena položky (quantity * price_per_unit). |

### Tabulka: `employees`
Tabulka obsahuje informace o zaměstnancích.

| Název sloupce  | Datový typ      | Popis                                             |
|----------------|-----------------|---------------------------------------------------|
| `ID`           | `INT`           | Primární klíč, automaticky inkrementovaný.        |
| `first_name`   | `VARCHAR(50)`    | Křestní jméno zaměstnance.                        |
| `last_name`    | `VARCHAR(50)`    | Příjmení zaměstnance.                             |
| `email`        | `VARCHAR(100)`   | E-mailová adresa zaměstnance (unikátní).          |
| `position`     | `ENUM`          | Pozice zaměstnance (možnosti: `Manager`, `Storekeeper`, `Support`). |

### Pohledy (Views)

#### `customer_summary`
Tento pohled zobrazuje souhrn informací o zákaznících. Obsahuje:
- `customer_id` - ID zákazníka.
- `customer_name` - Celé jméno zákazníka (křestní + příjmení).
- `customer_email` - E-mailová adresa zákazníka.
- `total_orders` - Počet objednávek, které zákazník vytvořil.
- `total_spent` - Celková částka, kterou zákazník utratil (sumarizováno na základě objednávek).

#### `order_summary`
Tento pohled zobrazuje souhrn informací o objednávkách. Obsahuje:
- `order_id` - ID objednávky.
- `customer_name` - Celé jméno zákazníka.
- `customer_email` - E-mailová adresa zákazníka.
- `employee_name` - Celé jméno zaměstnance, který zpracoval objednávku.
- `employee_email` - E-mailová adresa zaměstnance.
- `order_date` - Datum vytvoření objednávky.
- `total_price` - Celková cena objednávky.
- `order_status` - Stav objednávky (buď 'Processed' pro zpracovanou objednávku, nebo 'Pending' pro nevyřízenou).


---
Krejčiřík Lukáš, C4a | Email: krejcirik@spsejecna.cz | 15.01.2025 | SPŠE Ječná | Školní projekt
