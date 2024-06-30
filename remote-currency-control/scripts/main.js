import { getCurrency, updateCurrency } from './currency.js';
import { SocketLib } from 'socketlib';

// Ensure socketlib is available
const MODULE_ID = 'remote-currency-control';
const socket = SocketLib.registerModule(MODULE_ID);

// Log initialization
Hooks.once('init', async function() {
    console.log('Remote Currency Control | Initializing');
});

// Register socket event handler
Hooks.once('ready', async function() {
    console.log('Remote Currency Control | Ready');

    socket.register('handleRequest', async (data) => {
        console.log('Request received:', data);

        if (data.action === 'getCurrency') {
            const currency = await getCurrency(data.actorId);
            console.log('Currency fetched for actor:', data.actorId, currency);
            socket.executeAsGM('sendResponse', {
                action: 'currencyResponse',
                currency: currency,
                requestId: data.requestId
            });
        } else if (data.action === 'updateCurrency') {
            await updateCurrency(data.actorId, data.currency);
            console.log('Currency updated for actor:', data.actorId, data.currency);
        }
    });

    // Test if socket registration works by sending a test message
    socket.executeForEveryone('handleRequest', { action: 'test', message: 'This is a test message' });
});

// Function to send response
socket.register('sendResponse', async (data) => {
    console.log('Sending response:', data);
    game.socket.emit('module.remote-currency-control', data);
});
