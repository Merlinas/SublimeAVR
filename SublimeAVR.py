from __future__ import print_function
import os, json, zipfile
import sublime, sublime_plugin

"""
SublimeAVR plug-in for Sublime Text
Copyright (c) 2014 Kim Blomqvist, kblomqvist.github.io

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

PLUGIN_NAME = "SublimeAVR"
PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))

if not sublime.version() or int(sublime.version()) > 3000:
	try:
		from . import gcc, avrgcc, unix
	except:
		from AVR import gcc, avrgcc, unix
else:
	import gcc, avrgcc, unix

class AvrNewProjectCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		self.settings = sublime.load_settings(PLUGIN_NAME + ".sublime-settings")
		self.avrgcc = unix.which("avr-gcc", self.settings.get("path", ""))
		
		if not self.avrgcc:
			print("%s: Could NOT find avr-gcc" % PLUGIN_NAME)
			sublime.status_message("%s: Could NOT find avr-gcc" % PLUGIN_NAME)
			return
		self.settings.set("avr-gcc", self.avrgcc)

		self.pm = PrerequisitiesManager()
		if self.pm.install("SublimeClang") == False:
			return

		# Resolve default workdir for project location
		self.workdir = self.settings.get("workdir", "~")
		if not self.workdir: # Remember to check if empty
			self.workdir = "~"
		self.workdir = os.path.expanduser(self.workdir)
		self.settings.set("workdir", self.workdir)

		# Ask device (MCU)
		self.devices = avrgcc.devices(self.avrgcc)
		self.window.show_quick_panel(self.devices, self.mcu_resolved)

	def mcu_resolved(self, index):
		if index == -1:
			return
		else:
			self.settings.set("mcu", self.devices[index])

		# Ask location
		self.window.show_input_panel(
			"Create/Update project in folder: ",
			self.workdir,
			self.location_resolved,
			None,
			None
		)

	def location_resolved(self, location):
		self.location = location
		self.settings.set("location", location)
		try:
			self.new_project = True
			os.makedirs(location)
		except:
			self.new_project = False
			try:
				with open(location + "/SublimeAVR.sublime-project"):
					dialog = "SublimeAVR project found from \"%s\" ...\n\nDo you want to update it?" % location
			except:
				self.new_project = True
				dialog = "Location \"%s\" already exists ...\n\nStill want to start SublimeAVR project there?" % location
			if not sublime.ok_cancel_dialog(dialog):
				return

		if self.new_project:
			self.templates = []
			self.templates_search_path = os.path.join(PLUGIN_PATH, "templates")
			for f in os.listdir(self.templates_search_path):
				if f.endswith(".zip"):
					template_name = f.replace(".zip", "")
					template_name = template_name.replace("_", " ")
					self.templates.append(template_name)
			if not self.templates:
				print("%s: Cannot find a single tamplate" % PLUGIN_NAME)
				sublime.status_message("%s: Cannot find a single template." % PLUGIN_NAME)

			# Ask template
			self.window.show_quick_panel(self.templates, self.template_resolved)

		else:
			self.process_project_file()

	def template_resolved(self, index):
		if index == -1:
			if os.listdir(self.location) == []:
				# Avoid polluting user's file system with empty folders
				os.rmdir(self.location)
			return

		self.template = os.path.join(self.templates_search_path, self.templates[index].replace(" ", "_") + ".zip")
		try:
			zf = zipfile.ZipFile(self.template)
			zf.extractall(self.location)
			zf.close()
		except:
			print("%S: Could not extract the template '%s'" % (PLUGIN_NAME, self.template))
			return
		self.process_project_file()

	def process_project_file(self):
		projectfile = AVRSublimeProject(self.settings)
		projectfile.save()

		verb = "created" if self.new_project else "updated"
		print("%s: Project %s in '%s'" % (PLUGIN_NAME, verb, self.location))
		sublime.status_message("%s: Project %s in '%s'" % (PLUGIN_NAME, verb, self.location))

class AVRSublimeProject():
	def __init__(self, settings):
		s = settings
		self.settings = settings

		self.version = gcc.version(gcc="avr-gcc", location=s.get("avr-gcc"))

		self.c = ["-std=%s" % s.get("c_std", "c99")]
		self.c.append("-I%s" % os.path.normpath("%s/../avr/include" % self.settings.get("avr-gcc")))
		self.c.append("-I%s" % os.path.normpath("%s/../lib/avr/include" % self.settings.get("avr-gcc"))) # Linux
		self.c.append("-I%s" % os.path.normpath("%s/../lib/gcc/avr/%s/include" % (self.settings.get("avr-gcc"), self.version)))
		self.c.append("-I%s" % os.path.normpath("%s/../lib/gcc/avr/%s/include-fixed" % (self.settings.get("avr-gcc"), self.version)))
		self.c.extend(
			gcc.def2opt(
				gcc.predefs(
					gcc="avr-gcc",
					location=s.get("avr-gcc"),
					flags=[
						self.c[0],
						"-xc",
						"-mmcu=%s" % s.get("mcu"),
						"-O%s" % s.get("optimize", "s")
					]
				),
				undef=True
			)
		)

		self.cpp = ["-std=%s" % s.get("cpp_std", "c++98")]
		self.cpp.append("-I%s" % os.path.normpath("%s/../avr/include" % self.settings.get("avr-gcc")))
		self.cpp.append("-I%s" % os.path.normpath("%s/../lib/avr/include" % self.settings.get("avr-gcc"))) # Linux
		self.cpp.append("-I%s" % os.path.normpath("%s/../lib/gcc/avr/%s/include" % (self.settings.get("avr-gcc"), self.version)))
		self.cpp.append("-I%s" % os.path.normpath("%s/../lib/gcc/avr/%s/include-fixed" % (self.settings.get("avr-gcc"), self.version)))
		self.cpp.extend(
			gcc.def2opt(
				gcc.predefs(
					gcc = "avr-gcc",
					location = s.get("avr-gcc"),
					flags = [
						self.cpp[0],
						"-xc++",
						"-mmcu=%s" % s.get("mcu"),
						"-O%s" % s.get("optimize", "s")
					]
				),
				undef = True
			)
		)

	def save(self):
		try:
			location = self.settings.get("location")
			f = open(location + "/SublimeAVR.sublime-project", 'w+')
		except:
			return False
		try:
			project = json.load(f)
			project["build_systems"]["env"].update(self.template()["build_systems"]["env"])
			project["settings"]["sublimeclang_additional_language_options"].update(self.template()["settings"]["sublimeclang_additional_language_options"])
		except:
			project = self.template()

		# Save SublimeAVR.sublime-project
		f.seek(0)
		f.write(json.dumps(project, sort_keys=False, indent=4))
		f.truncate()
		f.close()
		return True

	def template(self):
		mcu = self.settings.get("mcu")
		c_std = self.settings.get("c_std", "c99")
		cpp_std = self.settings.get("cpp_std", "c++98")

		with open(os.path.join(PLUGIN_PATH, "avrdude_partno.json")) as f:
			dude_parts = json.load(f)

		if mcu in dude_parts:
			dude_flags = "-p " + dude_parts[mcu] + " -c dragon_isp"
		else:
			dude_flags = ""

		template = {
			"build_systems":
			[
				{
					"name": "SublimeAVR",
					"cmd": [
						"make"
					],
					"env": {
						"MMCU": mcu,
						"CSTD": c_std,
						"CXXSTD": cpp_std,
						"AVRDUDE_FLAGS": dude_flags,
					},
					"path": os.environ['PATH'],
					"working_dir": "${project_path}",
					"selector": "source.c, source.c++",
					"variants": [
						{ "cmd": ["make", "re"], "name": "Rebuild" },
						{ "cmd": ["make", "clean"], "name": "Clean" },
						{ "cmd": ["make", "debug"], "name": "Debug" },
						{ "cmd": ["make", "avrdude"], "name": "Run" }, # Ctrl+Shift+B
					]
				}
			],
			"folders":
			[
				{
					"path": "."
				}
			],
			"settings":
			{
				"sublimeclang_enabled": True,
				"sublimeclang_dont_prepend_clang_includes": True,
				"sublimeclang_hide_output_when_empty": True,
				"sublimeclang_worker_threadcount": -1,
				"sublimeclang_show_output_panel": False, # See issue #1
				"sublimeclang_show_status": True,
				"sublimeclang_show_visual_error_marks": True,
				"sublimeclang_options":
				[
					"-Wall",
					"-Wno-deprecated-declarations",
					"-ccc-host-triple", "mips",
					"-include", "${project_path:settings.h}"
				],
				"sublimeclang_add_language_option": True,
				"sublimeclang_additional_language_options":
				{
					"c": self.c,
					"c++": self.cpp
				}
			}
		}

		if self.settings.get("path", ""):
			template['build_systems'][0]['path'] = os.path.normpath(self.settings.get("path")) + os.pathsep + template['build_systems'][0]['path']

		return template

class PrerequisitiesManager():
	def install(self, package):
		if self.is_installed(package):
			return None

		print("%s: Installing the dependency package, %s..." % (PLUGIN_NAME, package), end=" ")
		sublime.status_message("%s: Installing the dependency package, %s..." % (PLUGIN_NAME, package))

		try:
			zf = zipfile.ZipFile(os.path.join(PLUGIN_PATH, "%s.sublime-package" % package))
			zf.extractall(self.install_path(package))
			zf.close()

			if package == "SublimeClang":
				# For convenience sake disable the SublimeClang plug-in by default
				f = open(os.path.join(sublime.packages_path(), "User/%s.sublime-settings" % package), 'w')
				f.write(json.dumps({"enabled": False}, indent=4))
				f.close()

			print("Ok.")
			sublime.status_message("%s: Installing the dependency package, %s... Ok." % (PLUGIN_NAME, package))

		except:
			print("Failed.")
			sublime.status_message("%s: Installing the dependency package, %s... Failed." % (PLUGIN_NAME, package))
			return False

		return True

	def is_installed(self, package):
		if os.path.exists(self.install_path(package)):
			return True
		if os.path.isfile(os.path.join(sublime.installed_packages_path(), "%s.sublime-package" % package)):
			return True
		return False

	def install_path(self, package):
		return os.path.join(sublime.packages_path(), package)
