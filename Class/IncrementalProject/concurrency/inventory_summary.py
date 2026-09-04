from multiprocessing import Process

def calculate_summary(products):
    print("\nInventory Summary")
    print("")
    total_items = sum(product.quantity for product in products)

    inventory_value = sum(product.price * product.quantity for product in products)

    print(f"Total Products: {total_items}")
    print(f"INventory value: Rs.{inventory_value:.2f}")

def generate_summary(products):
    process = Process(target=calculate_summary,args=(products,))

    process.start()
    process.join()