from cProfile import label

from dotenv import load_dotenv
import disnake
from disnake.ext import commands
from disnake.ui import Button, View, Modal, TextInput
from disnake import ButtonStyle, ApplicationCommandInteraction, ModalInteraction
import os
from item_lookup import lookup_item, get_item_name
from api_functions import get_crafting_requirements


load_dotenv()

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong')


# 1st modal weapon:
# Weapon = text input
# weapon tier 4.0 -- 4.4, 5.0, -- 5.4 -> 8.4 = dropdown

# 2nd modal market price (only ask for input on what it's made of):
# price of each component

#

class WeaponModal(Modal):
    def __init__(self):
        components = [
            TextInput(label="Item to craft", placeholder="e.g. bearpaws", custom_id="item"),
            TextInput(label="Tier", placeholder="e.g. 4.4", custom_id="tier")
        ]

        super().__init__(title="Select an Item", components=components)

    async def callback(self, interaction: ModalInteraction):
        item = interaction.text_values["item"]
        tier = interaction.text_values["tier"]
        items = lookup_item(item, tier)
        if len(items) == 0:
            await interaction.response.send_message(f"No items found for {item} at tier {tier}")
        else:
            resources = get_crafting_requirements(items[0])
            resource_str = ""
            for resource in resources:
                if 'ARTEFACT' in resource['uniqueName']:
                    split_item = items[0].split('_')
                    split_item.insert(1, 'ARTEFACT')
                    resource['uniqueName'] = '_'.join(split_item)
                resource_str += f"{get_item_name(resource['uniqueName'])}: {resource['count']}\n"
            await interaction.response.send_message(f"You selected {interaction.text_values['item']} at tier {tier}\n{resource_str}")


# async def get_item_input(inter: ApplicationCommandInteraction):


@bot.slash_command()
async def calculate(inter: ApplicationCommandInteraction):
    button = Button(label="Start Calculation", style=ButtonStyle.green)

    async def button_callback(interaction: ApplicationCommandInteraction):
        modal = WeaponModal()
        await interaction.response.send_modal(modal)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    await inter.response.send_message("Lets calculate crafting costs and profits!", view=view)



bot.run(os.getenv('DISCORD_TOKEN'))