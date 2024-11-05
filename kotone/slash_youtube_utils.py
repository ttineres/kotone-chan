#
# slash_youtube_utils.py
#
# YouTube API reference: https://developers.google.com/youtube/v3/docs
#


import discord
from discord.ext import commands
from discord.ui import View, Button
import googleapiclient.discovery
import os
from dotenv import load_dotenv

from .util_emoji import KOTONE_EMOJI, IDOL_EMOJI
from .util_chara_name import KOTONE_NICKNAME_OF


# Retrieve API key from environment variable
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube channel ID of Hatsuboshi Gakuen (初星学園)
HATSUBOSHI_CHANNEL_ID = "UC2dXx-3RXeeP8hA5AGt8vuw"
HATSUBOSHI_PLAYLIST_ID = "PL8AmPgz38WkXIiEnqf-Q5XkWpQgm5UiuF"

# YouTube API client setup
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


class YouTubeUtilsCog(commands.Cog):
    """ A cog for YouTube-related commands. """
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(
        name="hatsuboshi",
        description="初星学園公式YouTubeの楽曲や動画を表示する"
    )
    @discord.app_commands.rename(media_type="種類")
    @discord.app_commands.choices(media_type=[
        discord.app_commands.Choice(name="最新楽曲", value="any"),
        discord.app_commands.Choice(name="最新動画", value="video"),
        discord.app_commands.Choice(name="花海咲季", value="Saki Hanami"),
        discord.app_commands.Choice(name="月村手毬", value="Temari Tsukimura"),
        discord.app_commands.Choice(name="藤田ことね", value="Kotone Fujita"),
        discord.app_commands.Choice(name="有村麻央", value="Mao Arimura"),
        discord.app_commands.Choice(name="葛城リーリヤ", value="Lilja Katsuragi"),
        discord.app_commands.Choice(name="倉本千奈", value="China Kuramoto"),
        discord.app_commands.Choice(name="紫雲清夏", value="Sumika Shiun"),
        discord.app_commands.Choice(name="篠澤広", value="Hiro Shinosawa"),
        discord.app_commands.Choice(name="花海佑芽", value="Ume Hanami"),
        #discord.app_commands.Choice(name="秦谷美鈴", value="Misuzu Hataya"),
        #discord.app_commands.Choice(name="十王星南", value="Sena Juou"),
        discord.app_commands.Choice(name="姫崎莉波", value="Rinami Himesaki"),
    ])
    async def hatsuboshi(
        self,
        interaction: discord.Interaction,
        media_type: discord.app_commands.Choice[str] = None,
    ):
        """ Displays the latest media from Hatsuboshi Gakuen.
            If value=="any", retrieve the most recent songs and videos.
            If value=="video", retrieve the most recent videos.
            Otherwise, retrieve all media related to character specified by value.
        """
        if not media_type:
            await interaction.response.send_message(
                "[初星学園](https://www.youtube.com/@hatsuboshi_gakuen)の楽曲ですか？\n"
                "持ってきますよ！　どれにしますか？\n",
                view=MediaTypeView(),
                ephemeral=True
            )
            return
        match media_type.value:
            case "any":
                message = get_latest_music()
            case "video":
                message = get_latest_videos()
            case _:
                chara_name = media_type.value
                message = get_music(chara_name)

        await interaction.response.send_message(message, ephemeral=True, suppress_embeds=True)


class MediaTypeView(View):
    """ A UI View for /hatsuboshi command. """
    @discord.ui.button(label="最新楽曲", style=discord.ButtonStyle.green, row=0)
    async def latest_music_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_latest_music(),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="最新動画", style=discord.ButtonStyle.blurple, row=0)
    async def latest_videos_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_latest_videos(),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="花海咲季", emoji=IDOL_EMOJI["saki1"], style=discord.ButtonStyle.grey, row=1)
    async def saki_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Saki Hanami"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="月村手毬", emoji=IDOL_EMOJI["temari1"], style=discord.ButtonStyle.grey, row=1)
    async def temari_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Temari Tsukimura"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="藤田ことね", emoji=IDOL_EMOJI["kotone1"], style=discord.ButtonStyle.grey, row=1)
    async def kotone_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Kotone Fujita"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="有村麻央", emoji=IDOL_EMOJI["mao1"], style=discord.ButtonStyle.grey, row=2)
    async def mao_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Mao Arimura"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="葛城リーリヤ", emoji=IDOL_EMOJI["lilja1"], style=discord.ButtonStyle.grey, row=2)
    async def lilja_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Lilja Katsuragi"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="倉本千奈", emoji=IDOL_EMOJI["china1"], style=discord.ButtonStyle.grey, row=2)
    async def china_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("China Kuramoto"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="紫雲清夏", emoji=IDOL_EMOJI["sumika1"], style=discord.ButtonStyle.grey, row=3)
    async def sumika_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Sumika Shiun"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="篠澤広", emoji=IDOL_EMOJI["hiro1"], style=discord.ButtonStyle.grey, row=3)
    async def hiro_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Hiro Shinosawa"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="花海佑芽", emoji=IDOL_EMOJI["ume1"], style=discord.ButtonStyle.grey, row=3)
    async def ume_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Ume Hanami"),
            ephemeral=True,
            suppress_embeds=True,
        )
    
    @discord.ui.button(label="姫崎莉波", emoji=IDOL_EMOJI["rinami1"], style=discord.ButtonStyle.grey, row=4)
    async def rinami_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            get_music("Rinami Himesaki"),
            ephemeral=True,
            suppress_embeds=True,
        )
    

async def setup(bot: discord):
    await bot.add_cog(YouTubeUtilsCog(bot))


#
# Helper functions
#


def get_latest_music(num_music=5):
    """ Returns a message string displaying the latest music from Hatsuboshi Gakuen.
        The number of music is specified by num_music.
    """
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=HATSUBOSHI_PLAYLIST_ID,
        maxResults=num_music,
    )
    response = request.execute()
    message = f"初星学園の最新楽曲はこちら！{ KOTONE_EMOJI["kotone2"] }\n"
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={ video_id }"
        message += f"* [{ title }]({ video_url })\n"
    return message


def get_latest_videos(num_videos=5):
    """ Returns a message string displaying the latest videos from Hatsuboshi Gakuen.
        The number of videos is specified by num_videos.
    """
    request = youtube.search().list(
        part="snippet",
        channelId=HATSUBOSHI_CHANNEL_ID,
        order="date",
        maxResults=num_videos,
        type="video",
    )
    response = request.execute()
    message = f"初星学園の最新動画はこちら！{ KOTONE_EMOJI["kotone2"] }\n"
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={ video_id }"
        message += f"* [{ title }]({ video_url })\n"
    return message


def get_music(chara_name):
    """ Returns a message string that displays every music of specified character. """
    page_token = None
    music_list = []
    # Keep fetching results until there is no nextPageToken
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=HATSUBOSHI_PLAYLIST_ID,
            maxResults=50,
            pageToken=page_token,
        )
        response = request.execute()
        music_list += response["items"]
        if "nextPageToken" in response.keys():
            page_token = response["nextPageToken"]
        else:
            break

    message = (
        "こちらが、"
        f"{ KOTONE_NICKNAME_OF[chara_name] }"
        f"{ IDOL_EMOJI[ chara_name.split()[0].lower() + "_hlw" ] }"
        "の楽曲一覧でーす！\n"
    )
    for item in music_list:
        # Add to message if the character is involved in this music
        if chara_name in item["snippet"]["description"]:
            title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={ video_id }"
            message += f"* [{ title }]({ video_url })\n"
    return message
