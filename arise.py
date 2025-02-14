
import disnake
from disnake.ext import commands
import os
import asyncio

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', reload=True, intents=intents,
                   activity=disnake.Activity(name="Counter-Strike 2", type=disnake.ActivityType.playing))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready!")


class AppealModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Имя', style=disnake.TextInputStyle.short, placeholder='Пример: Илья',
                                 required=True, custom_id='**1.Имя**', max_length=100),
            disnake.ui.TextInput(label='Возраст', style=disnake.TextInputStyle.short, placeholder='Пример: 20',
                                 required=True, custom_id='**2.Возраст**', max_length=2),
            disnake.ui.TextInput(label='Профиль на yooma.su', style=disnake.TextInputStyle.short,
                                 placeholder='Пример: https://yooma.su/profile/76561199383005661', required=True,
                                 custom_id='**3.Профиль на yooma.su**',
                                 max_length=200),
            disnake.ui.TextInput(label='Почему', style=disnake.TextInputStyle.paragraph,
                                 placeholder='Пример: У вас крутой Разработчик!!!', required=True,
                                 custom_id='**4.Причина вступления в клан**',
                                 max_length=400),
            disnake.ui.TextInput(label='Кратко о себе', style=disnake.TextInputStyle.paragraph,
                                 placeholder='Пример: Я 10 лвл фейсита!, общительный', required=True,
                                 custom_id='**5.Кратко о себе**',
                                 max_length=400),
        ]
        super().__init__(title="Заявка", components=components, custom_id='appeal_modal')

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        await interaction.response.defer(ephemeral=True)

        profile_link = interaction.text_values['**3.Профиль на yooma.su**']

        embed = disnake.Embed(title="Заявка", color=disnake.Color(0x000000),
                              description=f"Заявка от {interaction.author.mention}")
        embed.set_thumbnail(url=interaction.author.avatar.url)
        for title, resp in interaction.text_values.items():
            ilovefootjob = f"\n```{resp}```\n"
            embed.add_field(name=title, value=ilovefootjob, inline=False)

        channel_id = 1305654259806634004
        try:
            channel = interaction.bot.get_channel(channel_id) or await interaction.bot.fetch_channel(channel_id)
            message = await channel.send(embed=embed)
            await interaction.edit_original_response('Заявка успешно отправлена!')
        except disnake.Forbidden:
            await interaction.edit_original_response('У меня нет доступа к каналу для отправки заявки.')


@bot.command(name='заявка')
async def open_modal(ctx):
    view = disnake.ui.View(timeout=None)
    allowed_channel_id = 1305554826477703209

    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Эта команда недоступна в данном канале.")
        return

    async def modal_callback(interaction):
        if interaction.component.custom_id == "open_modal":
            modal = AppealModal()
            await interaction.response.send_modal(modal)

    button = disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Подать Заявку", custom_id="open_modal")
    button.callback = modal_callback

    view.add_item(button)

    embed = disnake.Embed(
        title="**Заявка в клан**",
        description="**Здравствуйте, уважаемый игрок.\nНажмите на кнопку, чтобы подать заявку в клан!**",
        color=disnake.Color(0x000000) 
    )
    embed.set_footer(text="by carharttz")

    await ctx.send(embed=embed, view=view)


bot.run("TOKEN")
