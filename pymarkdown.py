import sys, subprocess
import sublime
import sublime_plugin


class RunCodeBlockCommand(sublime_plugin.TextCommand):

    def is_visible(self):
        return is_code_block_selected(self.view)
    
    def run(self, edit):
        for region in self.view.sel():
            code_block = code_block_at_point(region.begin(), self.view)
            if code_block is None:
                continue
            stdout, stderr = run_code_block(code_block)
            fence_region = self.view.find('```', region.begin())
            if stderr:
                stderr = '\n' + stderr
                self.view.insert(edit, fence_region.end(), stderr)
                return
            if stdout:
                stdout = '\n' + stdout
                self.view.insert(edit, fence_region.end(), stdout)


def is_code_block_selected(view):
    result = False
    for region in view.sel():
        if view.match_selector(region.begin(), 'source.python'):
            result = True
    return result


def code_block_at_point(point, view):
    for region in find_code_block_regions(view):
        if region.contains(point):
            return view.substr(region)


def run_code_block(code_block):
    proc = subprocess.Popen(
        sys.executable,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return proc.communicate(code_block)


def find_code_block_regions(view):
    return view.find_by_selector('source.python')
