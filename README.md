# Codex for Sublime Text

This is a package that lets you use OpenAI Codex in Sublime Text. To use it, you need to have access to OpenAI's Codex API.

## Manual Installation

Open Sublime Text and go to `Preferences > Browse Packages...` to get to the Sublime packages folder, and `git clone` this repo into the folder. Rename it from `sublime-codex` to `Codex`.

## Usage

First go to `Preferences > Codex > Codex Settings` and add your API key.

Then, place your cursor where you'd like to generate code or highlight one or more regions you'd like to include in the prompt and press `CTRL+\`.

If you've highlighted multiple regions, the generation will be after either the last highlighted block or a cursor (if you've placed one somewhere not next to a highlighted region).


