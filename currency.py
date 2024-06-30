import asyncio
import socketio

sio = socketio.AsyncClient()

async def connect_and_send(request, event_name, response_handler):
    @sio.event
    async def connect():
        print('Connection established')
        await sio.emit('module.remote-currency-control', request)
        print(f'{event_name} request sent:', request)

    @sio.on(event_name)
    async def on_response(data):
        print(f'{event_name} response received:', data)
        await response_handler(data)
        await sio.disconnect()

    await sio.connect('http://x:30000')
    await sio.wait()

async def get_currency(actor_id):
    request_id = "unique-request-id-get"
    request = {
        "action": "getCurrency",
        "actorId": actor_id,
        "requestId": request_id
    }

    async def handle_response(data):
        if data['requestId'] == request_id:
            print('Currency:', data.get('currency'))
        else:
            print('Unexpected response:', data)

    await connect_and_send(request, 'currencyResponse', handle_response)

async def update_currency(actor_id, new_currency):
    request_id = "unique-request-id-update"
    request = {
        "action": "updateCurrency",
        "actorId": actor_id,
        "currency": new_currency,
        "requestId": request_id
    }

    async def handle_response(data):
        if data['requestId'] == request_id:
            print('Update confirmed')
        else:
            print('Unexpected response:', data)

    await connect_and_send(request, 'updateCurrencyResponse', handle_response)

@sio.event
async def connect_error(data):
    print("The connection failed!", data)

@sio.event
async def disconnect():
    print('Disconnected from server')

# Example usage
actor_id = "8s3BJnLyIZu7otje"
new_currency = {
    "pp": 10,
    "gp": 50,
    "ep": 5,
    "sp": 100,
    "cp": 200
}

# Ensure all tasks run in the same event loop
async def main():
    await get_currency(actor_id)
    await update_currency(actor_id, new_currency)

# Run the main function
asyncio.run(main())
