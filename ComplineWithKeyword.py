import sublime, sublime_plugin, re

class ComplineWithKeywordCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		def uniq(seq): 
			checked = []
			for e in seq:
				if e.strip() not in checked:
					checked.append(e)
			return checked
		
		def target():
			# return text at current position. This target is converted to matches' sentence.
			line = self.view.line(self.view.sel()[0].begin())
			return self.view.substr(line)

		def foo(index):
			if(index > -1):
				for i in range(len(self.view.sel())):
					line = self.view.line(self.view.sel()[i].begin())
					src = self.view.substr(line)
					match = re.search(r"$", src)
					if(match):
						end = match.end()
						match = re.search(r"\S", src)
						if(match):
							start = match.start()
						else:
							start = self.view.sel()[i].begin()
							end = line.end()
						length = end - start
						begin = self.view.sel()[i].begin()-length
						self.view.run_command("compline_with_keyword_complete",{"matches": matches, "i": i, "begin": begin, "index": index})
		# whole text
		region = sublime.Region(0, self.view.size())
		lines = self.view.lines(region)
		# text at current position
		target = target().strip()
		# The sentences including target are saved to matches variable.
		# matches = uniq([self.view.substr(line).lstrip() for line in lines if self.view.substr(line).lstrip().startswith(target)])
		matches = uniq([self.view.substr(line).lstrip() for line in lines if target in self.view.substr(line).lstrip()])
		# if matches are too long, the quick panel 
		shortmatches = []
		for n in matches:
			shortmatches.append(n[0:70])
		# sublime.active_window().show_quick_panel(matches, foo)
		sublime.active_window().show_quick_panel(shortmatches, foo)


class ComplineWithKeywordCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit, matches, begin, i, index):
		self.view.replace(edit, sublime.Region(begin, self.view.sel()[i].end()), matches[index])

