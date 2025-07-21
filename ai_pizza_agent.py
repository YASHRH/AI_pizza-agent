import gradio as gr

# Session context
chat_history = []
order = {
    "pizza": None,
    "toppings": [],
    "sides": [],
    "drink": None,
    "address": None,
    "confirmed": False
}

pizza_menu = [
    "Margherita", "Pepperoni", "BBQ Chicken", "Veggie Supreme", "Hawaiian", "Four Cheese", "Spicy Sausage", "Mushroom Delight"
]

toppings_menu = [
    "Extra cheese", "Olives", "Mushrooms", "Peppers", "Onions", "Jalapenos", "Basil", "Sweetcorn", "Paneer"
]

sides_menu = [
    "Garlic Bread", "Chicken Wings", "Cheesy Sticks", "Fries", "Salad", "Mozzarella Bites"
]

drinks_menu = [
    "Coke", "Sprite", "Fanta", "Water", "Pepsi", "Iced Tea", "Lemonade", "Orange Juice"
]

def pizza_agent(message, history):
    global order
    try:
        user_input = message.lower()

        # Reset confirmation if user wants to start over
        if "start over" in user_input or "reset" in user_input:
            order = { "pizza": None, "toppings": [], "sides": [], "drink": None, "address": None, "confirmed": False }
            return "", history + [(message, "Sure! Let's start fresh. What pizza would you like?")]

        response = ""

        if not order["pizza"]:
            for pizza in pizza_menu:
                if pizza.lower() in user_input:
                    order["pizza"] = pizza
                    response = f"{pizza}? Great choice! Any toppings you want to add?"
                    break
            if not order["pizza"]:
                response = "Which pizza would you like? Options: " + ", ".join(pizza_menu)

        elif order["pizza"] and not order["toppings"]:
            found_toppings = [top for top in toppings_menu if top.lower() in user_input]
            if found_toppings:
                order["toppings"].extend(found_toppings)
                response = f"Added {', '.join(found_toppings)}. Would you like any sides? We have {', '.join(sides_menu)}"
            else:
                response = "Do you want any toppings? You can say things like 'extra cheese' or 'olives'."

        elif order["toppings"] and not order["sides"]:
            found_sides = [side for side in sides_menu if side.lower() in user_input]
            if found_sides:
                order["sides"].extend(found_sides)
                response = f"Got it: {', '.join(found_sides)}. Want a drink? Options: {', '.join(drinks_menu)}"
            elif any(word in user_input for word in ["no", "none"]):
                response = f"No problem. Would you like a drink? Options: {', '.join(drinks_menu)}"
            else:
                response = f"Please choose from our sides: {', '.join(sides_menu)}"

        elif order["sides"] is not None and not order["drink"]:
            found_drink = next((drink for drink in drinks_menu if drink.lower() in user_input), None)
            if found_drink:
                order["drink"] = found_drink
                response = "Thanks! Now, could you please give me your delivery address?"
            elif any(word in user_input for word in ["no", "none"]):
                order["drink"] = "No drink"
                response = "Okay, no drink then. Can you give me your delivery address?"
            else:
                response = f"Pick a drink from: {', '.join(drinks_menu)} or say 'no drink'."

        elif not order["address"]:
            order["address"] = message
            summary = f"""Here’s your order summary:
- 🍕 Pizza: {order['pizza']}
- 🧀 Toppings: {', '.join(order['toppings']) if order['toppings'] else 'None'}
- 🍟 Sides: {', '.join(order['sides']) if order['sides'] else 'None'}
- 🥤 Drink: {order['drink']}
- 🏠 Delivery Address: {order['address']}

Shall I confirm this order? (yes/no)"""
            response = summary

        elif not order["confirmed"]:
            if "yes" in user_input:
                order["confirmed"] = True
                response = "✅ Your order is confirmed! It’ll be delivered shortly. Enjoy your meal! 🍕"
            elif "no" in user_input:
                response = "Order cancelled. Would you like to start over?"
                order = { "pizza": None, "toppings": [], "sides": [], "drink": None, "address": None, "confirmed": False }
            else:
                response = "Please reply 'yes' to confirm or 'no' to cancel."

        else:
            response = "Would you like to place another order?"

        history.append((message, response))
        return "", history

    except Exception as e:
        error_msg = f"⚠️ Error: {e}"
        print("Exception:", e)
        history.append((message, error_msg))
        return "", history

# Optional TTS and STT imports (you can implement later if needed)
# import pyttsx3
# import speech_recognition as sr

# UI
with gr.Blocks(theme=gr.themes.Base()) as demo:
    gr.Markdown("🍕 **PizzaBot Express - Your Personal Assistant**\nTalk to your assistant like you would on a phone call. It understands toppings, sides, drinks, and even addresses!")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    clear_btn = gr.Button("Restart")

    msg.submit(pizza_agent, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: ("", []), None, [msg, chatbot])

# Run
if __name__ == "__main__":
    demo.launch()
