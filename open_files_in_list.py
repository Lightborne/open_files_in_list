import sublime
import sublime_plugin
from os.path import isfile
from os.path import abspath

class OpenFilesInListCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Active sheet is assumed to be file list
        file_list_sheet = self.window.active_sheet()
        file_list_view = file_list_sheet.view()

        # Contents of view is list of files
        file_list_regions = file_list_view.split_by_newlines(sublime.Region(0, file_list_view.size()))

        # Process each region
        not_found = []
        for region in file_list_regions:
            # Check that we're not processing a blank line
            if (region.size() == 0):
                continue

            # If the file doesn't exist, keep the region around to highlight later
            path = abspath(file_list_view.substr(region))
            if (not isfile(path)):
                not_found.append(region)
                continue

            # Should be able to open it now
            self.window.open_file(path)

        # Highlight those not found
        file_list_view.add_regions("not_found", not_found, "invalid")

        # Refocus on file list sheet
        self.window.focus_sheet(file_list_sheet)
