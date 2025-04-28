const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once('ready', () => {
    console.log('Ready! Logged in as ' + client.user.tag);
});

client.login('YOUR_TOKEN_HERE');

// Make sure to replace YOUR_TOKEN_HERE with your Discord bot token.