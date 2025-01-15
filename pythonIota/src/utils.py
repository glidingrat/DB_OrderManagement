from src.models import Customer, Product, Order, OrderItem, Employee
import csv
import json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from sqlalchemy.sql import text
import re



def show_customers(session):
    """Zobrazí seznam zákazníků."""
    customers = session.query(Customer).all()
    print("\nZákazníci:")
    for customer in customers:
        print(f"{customer.id}: {customer.first_name} {customer.last_name} ({customer.email})")

def show_products(session):
    """Zobrazení všech produktů."""
    products = session.query(Product).all()
    if not products:
        print("Žádné produkty nebyly nalezeny.")
        return

    print("\nSeznam produktů:")
    for product in products:
        print(
            f"ID: {product.id}, Název: {product.name}, Popis: {product.description}, "
            f"Cena: {product.price}, Skladem: {product.stock}, Kategorie: {product.category}"
        )

def show_orders(session):
    """Zobrazení všech objednávek s detaily."""
    orders = session.query(Order).all()
    if not orders:
        print("Žádné objednávky nebyly nalezeny.")
        return

    print("\nSeznam objednávek:")
    for order in orders:
        customer = order.customer
        employee = order.employee
        employee_name = f"{employee.first_name} {employee.last_name}" if employee else "Nepřiřazen"
        print(
            f"ID objednávky: {order.id}, Zákazník: {customer.first_name} {customer.last_name}, "
            f"Zaměstnanec: {employee_name}, Datum: {order.order_date}, "
            f"Celková cena: {order.total_price}, Zpracováno: {'Ano' if order.is_processed else 'Ne'}"
        )

        order_items = order.order_items
        if order_items:
            print("  Položky objednávky:")
            for item in order_items:
                print(
                    f"    - Produkt: {item.product.name}, Množství: {item.quantity}, "
                    f"Cena za kus: {item.price_per_unit}, Celkem: {item.total_price}"
                )
        print()


def insert_order(session):
    """Vloží novou objednávku a přiřadí ji zaměstnanci."""
    try:
        while True:
            try:
                customer_id = int(input("Zadejte ID zákazníka: "))
                break
            except ValueError:
                print("Neplatný vstup. Zadejte celé číslo.")

        customer = session.query(Customer).filter_by(id=customer_id).first()
        if not customer:
            print("Zákazník nebyl nalezen.")
            return

        items = []
        while True:
            try:
                product_id = int(input("Zadejte ID produktu (nebo -1 pro ukončení): "))
            except ValueError:
                print("Neplatný vstup. Zadejte celé číslo.")
                continue

            if product_id == -1:
                break

            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                print("Produkt nebyl nalezen.")
                continue

            while True:
                try:
                    quantity = int(input(f"Zadejte množství produktu {product.name}: "))
                    break
                except ValueError:
                    print("Neplatný vstup. Zadejte celé číslo.")

            if quantity > product.stock:
                print(f"Nedostatečný sklad produktu {product.name}.")
                continue

            total_price = product.price * quantity
            items.append({"product": product, "quantity": quantity, "total_price": total_price})

        if not items:
            print("Nebyla vybrána žádná položka.")
            return


        total_order_price = sum(item["total_price"] for item in items)
        new_order = Order(
            customer_id=customer_id,
            total_price=total_order_price,
            order_date=datetime.now()
        )
        session.add(new_order)
        session.flush()  # Pro získání ID objednávky

        for item in items:
            product = item["product"]
            quantity = item["quantity"]
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price_per_unit=product.price,
                total_price=item["total_price"]
            )
            session.add(order_item)
            product.stock -= quantity  # Aktualizace skladu


        employees = session.query(Employee).all()
        if not employees:
            print("V databázi nejsou žádní zaměstnanci.")
            session.rollback()
            return

        print("\nDostupní zaměstnanci:")
        for emp in employees:
            print(f"{emp.id}: {emp.first_name} {emp.last_name} ({emp.position})")

        while True:
            try:
                employee_id = int(input("Zadejte ID zaměstnance pro přiřazení objednávky: "))
                break
            except ValueError:
                print("Neplatný vstup. Zadejte celé číslo.")

        employee = session.query(Employee).filter_by(id=employee_id).first()
        if not employee:
            print("Zaměstnanec nebyl nalezen.")
            session.rollback()
            return

        # Přiřazení zaměstnance k objednávce
        new_order.employee_id = employee_id

        session.commit()
        print("Objednávka byla úspěšně přidána a přiřazena zaměstnanci.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Chyba při vkládání objednávky: {e}")


def delete_order(session):
    """Smaže objednávku a její položky."""
    try:
        while True:
            try:
                order_id = int(input("Zadejte ID objednávky ke smazání: "))
                break
            except ValueError:
                print("Neplatný vstup. Zadejte celé číslo.")

        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            print("Objednávka nebyla nalezena.")
            return

        # Smazání položek objednávky
        order_items = session.query(OrderItem).filter_by(order_id=order_id).all()
        for item in order_items:
            session.delete(item)

        # Smazání samotné objednávky
        session.delete(order)
        session.commit()
        print("Objednávka a její položky byly úspěšně smazány.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Chyba při mazání objednávky: {e}")

def update_order(session):
    """Upraví objednávku a její položky."""
    try:
        while True:
            try:
                order_id = int(input("Zadejte ID objednávky k úpravě: "))
                break
            except ValueError:
                print("Neplatný vstup. Zadejte celé číslo.")

        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            print("Objednávka nebyla nalezena.")
            return

        is_processed = input("Je objednávka zpracovaná? (ano/ne): ").strip().lower()
        order.is_processed = True if is_processed == "ano" else False

        session.commit()
        print(f"Objednávka s ID {order_id} byla úspěšně upravena.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Chyba při úpravě objednávky: {e}")

