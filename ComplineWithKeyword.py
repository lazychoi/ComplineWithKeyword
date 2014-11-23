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
			# return word(s) at current line from the beginning. This target will be converted to matches' sentence.
			# line = self.view.line(self.view.sel()[0].begin())
			# return self.view.substr(line)

			# return a word at current position
			cursor = self.view.sel()[0]
			word_region = self.view.word(cursor)
			return self.view.substr(word_region)

		def foo(index):
			# setting replacing position of keyword by sentence in matches. 
			# .begin() indicate position after keyword
			# start indicate position before keyword
			# length is the length of keyword. 
			# begin is the starting position where sentence enters. We can get begin position from length. by ComplineWithKeywordComplete class, the keyword is replaced with sentence.
			if(index > -1):
				for i in range(len(self.view.sel())):
					# Replaced keywords is defined from the start of the line.
					# line = self.view.line(self.view.sel()[i].begin())
					# src = self.view.substr(line)

					# Replaced keywords is a word where a cursor is located
					cursor = self.view.sel()[0]
					word_region = self.view.word(cursor)
					src = self.view.substr(word_region)
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

		# The sentences including target word are saved to matches variable.
		# matches = uniq([self.view.substr(line).lstrip() for line in lines if self.view.substr(line).lstrip().startswith(target)])
		matches = uniq([self.view.substr(line).lstrip() for line in lines if target in self.view.substr(line).lstrip()])

		# if matches are too long, the quick panel don't display whole sentence. The appearently length of the sentence is limited to 70 characters.
		shortmatches = []
		for n in matches:
			shortmatches.append(n[0:70])
		# sublime.active_window().show_quick_panel(matches, foo)
		sublime.active_window().show_quick_panel(shortmatches, foo)


class ComplineWithKeywordCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit, matches, begin, i, index):
		self.view.replace(edit, sublime.Region(begin, self.view.sel()[i].end()), matches[index])