import { getCurrency, updateCurrency } from './currency.js';

Hooks.once('init', async function() {
    console.log('Remote Currency Control | Initializing');

    game.socket.on('module.remote-currency-control', async (data) => {
        if (data.action === 'getCurrency') {
            const currency = await getCurrency(data.actorId);
            game.socket.emit('module.remote-currency-control', {
                action: 'currencyResponse',
                currency: currency,
                requestId: data.requestId
            });
        } else if (data.action === 'updateCurrency') {
            await updateCurrency(data.actorId, data.currency);
        }
    });
});
