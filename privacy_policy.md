# プライバシーポリシー（ことねちゃんbot）

> [!Note]
> An English version of this privacy policy can be found [later in the text](#privacy-policy-for-kotone-chan-(ことねちゃんbot)).

## はじめに

ことねちゃんbot（以下、「当アプリ」）は、利用者のお客様の個人情報について以下のプライバシーポリシーを定めます。
本ポリシーは、当アプリがお客様のデータを収集する方法と用途、およびお客様のデータを安全に管理する方法について説明するものです。

## 個人情報

当アプリをご利用になる際、お客様の以下の情報を収集いたします：

* **アカウント情報**：お客様のDiscordユーザーIDやユーザー名、およびDiscordに公開されたアカウント情報を収集します。
    - 当アプリが正常にコマンドに反応するには、お客様のアカウント情報が必要になります。

* **サーバー情報**：お客様の所属するサーバーのチャンネルID、チャンネル名、チャンネル設定や、
  その他お客様やサーバーのモデレーターによって許可された内容を収集します。
    - 当アプリはチャンネル情報からメッセージの宛先を取得しているため、サーバーに関する情報を収集する必要があります。

* **入力データ**：お客様やサーバーのモデレーターに許可された場合、チャンネルに送信されたメッセージを収集します。
    - コマンド入力を検出し、または入力された内容に対して適切なメッセージを出力するには、お客様に送信されたメッセージを読み込む必要があります。

## 個人情報の第三者提供

当アプリは、サービスの運用にお客様の個人情報を利用しますが、これ以外の目的でお客様の情報を使用したり共有したりすることはありません。
ただし、以下の場合、第三者にお客様の情報を提供することがあります。

* 当アプリは[Render.com](https://render.com)にホスティングされているため、収集した情報はRenderにアクセスされることがあります。
  Render.comのプライバシーポリシーは[こちら](https://render.com/privacy)で確認できます。

* 法律で認められる場合、お客様の個人情報を共有することがあります。

## 情報セキュリティ

当アプリはDiscordに提供されたGateway APIを使用しています。
安全なWebSocketプロトコルを適用しているため、お客様の情報は守られております。

## 情報管理

当アプリはデバッグ目的でコマンド履歴を定期的にログに記録しています。
ただし、ユーザー名や入力プロンプト、無関係のメッセージといったセンシティブなデータを記録することはありません。

当アプリのホスティング先のRender.comは、ログを無期限に保管することを[プライバシーポリシー](https://render.com/privacy#how-we-store-and-protect-your-information)にて記載しています。

## 個人情報を守るには

当アプリをお客様のサーバーに招待する際、アプリ権限を設定することをお勧めいたします。

* **当アプリにセンシティブな情報が漏洩しないよう、当アプリのアクセスできないプライベートチャンネルを適用してください。**
  プライベートチャンネルを適用するには、[こちらの記事](https://support.discord.com/hc/ja/articles/206029707-権限をセットアップするには)をご参照ください。

* **アプリコマンドの権限設定から、コマンドの適用されるチャンネルを制限してください。**
  アプリコマンドを設定するには、[こちらの記事](https://support.discord.com/hc/ja/articles/4644915651095-コマンド権限)をご参照ください。



# Privacy policy for kotone-chan (ことねちゃんbot)

Updated 2024-09-17.

## Introduction

The developers ("we") of kotone-chan ("application") are committed to protecting your privacy.
This privacy policy outlines how and why we collect your data, and how we securely manage your data.

## Personal data

When you use our application, we collect the following information about you:

* **Account information**: This includes your Discord user ID, username, and other public information that Discord provides.
    - *Why do we collect this?* When you use a command or perform an action that triggers a command,
      our application needs to know your username and ID to react.

* **Server information**: This includes your server's channel IDs, channel names, channel settings,
  and other information visible to the application as configured by you or your moderators.
    - *Why do we collect this?* Our application needs information about the channels in your server to know where to send messages.

* **Interaction data**: This includes messages that are sent to channels where the application has permission to read, as configured by you or your moderators.
    - *Why do we collect this?* Our application needs to process messages to know when a command is used.
      The application also needs to process input prompts to provide appropriate outputs.

## Data sharing practice

We use your data solely to keep the application operational.
We neither use nor share your data for purposes unrelated to the application.
We may share your data with outside parties in the following scenarios:

* The application is hosted by [Render.com](https://render.com), which has access to your data seen by the application.
  Render.com has a privacy policy stating how it handles personal information.
  You can read the policy [here](https://render.com/privacy).

* We will share your data if informed by the law.

## Data security

The application uses the Gateway API provided by Discord.
Your personal information is transferred to the application via secure WebSocket connections.

## Data retention

The application regularly logs command history for debugging purposes.
It never logs sensitive information such as usernames, input prompts, and unrelated messages.

Render.com, which hosts the application, retains the log indefinitely as outlined in their [privacy policy](https://render.com/privacy#how-we-store-and-protect-your-information):

> We will retain your information as long as necessary for the purposes outlined in this Privacy Policy,
and for a commercially reasonable time thereafter for backup, archival, fraud prevention or detection, or audit purposes, or as otherwise required by law.

## How you can protect your information

When you invite our application to your server, you can customize permissions to restrict how the application collects your information.

* Use private channels to avoid sending sensitive information to the application.
  You can read Discord's [article](https://support.discord.com/hc/en-us/articles/10543994968087-Channel-Permissions-Settings-101) for help on doing this.

* Set command permissions to restrict where the application can react to application commands.
  You can read Discord's [other article](https://support.discord.com/hc/en-us/articles/4644915651095-Command-Permissions) for help on doing this.
