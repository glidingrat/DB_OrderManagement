from src.utils import show_customers, show_products, insert_order, generate_report, show_orders, import_data, delete_order, update_order


def start_ui(session):
    print("Správa objednávek")
    while True:
        print("=" * 35)
        print("Vyberte příkaz:")
        print("\t1. Zobrazit zákazníky")
        print("\t2. Zobrazit produkty")
        print("\t3. Zobrazit objednavky")
        print("\t4. Vložit novou objednávku")
        print("\t5. Upravit objednávku")
        print("\t6. Smazat objednávku")
        print("\t7. Vygenerovat report")
        print("\t8. Importovat data")
        print("\t9. Ukončit aplikaci")

        choice = input("Zadejte číslo příkazu(1-9): ")
        if choice == "1":
            show_customers(session)
        elif choice == "2":
            show_products(session)
        elif choice == "3":
            show_orders(session)
        elif choice == "4":
            insert_order(session)
        elif choice == "5":
            update_order(session)
        elif choice == "6":
            delete_order(session)
        elif choice == "7":
            generate_report(session)
        elif choice == "8":
            while True:
                print("=" * 35)
                print("\t1. Import customers.csv")
                print("\t2. Import products.json")
                print("\t3. Zpět do menu")
                choice = input("Zadejte číslo akce: ")
                if choice == "1":
                    import_data(session, "customers.csv", "customers")
                elif choice == "2":
                    import_data(session, "products.json", "products")
                elif choice == "3":
                    break
        elif choice == "9":
            print("Aplikace ukončena.")
            break
        else:
            print("Neplatná volba.")