def generate_report(session):
    """Vygeneruje souhrnný report pouze pro zákazníky, kteří mají objednávky."""
    try:
        # Použití funkce text() pro označení SQL příkazu
        query = text("""
            SELECT c.first_name, c.last_name, COUNT(DISTINCT o.id) AS order_count, 
                   SUM(o.total_price) AS total_spent,
                   COUNT(DISTINCT oi.product_id) AS unique_products
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            JOIN order_items oi ON o.id = oi.order_id
            GROUP BY c.id
            HAVING COUNT(DISTINCT o.id) > 0
        """)

        results = session.execute(query)

        print("\nSouhrnný report:")
        print(f"{'Jméno a příjmení':<25} | {'Počet objednávek':<20} | {'Celková útrata':<15} | {'Počet produktů':<25}")
        print("-" * 85)

        for row in results:
            print(
                f"{row.first_name} {row.last_name:<20} | "
                f"{row.order_count:<20} | "
                f"{row.total_spent:<15.2f} | "
                f"{row.unique_products:<15}"
            )

    except SQLAlchemyError as e:
        print(f"Chyba při generování reportu: {e}")



def get_allowed_categories(session, table_name, column_name):
    """Načte povolené hodnoty ENUM pro zadaný sloupec z tabulky."""
    try:
        query = text(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
        result = session.execute(query).fetchone()
        if result:
            enum_values = result[1]  # Druhý sloupec obsahuje definici typu ENUM
            if enum_values.startswith("enum("):
                # Extrahujeme hodnoty ENUM
                values = enum_values[5:-1].replace("'", "").split(",")
                return values
        return []
    except Exception as e:
        print(f"Chyba při načítání kategorií: {e}")
        return []

def safe_strip(value):
    """Pomocná funkce pro bezpečné ořezání hodnoty."""
    return str(value).strip() if value is not None else ""


def validate_customer_data(row):
    """Validuje a vrací data zákazníka."""
    try:
        first_name = safe_strip(row.get("FirstName"))
        last_name = safe_strip(row.get("LastName"))
        email = safe_strip(row.get("Email"))

        # Kontrola, zda je křestní jméno a příjmení validní
        name_pattern = r"^[a-zA-ZÀ-ž]{2,}$"
        if not first_name:
            raise ValueError("Chybějící nebo neplatné křestní jméno.")
        if not re.match(name_pattern, first_name):
            raise ValueError(
                f"Neplatné křestní jméno: '{first_name}'. Musí obsahovat pouze písmena a mít alespoň 2 znaky.")

        if not last_name:
            raise ValueError("Chybějící nebo neplatné příjmení.")
        if not re.match(name_pattern, last_name):
            raise ValueError(f"Neplatné příjmení: '{last_name}'. Musí obsahovat pouze písmena a mít alespoň 2 znaky.")

        # Kontrola platnosti e-mailu
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not email:
            raise ValueError("Chybějící nebo neplatný e-mail.")
        if not re.match(email_pattern, email):
            raise ValueError(f"Neplatný formát e-mailu: '{email}'.")

        # Vytvoření objektu Customer
        return Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            created_at=datetime.now()
        )

    except KeyError as e:
        raise ValueError(f"Chybějící povinné pole: {e}")
    except ValueError as e:
        raise ValueError(f"Neplatná hodnota: {e}")


def validate_product_data(row, allowed_categories):
    """Validuje a vrací produktová data."""
    try:
        name = safe_strip(row["Name"])
        description = safe_strip(row.get("Description", ""))
        price = float(row["Price"]) if row["Price"] else 0.0
        stock = int(row["Stock"]) if row["Stock"] else 0
        category = safe_strip(row["Category"])

        # Ověření, že name není prázdné a obsahuje alespoň jedno písmeno
        if not name or not re.search(r"[a-zA-Z]", name):
            raise ValueError("Název produktu musí obsahovat alespoň jedno písmeno.")

        # Popis je volitelný, ale pokud existuje, měl by obsahovat alespoň jedno písmeno
        if description and not re.search(r"[a-zA-Z]", description):
            raise ValueError("Popis produktu (pokud je zadán) musí obsahovat alespoň jedno písmeno.")

        if price < 0:
            raise ValueError("Cena nesmí být záporná.")
        if stock < 0:
            raise ValueError("Sklad nesmí být záporný.")
        if category not in allowed_categories:
            raise ValueError(
                f"Neplatná kategorie: '{category}'. Povolené kategorie: {', '.join(allowed_categories)}.")

        return Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )
    except KeyError as e:
        raise ValueError(f"Chybějící povinné pole: {e}")
    except ValueError as e:
        raise ValueError(f"Neplatná hodnota: {e}")

def import_data(session, file_path, table_name):
    """Importuje data z CSV nebo JSON do zvolené tabulky."""
    try:
        allowed_categories = get_allowed_categories(session, "products", "category")
        if not allowed_categories:
            print("Nepodařilo se načíst povolené kategorie.")
            return

        if file_path.endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customer = validate_customer_data(row)
                    session.add(customer)
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for row in data:
                    customer = validate_customer_data(row)
                    session.add(customer)
        else:
            print("Nepodporovaný formát souboru.")
            return

        try:
            session.commit()
            print(f"Data byla úspěšně importována do tabulky {table_name}.")
        except IntegrityError as e:
            session.rollback()
            if 'Duplicate entry' in str(e.orig):
                duplicated_email = str(e.orig).split("for key")[0].split("entry ")[1][:-1]
                print(f"Chyba: Tento e-mail je již zaregistrován: {duplicated_email}")
            else:
                print(f"Chyba při importu dat: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Chyba při importu dat: {e}")
    except Exception as e:
        print(f"Obecná chyba při importu dat: {e}")

