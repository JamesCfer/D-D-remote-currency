export async function getCurrency(actorId) {
    const actor = game.actors.get(actorId);
    if (!actor) return null;

    const currency = actor.data.data.currency;
    return currency;
}

export async function updateCurrency(actorId, newCurrency) {
    const actor = game.actors.get(actorId);
    if (!actor) return;

    await actor.update({'data.currency': newCurrency});
}