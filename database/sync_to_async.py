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
        
        result = f"ID: {item['id']}\n" \
                    f"Product: {item['product']['liters']}L\n" \
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
        