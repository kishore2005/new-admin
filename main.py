import sqlitecloud
import flet as ft

# Step 1: Set up the database
def setup_database():
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            image TEXT,
            name TEXT,
            price TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Step 2: Fetch data from the database
def fetch_products():
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('SELECT id, image, name, price FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

# Step 3: Insert data into the database
def insert_product(image, name, price):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (image, name, price) VALUES (?, ?, ?)', (image, name, price))
    conn.commit()
    conn.close()

# Step 4: Update data in the database
def update_product(product_id, image, name, price):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET image = ?, name = ?, price = ? WHERE id = ?', (image, name, price, product_id))
    conn.commit()
    conn.close()

# Step 5: Delete data from the database
def delete_product(product_id):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# Step 6: Display data in Flet
def main(page: ft.Page):
    # Add an AppBar with a metallic look
    page.appbar = ft.AppBar(
        title=ft.Text("ADMIN"),
        center_title=True,
        bgcolor="#000000"  # Silver metallic color
    )

    selected_product_id = None

    def add_product(e):
        insert_product(image_input.value, name_input.value, price_input.value)
        image_input.value = ""
        name_input.value = ""
        price_input.value = ""
        page.update()
        load_data()

    def load_data():
        products = fetch_products()
        table.rows.clear()
        for product in products:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Image(src=product[1], width=50, height=50)),
                        ft.DataCell(ft.Text(product[2])),
                        ft.DataCell(ft.Text(product[3])),
                        ft.DataCell(ft.Row([
                            ft.ElevatedButton(text="Edit", on_click=lambda e, product=product: edit_product(product)),
                            ft.ElevatedButton(text="Delete", on_click=lambda e, product_id=product[0]: delete_product_info(product_id))
                        ]))
                    ]
                )
            )
        
        page.update()

    def edit_product(product):
        nonlocal selected_product_id
        selected_product_id = product[0]
        image_input.value = product[1]
        name_input.value = product[2]
        price_input.value = product[3]
        page.update()

    def update_product_info(e):
        if selected_product_id is not None:
            update_product(selected_product_id, image_input.value, name_input.value, price_input.value)
            image_input.value = ""
            name_input.value = ""
            price_input.value = ""
            page.update()
            load_data()

    def delete_product_info(product_id):
        delete_product(product_id)
        page.update()
        load_data()

    image_input = ft.TextField(label="Product Image URL")
    name_input = ft.TextField(label="Product Name")
    price_input = ft.TextField(label="Product Price")
    add_button = ft.ElevatedButton(text="Add Product", on_click=add_product)
    update_button = ft.ElevatedButton(text="Update Product", on_click=update_product_info)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Image")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[]
    )

    # Wrap the product table in a ListView to enable scrolling
    product_list_view = ft.ListView(
        controls=[table],
        expand=True
    )

    # Wrap the content in a Column with scroll mode inside a Container
    scrollable_content = ft.Container(
        content=ft.Column(
            [
                image_input, name_input, price_input, add_button, update_button, product_list_view
            ],
            scroll=ft.ScrollMode.AUTO
        ),
        expand=True
    )

    page.add(scrollable_content)
    load_data()

# Run the setup function to create the database
setup_database()

# Run the Flet app
ft.app(target=main)
