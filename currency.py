import asyncio
import socketio

sio = socketio.AsyncClient()

async def get_currency(actor_id):
    request_id = "unique-request-id-get"
    request = {
        "action": "getCurrency",
        "actorId": actor_id,
        "requestId": request_id
    }

    @sio.event
    async def connect():
        print('Connection established')
        await sio.emit('module.remote-currency-control', request)
        print('Request sent:', request)

    @sio.on('currencyResponse')
    async def on_currency_response(data):
        print('Currency response received:', data)
        if data['requestId'] == request_id:
            print('Currency:', data['currency'])
            await sio.disconnect()

    @sio.event
    async def connect_error(data):
        print("The connection failed!", data)

    @sio.event
    async def disconnect():
        print('Disconnected from server')

    await sio.connect('http://192.18.144.0:30000')
    await sio.wait()

async def update_currency(actor_id, new_currency):
    request_id = "unique-request-id-update"
    request = {
        "action": "updateCurrency",
        "actorId": actor_id,
        "currency": new_currency,
        "requestId": request_id
    }

    @sio.event
    async def connect():
        print('Connection established')
        await sio.emit('module.remote-currency-control', request)
        print('Update request sent:', request)

    @sio.event
    async def connect_error(data):
        print("The connection failed!", data)

    @sio.event
    async def disconnect():
        print('Disconnected from server')

    await sio.connect('http://192.18.0.0:30000')
    await sio.wait()

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
