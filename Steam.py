import discord
import os
from discord.ext import commands
from discord.ui import Select, View, Button

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.environ.get('DISCORD_BOT_TOKEN') # Token'ı Railway değişkenlerinden çeker

# Senin Discord ID'n (DM bildirimi için)
MY_ID = 123456789012345678 

# Oyun Listesi
GAMES = [
    "Call of Duty: Modern Warfare", "Cyberpunk 2077", "Detroit: Become Human",
    "Dying Light", "EA SPORTS FC 25", "Elden Ring", "Frostpunk", "God of War",
    "God of War Ragnarök", "Marvel’s Spider-Man: Miles Morales", "Resident Evil Village",
    "Resident Evil 4", "Red Dead Redemption 2", "Rise of the Tomb Raider",
    "Shadow of the Tomb Raider", "Sons of the Forest", "The Last of Us part 1",
    "The Last of Us part 2", "The Witcher 3: Wild Hunt", "Tomb Raider"
]

# --- Arayüz Sınıfları ---

class GameSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=game) for game in GAMES]
        super().__init__(placeholder="Satın almak istediğin oyunu seç...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # 1. Kullanıcıya özel bekleme mesajı
        await interaction.response.send_message("✅ Seçiminiz alındı! Satıcı aktif olana kadar bekleyin, size ulaşacaktır.", ephemeral=True)
        
        # 2. Sana DM atma işlemi
        owner = await interaction.client.fetch_user(MY_ID)
        if owner:
            embed = discord.Embed(title="🛒 Yeni Satış Talebi!", color=discord.Color.gold())
            embed.add_field(name="👤 Kullanıcı", value=f"{interaction.user} ({interaction.user.mention})", inline=False)
            embed.add_field(name="🎮 Seçilen Oyun", value=self.values[0], inline=False)
            embed.set_footer(text="İletişime geçmek için aşağıdaki butonu kullanın.")
            
            # DM içine buton ekleme
            view = View()
            view.add_item(Button(label="Kullanıcıya Mesaj At", url=f"https://discord.com/users/{interaction.user.id}"))
            
            await owner.send(embed=embed, view=view)

class GameView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GameSelect())

# --- Bot Olayları ve Komutlar ---

@bot.event
async def on_ready():
    print(f"Bot Hazır: {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def oyunlar(ctx):
    """Kanalda oyun seçim menüsünü başlatır."""
    embed = discord.Embed(
        title="Oyun Satın Alma Listesi",
        description="Aşağıdaki menüden almak istediğiniz oyunu seçin. Satıcı en kısa sürede sizinle iletişime geçecektir.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=GameView())
    await ctx.message.delete() # Komut mesajını temizler

# --- BOTU BAŞLATMA ---
if __name__ == "__main__":
    bot.run(TOKEN)