from asgiref.sync import sync_to_async

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import markups as btn

@sync_to_async
def get_all_items(items):
    result = [
                {
                    "id": item.id,
                    "quantity": item.quantity,
                    "product": {
                        "id": item.product.id,
                        "liters": item.product.litrs,
                        "price": item.product.price,
                    },
                }
                for item in items
            ]
    return {"items": result}


@sync_to_async
def get_basket_inline_btn(basket_items):
    messages = []
    for i in range(len(basket_items['items'])): 
        item = basket_items['items'][i]  
        
        result = f"Product: {item['product']['liters']}L\n" \
                    f"Quantity: {item['quantity']}\n" \
                    f"Price per item: {item['product']['price']} UZS\n" \
                    f"Total: {item['product']['price'] * item['quantity']} UZS\n\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_cart_{item['id']}"),
        ],
        [
            InlineKeyboardButton(text="➕ 1", callback_data=f"add_{item['id']}"),
            InlineKeyboardButton(text="➖ 1", callback_data=f"subtract_{item['id']}"),
        ]
        ])
        messages.append((result, keyboard))
    return messages
        

async def format_orders_for_message(orders):
    messages = []
    for order in orders:
        # Start with order details
        message = (
            f"🏢 Company Name: {order['company_name']}\n"
            f"📞 Contact: {order['company_contact']}\n"
            f"👥 Number of Employees: {order['number_employee']}\n"
            f"⏳ Drink Time: {order['time_drink']} mins\n"
            f"🗓 Created At: {order['created_at']:%Y-%m-%d %H:%M:%S}\n"
            f"📦 Products:\n"
        )
        
        # Add product details
        for product in order['products']:
            message += (
                f"     📋 Product Name: {product['product_name']}\n"
                f"     🔢 Quantity: {product['quantity']}\n"
                f"     💵 Price: {product['price']:.2f}\n"
            )
        
        messages.append(message)
    
    return "\n\n".join(messages)