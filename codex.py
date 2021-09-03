import sublime
import sublime_plugin

import subprocess
import json


class CodexCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        pass

    def run(self, edit):
        # Get settings every API call so that changes to Codex.sublime-settings are automatically used
        # without needing to reload codex.py
        settings = sublime.load_settings("Codex.sublime-settings")
        max_tokens = settings.get("max_tokens")
        engine = settings.get("engine")
        api_key = settings.get("openai_api_key")
        
        if api_key == "<Your OpenAI API key should go here!>":
            sublime.error_message("""Make sure to put your OpenAI API Key in Codex.sublime-settings
Go to `Preferences > Package Settings > Codex > Codex Settings`""")
            return

        # Get sublime selections (highlighted regions and cursor positions)
        sels = self.view.sel()

        # get output_idx and prompt
        if len(sels) == 0:
            sublime.error_message('You need to place your cursor or highlight a selection of text.')
            return
        elif len(sels) > 1:
            prompt = ""
            cursorSeen = False
            output_idx = 0
            for sel in sels:
                if sel.a == sel.b:
                    output_idx = sel.b
                    if cursorSeen:
                        sublime.error_message("""Error: you may place at most one cursor not next to a highlighted region. (you can only generate text from one position)""")
                        return
                    cursorSeen = True
                if not cursorSeen:
                    output_idx = max([sel.a, sel.b, output_idx])
                prompt += self.view.substr(sel)
        elif len(sels) == 1:
            if sels[0].a == sels[0].b:
                sel = sublime.Region(0, sels[0].b)
            else:
                sel = sels[0]
            prompt = self.view.substr(sel)
            output_idx = max([sel.a, sel.b])# index to insert codex output
        
        

        self.view.set_status('codex', 'Waiting for a response...')

        data = json.dumps({
            'prompt': prompt,
            'max_tokens': max_tokens
            })
        proc = subprocess.Popen(["curl", "https://api.openai.com/v1/engines/"+engine+"/completions", "-H", "Content-Type: application/json", "-H", "Authorization: Bearer "+api_key, "-d", data], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()

        self.view.erase_status('codex')
        sublime.status_message('Codex successfully run.')

        response = json.loads(out.decode("utf-8"))
        
        if 'error' in response:
            sublime.error_message('OpenAI API error message: '+response['error']['message'])
        output_str = response['choices'][0]['text']

        # Insert text
        self.view.insert(edit, output_idx, output_str)
        
        # Clear selections and highlight newly-generated text
        sels.clear()
        gen_region = sublime.Region(output_idx, output_idx+len(output_str))
        sels.add(gen_region)