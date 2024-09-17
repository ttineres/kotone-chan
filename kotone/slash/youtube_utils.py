#
# slash/youtube_utils.py
#
# YouTube API reference: https://developers.google.com/youtube/v3/docs
#

import discord
import googleapiclient.discovery
import os
from dotenv import load_dotenv

from utils.emoji import KOTONE_EMOJI, IDOL_EMOJI
from utils.chara_name import KOTONE_NICKNAME_OF


# Retrieve API key from environment variable
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube channel ID of Hatsuboshi Gakuen (初星学園)
HATSUBOSHI_CHANNEL_ID = "UC2dXx-3RXeeP8hA5AGt8vuw"
HATSUBOSHI_PLAYLIST_ID = "PL8AmPgz38WkXIiEnqf-Q5XkWpQgm5UiuF"

# YouTube API client setup
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

async def setup(bot: discord):
    @bot.tree.command(
        name="hatsuboshi",
        description="初星学園公式YouTubeの楽曲や動画を表示する"
    )
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
                "このコマンド`/hatsuboshi`を使うと、[初星学園](https://www.youtube.com/@hatsuboshi_gakuen)の最新楽曲が表示されますよ！\n"
                "また、アイドルを指定すれば特定の楽曲のみ表示されまーす！\n"
                f"まずは`/hatsuboshi media_type:最新楽曲`を使ってみよーね{ KOTONE_EMOJI["KOTONE_2"] }",
                ephemeral=True
            )
            return
        match media_type.value:
            case "any":
                message = get_latest_music()
            case "video":
                message = get_latest_videos()
            case _:
                message = get_music(media_type.value)

        await interaction.response.send_message(message, ephemeral=True, suppress_embeds=True)


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
    message = f"初星学園の最新楽曲はこちら！{ KOTONE_EMOJI["KOTONE_2"] }\n"
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
    message = f"初星学園の最新動画はこちら！{ KOTONE_EMOJI["KOTONE_2"] }\n"
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
        f"{ IDOL_EMOJI[ chara_name.split()[0].upper() + "_2" ] }"
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
