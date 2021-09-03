# Codex for Sublime Text

This package won't work unless you have an OpenAI API key. If you'd like to use Codex (i.e. `davinci-codex` as opposed to another model), you need an API key that has Codex enabled. To apply for an OpenAI API key go to https://beta.openai.com/

## Instructions

First go to `Preferences > Codex > Codex Settings` and add your API key.

Then, place your cursor where you'd like to generate or highlight one or more regions you'd like to include in the prompt and press `CTRL+\`.

If you've highlighted multiple regions, the generation will be after either the last highlighted block or a cursor (if you've placed one somewhere not next to a highlighted region).
