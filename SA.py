
# IMPORTS
from __future__ import division
import os, sys, platform, commands
from distutils.sysconfig import get_python_lib
import gtk, pygtk, gobject
pygtk.require('2.0')
import shutil
import fnmatch
import webbrowser, urllib, urllib2
from HTMLParser import HTMLParser
import random
import time
import zipfile, tarfile
import threading, multiprocessing, subprocess
import gettext, locale
import Source.Src
_ = gettext.gettext

try: from PIL import ImageOps, Image
except: pass



# VARIABLES

ScriptDir=os.path.dirname(os.path.realpath(__file__))
Home=os.path.expanduser('~')
ConfDir = os.path.join(Home, ".SA")
MyFile = os.path.basename(__file__)
FullFile = os.path.abspath(os.path.join(ScriptDir, "SA.py"))
Cores = str(multiprocessing.cpu_count())
Python = os.path.abspath(sys.executable)
PythonDir = os.path.dirname(Python)


# OS Determination

if sys.platform == 'linux2':
	OS = 'Lin'
elif sys.platform == 'win32':
	OS = 'Win'
elif sys.platform == 'win64':
	OS = 'Win'
elif sys.platform == 'darwin':
	OS = 'Mac'
else:
	OS = 'Default'

if (sys.maxsize > 2**32) == True: bit = 64
else: bit = 32

PATH = []
if OS == "WIN": sep = ";"
else: sep = ":"
for x in str(os.environ["PATH"]).split(sep): PATH.append(x)


# Choose language


if not os.path.exists(os.path.join(ConfDir, "Language")):
	def delete_event(self, widget, event, data=None):
		exit()
		return False
	def PickLanguage(cmd):
		f = open(os.path.join(Home, ".SA", "Language"), "w")
		f.flush()
		if FrBtn.get_active(): f.write("fr_FR")
		elif EnBtn.get_active(): f.write("en_US")
		elif ItBtn.get_active(): f.write("it_IT")
		elif NlBtn.get_active(): f.write("nl_NL")
		else: 
			active = [r for r in FrBtn.get_group() if r.get_active()][0].get_label()
			f.write(active)
		f.flush()
		window2.destroy()
		os.execl(sys.executable, sys.executable, * sys.argv)
	if not os.path.exists(os.path.join(Home, ".SA")):
		os.makedirs(ConfDir)
	window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window2.set_position(gtk.WIN_POS_MOUSE)
	window2.set_resizable(False)
	window2.connect("delete_event", delete_event, 0)
	window2.set_title("Choose language")
	vbox = gtk.VBox(False, 0)
	window2.add(vbox)
	EnBtn = gtk.RadioButton(None, "English")
	FrBtn = gtk.RadioButton(EnBtn, "Francais")
	ItBtn = gtk.RadioButton(FrBtn, "Italiano")
	NlBtn = gtk.RadioButton(FrBtn, "Nederlands")
	RoBtn = gtk.RadioButton(FrBtn, "Romanian")
	NewLang = []
	for langd in os.listdir(os.path.join(ScriptDir, "lang")):
		if not "fr" in langd and not "en" in langd and not "it" in langd and not "nl" in langd and not "ro" in langd:
			NewBtn = gtk.RadioButton(FrBtn, langd)
			vbox.pack_start(NewBtn)
			NewLang.append(langd)
	vbox.pack_start(EnBtn)
	vbox.pack_start(FrBtn)
	vbox.pack_start(ItBtn)
	vbox.pack_start(NlBtn)
	
	ChooseBtn = gtk.Button("")
	vbox.pack_start(ChooseBtn)
	ChooseBtn.connect("clicked", PickLanguage)
	window2.show_all()
	gtk.main()
	while 1:
		time.sleep(1)

# APPLY LANGUAGE

DIR = os.path.join(ScriptDir, "lang")
APP = 'SA'
gettext.textdomain(APP)
gettext.bindtextdomain(APP, DIR)
gettext.bind_textdomain_codeset("default", 'UTF-8')
locale.setlocale(locale.LC_ALL, "")
Language = open(os.path.join(Home, ".SA", "Language"), "r").read()
LANG = Language


lang = gettext.translation(APP, DIR, languages=[LANG], fallback = True)
_ = lang.gettext
	


# Double output
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(os.path.join(ScriptDir, "log"), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
	self.log.flush()

sys.stdout = Logger()

# Debug

if os.path.exists(os.path.join(ConfDir, "debug")):
	Debug = True
	bug = "ON"
else:
	Debug = False
	bug = "OFF"

# External Output redirection

def SystemLog(cmd):
	if Debug == True:
		print(cmd)
		print(commands.getoutput(cmd))
	elif Debug == False:
		os.system(cmd)



# GTK TOOLS

def delete_event(self, widget, event, data=None):
	gtk.main_quit()
	return False

def destroy(self, widget, data=None):
	gtk.main_quit()

def Restart(cmd):
	python = sys.executable
	os.execl(python, python, * sys.argv)

def DebugOn(cmd):
	f = open(os.path.join(ConfDir, "debug"), "w")
	f.close()
	Restart("cmd")

# Shotcuts 

sz = os.path.join(ScriptDir, "Utils", "7za")
UtilDir = os.path.join(ScriptDir, "Utils")
SourceDir = os.path.join(ScriptDir, "Source")
ApkJar = os.path.join(ScriptDir, "Utils", "apktool.jar")
aapt = os.path.join(ScriptDir, "Utils", "aapt")
adb = os.path.join(ScriptDir, "Utils", "adb")
SignJar = os.path.join(ScriptDir, "Utils", "signapk.jar")
ZipalignFile = os.path.join(ScriptDir, "Utils", "zipalign")
SmaliJar = os.path.join(ScriptDir, "Utils", "smali-1.3.2.jar")
BaksmaliJar = os.path.join(ScriptDir, "Utils", "baksmali-1.3.2.jar")
OptPng = os.path.join(ScriptDir, "Utils", "optipng")
Web = webbrowser.get()
GovDir = os.path.join(UtilDir, "Gov")


# MAC OSX Fix
def ExZip(zipf, expath, type='zip'):
	if type == 'zip':
		Zip = zipfile.ZipFile(zipf, "r")
		namelist = Zip.namelist()
	else:
		Zip = tarfile.open(zipf, "r")
		namelist = Zip.getnames()
	for f in namelist:
		if f.endswith('/'):
			if not os.path.exists(os.path.join(expath, f)):os.makedirs(os.path.join(expath, f))
		else: 
			try:Zip.extract(f, path=expath)
			except IOError: 
				os.remove(os.path.join(expath, f))
				Zip.extract(f, path=expath)

# EXTRACT UTILS.ZIP AND REMOVE UNNECESSARY FILES
#ExZip(os.path.join(ScriptDir, "Utils.zip"), ScriptDir)

for dep in [aapt, adb, ZipalignFile, sz]:
	if OS == "Win":
		if os.path.exists(dep):
			os.remove(dep)
		dep = dep + ".exe"
	else:
		if os.path.exists(dep + ".exe"):
			os.remove(dep + ".exe")


def callback(widget, option):
	# REDIRECTS THE BUTTON OPTION TO A FUNCTION
	try: globals()[option]
	except KeyError: print _("%s is not defined yet, SORRY!" % option)
	else: 
		#threading.Thread(None, globals()[option]).start()
		globals()[option]()

# New dialog

def NewDialog(Title, Text):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_markup("<b>%s</b>" % Title)
	dialog.format_secondary_markup("%s" % Text)
	dialog.run()
	dialog.destroy()

def KillPage(cmd, child):
	notebook = MainApp.notebook
	page = notebook.page_num(child)
	if page == -1:
		page = notebook.get_n_pages() - 1
	notebook.remove_page(page)
	child.destroy()
	notebook.set_current_page(notebook.get_n_pages() - 1)

# Basic AddToList

def AddToList(cmd, List, name, NameBtn, Single=False):
	if Single==False:
		if not name in List:
			List.append(name)
		if not NameBtn.get_active():
			List.remove(name)

def DirChoose(DirChooser, filtern=None):
	if not filtern == None:
		filter = gtk.FileFilter()
		filter.set_name(filtern)
		filter.add_mime_type(filtern)
		filter.add_pattern("*" + filtern)
		DirChooser.add_filter(filter)
	DirChooser.set_select_multiple(False)
	DirChooser.set_current_folder(ScriptDir)
	response = DirChooser.run()
	if response == gtk.RESPONSE_OK:
		Chosen = DirChooser.get_filename()
	DirChooser.hide()
	return Chosen

def FileChoose(FileChooser, filtern=None, multiple=False):
	if not filtern == None:
		filter = gtk.FileFilter()
		filter.set_name(filtern)
		filter.add_mime_type(filtern)
		filter.add_pattern("*" + filtern)
		FileChooser.add_filter(filter)
	FileChooser.set_select_multiple(multiple)
	FileChooser.set_current_folder(ScriptDir)
	response = FileChooser.run()
	FileChooser.hide()
	if response == gtk.RESPONSE_OK:
		Chosen = FileChooser.get_filename()
		return Chosen

def GetFile(cmd, FileChooser, BtnChange=False, Multi=False, filtern=None):
	Returned = FileChoose(FileChooser, filtern, Multi)
	if not BtnChange == False:
		Btn = BtnChange[0]
		label = str(Btn.get_label()).split(" :")[0]
		Btn.set_label("%s : %s" %(label, Returned))
	MainApp.Out = Returned

def YesNo(Title, Text):
	dialog = gtk.Dialog(Title,
		           None,
		           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		           (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	label = gtk.Label(Text)
	dialog.vbox.pack_start(label)
	label.show()
	response = dialog.run()
	dialog.hide_all()
	dialog.destroy()
	return ['1', '0', 'error'][response]


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def remove_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor
# (C) ActivateState


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
# FindFiles (C) StackOverflow


def NewPage(Label, parent):
	box = gtk.HBox()
	label = gtk.Label(Label)
	closebtn = gtk.Button()
	image = gtk.Image()
	image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
	closebtn.connect("clicked", KillPage, parent)
	closebtn.set_image(image)
	closebtn.set_relief(gtk.RELIEF_NONE)
	box.pack_start(label, False, False)
	box.pack_end(closebtn, False, False)
	box.show_all()
	return box

for DIRS in [["APK", "IN"], ["APK", "OUT"], ["APK", "EX"], ["APK", "DEC"], ["Resize"], ["Advance", "Smali", "IN"], ["Advance", "Smali", "Smali"], ["Advance", "Smali", "OUT"], ["Advance", "ODEX", "IN"], ["Advance", "ODEX", "CURRENT"], ["Advance", "ODEX", "WORKING"], ["Advance", "ODEX", "OUT"], ["Advance", "PORT", "TO"], ["Advance", "PORT", "ROM"], ["Advance", "PORT", "WORKING"], ['ADB']]:
	try:
		subdir = ''
		for x in DIRS:
			subdir = os.path.join(subdir, x)
		dir = os.path.join(ScriptDir, subdir)
		os.makedirs(dir)
	except:
		pass

# FIX PERMISSIONS
if not OS == "Win":
	for filen in find_files(UtilDir, "*"):
		os.chmod(filen, 0755)
	os.chmod(os.path.join(SourceDir, "Build.sh"), 0755)
else:
	if " " in ScriptDir:
		print _("You extracted StudioAndroid to a path with spaces!\nPlease move it somewhere without spaces.")
		exit()
	# ADD PYTHON AND UTILS TO THE PATH
	if not UtilDir in PATH:
		SystemLog('PATH %s;%s;' % (UtilDir, PythonDir) + r'%path%')


if not os.path.exists(os.path.join(Home, ".SA", "ran")):
	FirstRun = True
	NewDialog( _("First Run"), _("Hi there! It seems this is your first time to run StudioAndroid!\nPlease note this tool still has a long way to go,\n and I need testers and reporters...\n So please publish your LOG!") )
	open(os.path.join(Home, ".SA", "ran"), "w").flush()
else:
	FirstRun = False

# DEFINE WINDOW


window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title("StudioAndroid")
window.connect("delete_event", delete_event, 0)
window.set_border_width(15)
window.set_size_request(750,500)
window.set_resizable(False)
window.set_position(gtk.WIN_POS_CENTER)

vbox = gtk.VBox(False, 5)
hbox = gtk.HBox(False, 5)


# PRINT INFO

Weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
Weekday = Weekdays[time.localtime()[6]]
Month = Months[time.localtime()[1]]

def date():
	date = "%s-%s-%s--%s.%s.%s" %(time.localtime()[0], time.localtime()[1], time.localtime()[2], time.localtime()[3], time.localtime()[4], time.localtime()[5])
	return date


print("### %s %s %s - %s.%s.%s ###" %(Weekday, time.localtime()[2], Month, time.localtime()[3], time.localtime()[4], time.localtime()[5]) )
print _("OS = %s %s-bit" %(OS, bit))
print _("PythonDir = %s" %(PythonDir))
print _("Cores = %s" %(Cores))
print _("Home = %s" %(Home))
print _("ScriptDir = %s" %(ScriptDir))
print _("File = %s" %(MyFile))
print ("Debug = %s" %(bug))
print _("Language = %s" %(Language))



class MainApp():

	# MAIN APP

	placeIcon = gtk.gdk.pixbuf_new_from_file(os.path.join(ScriptDir, "images", "icon.png"))
	window.set_icon(placeIcon)

	#
	# MAIN TABLE
	#

	global menu

	vbox = gtk.VBox()

	menu = gtk.MenuBar()
	OptionsMenu = gtk.MenuItem( _("Options") )
	Options = gtk.Menu()
	menu.append(OptionsMenu)
	OptionsMenu.set_submenu(Options)

	MainOptCl = gtk.MenuItem( _("Clean Workspace"))
	MainOptCl.connect("activate", callback, "Clean")
	Options.append(MainOptCl)

	DebugOption = gtk.MenuItem( _("Debug") )
	DebugOption.connect("activate", DebugOn)
	Options.append(DebugOption)

	LogOption = gtk.MenuItem( _("Check the log") )
	LogOption.connect("activate", callback, "Log")
	Options.append(LogOption)

	ReportBug = gtk.MenuItem( _("Report a bug") )
	ReportBug.connect("activate", callback, "Bug")
	Options.append(ReportBug)

	sep = gtk.SeparatorMenuItem()
	Options.append(sep)


	ChangelogOption = gtk.MenuItem( _("Changelog"))
	ChangelogOption.connect("activate", callback, "Changelog")
	Options.append(ChangelogOption)

	UpdateOption = gtk.MenuItem( _("Update"))
	UpdateOption.connect("activate", callback, "Update")
	Options.append(UpdateOption)


	RestartOption = gtk.MenuItem( _("Restart"))
	RestartOption.connect("activate", Restart)
	Options.append(RestartOption)



	menu.show_all()
	
	vbox.pack_start(menu, False, False, 0)

	notebook = gtk.Notebook()
	notebook.set_tab_pos(gtk.POS_TOP)
	vbox.pack_start(notebook)
	notebook.set_scrollable(True)

        notebook.show()

	# UTIL TABLE
	UtilVBox = gtk.VBox()

	UtilLabel = gtk.Label( _("Images"))

	image = gtk.Image()
	image.set_from_file(os.path.join(ScriptDir, "images", "Utils.png"))
	image.show()
	UtilVBox.pack_start(image, False, False, 10)

	MainOpt1 = gtk.Button( _("Install Image Tools"))
	MainOpt1.connect("clicked", callback, "Utils")
	UtilVBox.pack_start(MainOpt1, True, False, 10)

	MainOpt2 = gtk.Button( _("CopieFrom"))
	MainOpt2.connect("clicked", callback, "CopyFrom")
	UtilVBox.pack_start(MainOpt2, True, False, 10)

	MainOpt3 = gtk.Button( _("Resize"))
	MainOpt3.connect("clicked", callback, "Resize")
	UtilVBox.pack_start(MainOpt3, True, False, 10)

	MainOpt4 = gtk.Button( _("Batch Theme"))
	MainOpt4.connect("clicked", callback, "Theme")
	UtilVBox.pack_start(MainOpt4, True, False, 10)

	MainOpt5 = gtk.Button( _("Optimize Images") )
	MainOpt5.connect("clicked", callback, "OptimizeImage")
	UtilVBox.pack_start(MainOpt5, True, False, 10)

	notebook.insert_page(UtilVBox, UtilLabel, 1)

	# DEVELOP TABLE

	DevelopTable = gtk.Table(8, 1, False)
	DevelopLabel = gtk.Label( _("Development") )
	DevelopVBox = gtk.VBox()

	image = gtk.Image()
	image.set_from_file(os.path.join(ScriptDir, "images", "Develop.png"))
	image.show()
	DevelopVBox.pack_start(image, False, False, 10)

	if not OS == 'Win':
		MainOpt6 = gtk.Button( _("Prepare Building") )
		MainOpt6.connect("clicked", callback, "PrepareBuilding")
		DevelopVBox.pack_start(MainOpt6, True, False, 10)

		MainOpt7 = gtk.Button( _("Build from Source") )
		MainOpt7.connect("clicked", callback, "BuildSource")
		DevelopVBox.pack_start(MainOpt7, True, False, 10)

		MainOpt9 = gtk.Button( _("Add Governor") )
		MainOpt9.connect("clicked", callback, "AddGovernor")
		DevelopVBox.pack_start(MainOpt9, True, False, 10)

	MainOpt11 = gtk.Button( _("Install Android-SDK") )
	MainOpt11.connect("clicked", callback, "SDK")
	DevelopVBox.pack_start(MainOpt11, True, False, 10)

	MainOpt12 = gtk.Button(_("Install Java JDK"))
	MainOpt12.connect("clicked", callback, "JDK")
	DevelopVBox.pack_start(MainOpt12, True, False, 10)

	BinaryPortOpt = gtk.Button(_("Binary port a ROM"))
	BinaryPortOpt.connect("clicked", callback, "BinaryPort")
	DevelopVBox.pack_start(BinaryPortOpt, True, False, 10)

	notebook.insert_page(DevelopVBox, DevelopLabel, 2)

	# APK TABLE

	ApkLabel = gtk.Label("APK")
	APKVBox = gtk.VBox(False, 10)

	image = gtk.Image()
	image.set_from_file(os.path.join(ScriptDir, "images", "APK.png"))
	image.show()
	APKVBox.pack_start(image, False, False, 10)

	MainOpt13 = gtk.Button( _("(De)Compile"))
	MainOpt13.connect("clicked", callback, "DeCompile")
	APKVBox.pack_start(MainOpt13, True, False, 10)

	MainOpt14 = gtk.Button( _("Extract/Repackage") )
	MainOpt14.connect("clicked", callback, "ExPackage")
	APKVBox.pack_start(MainOpt14, True, False, 10)

	MainOpt15 = gtk.Button( _("Sign APK") )
	MainOpt15.connect("clicked", callback, "Sign")
	APKVBox.pack_start(MainOpt15, True, False, 10)

	MainOpt16 = gtk.Button( _("Zipalign APK") )
	MainOpt16.connect("clicked", callback, "Zipalign")
	APKVBox.pack_start(MainOpt16, True, False, 10)

	MainOpt18 = gtk.Button( _("Install APK") )
	MainOpt18.connect("clicked", callback, "Install")
	APKVBox.pack_start(MainOpt18, True, False, 10)
	
	MainOpt19 = gtk.Button( _("Optimize Image Inside APK") )
	MainOpt19.connect("clicked", callback, "OptimizeInside")
	APKVBox.pack_start(MainOpt19, True, False, 10)

	notebook.insert_page(APKVBox, ApkLabel, 3)

	# ADVANCE TABLE

	AdvanceVBox = gtk.VBox()
	AdvanceLabel = gtk.Label( _("Advanced") )

	image = gtk.Image()
	image.set_from_file(os.path.join(ScriptDir, "images", "Advanced.png"))
	image.show()
	AdvanceVBox.pack_start(image, False, False, 10)

	MainOpt20 = gtk.Button( _("(Bak)Smali"))
	MainOpt20.connect("clicked", callback, "BakSmali")
	AdvanceVBox.pack_start(MainOpt20, True, False, 10)

	MainOpt22 = gtk.Button( _("ODEX") )
	MainOpt22.connect("clicked", callback, "Odex")
	AdvanceVBox.pack_start(MainOpt22, True, False, 10)

	MainOpt23 = gtk.Button(_("DE-ODEX"))
	MainOpt23.connect("clicked", callback, "Deodex")
	AdvanceVBox.pack_start(MainOpt23, True, False, 10)

	MainOpt24 = gtk.Button(_("Aroma Menu"))
	MainOpt24.connect("clicked", callback, "Aroma")
	AdvanceVBox.pack_start(MainOpt24, True, False, 10)

	MainOptComp = gtk.Button(_("Compile to an exe"))
	MainOptComp.connect("clicked", callback, "Compile")
	AdvanceVBox.pack_start(MainOptComp, True, False, 10)

	notebook.insert_page(AdvanceVBox, AdvanceLabel, 4)

	# ANDROID TABLE

	AndroidVBox = gtk.VBox()
	AndroidLabel = gtk.Label( _("Android") )

	ADBBtn = gtk.Button(_("Configure ADB"))
	ADBBtn.connect("clicked", callback, 'ADBConfig')
	AndroidVBox.pack_start(ADBBtn, True, False, 10)

	LogcatBtn = gtk.Button(_("Logcat"))
	LogcatBtn.connect("clicked", callback, 'LogCat')
	AndroidVBox.pack_start(LogcatBtn, True, False, 10)

	BuildPropBtn = gtk.Button(_("Build.prop ADB"))
	BuildPropBtn.connect("clicked", callback, 'BuildProp')
	AndroidVBox.pack_start(BuildPropBtn, True, False, 10)

	BackUpBtn = gtk.Button(_("Backup / Restore"))
	BackUpBtn.connect("clicked", callback, "BackupRestore")
	AndroidVBox.pack_start(BackUpBtn, True, False, 10)

	AdbFEBtn = gtk.Button(_("ADB File Explorer"))
	AdbFEBtn.connect("clicked", callback, "AdbFE")
	AndroidVBox.pack_start(AdbFEBtn, True, False, 10)


	notebook.insert_page(AndroidVBox, AndroidLabel, 5)

	
	
	#notebook.insert_page(AndroidVBox, AndroidLabel, 5)


	# END, show main tab
	window.add(vbox)

	vbox.show_all()
	window.show_all()

class GlobalData():
	AdbOpts = ''

# FROM HERE, ALL FUNCTIONS USED IN MAINAPP WILL BE DEFINED

def Clean():
	open(os.path.join(ScriptDir, "log")).close()
	for tree in ['APK', 'Resize', 'Resized', 'Resizing', 'Advance', 'Utils', 'Theme', 'ADB']:
		tree = os.path.join(ScriptDir, tree)
		shutil.rmtree(tree, True)
	shutil.rmtree(os.path.join(Home, ".SA"), True)
	os.remove(os.path.join(ScriptDir, "log"))
	if os.path.exists(os.path.join(ConfDir, "debug")):
		os.remove(os.path.join(ConfDir, "debug"))
	for x in ['SA.pyc', os.path.join('Source', 'repocmd'), os.path.join('Source', 'syncswitches')]:
		try:
			os.remove(os.path.join(ScriptDir, x))
		except OSError:
			pass



def Utils():
	def Install(cmd):
		if not OS == 'Lin' or OS == 'Mac':
			if not UtilDir in PATH:
				SystemLog('echo "PATH=%s:$PATH" >> %s' %(UtilDir, os.path.join(Home, ".profile")))
			if ImageBtn.get_active():
				if OS == 'Lin': SystemLog("sudo apt-get install imagemagick")
				elif OS == 'Mac':
					if not os.path.exists(os.path.join(ConfDir, "IM.tar.gz")):
						urllib.urlretrieve('http://www.imagemagick.org/download/binaries/ImageMagick-x86_64-apple-darwin12.0.0.tar.gz', os.path.join(ConfDir, "IM.tar.gz"))
					ExZip(os.path.join(ConfDir, "IM.tar.gz"), Home, 'tar')
					if not os.path.join(Home, "ImageMagick-6.7.8", "bin") in PATH:
						HOME = os.environ['HOME']
						MAGICK_HOME=os.path.join(HOME, "ImageMagick-6.7.8")
						msg = "#\nMAGICK_HOME=%s\nPATH=%s/bin/:$PATH\nDYLD_LIBRARY_PATH=%s/lib/" %(MAGICK_HOME, MAGICK_HOME, MAGICK_HOME)
						SystemLog('echo "%s" >> %s' %(msg, os.path.join(Home, ".profile")))
			if PILBtn.get_active():
				SystemLog("sudo easy_install pip")
				SystemLog("sudo sh %s 1")
		if OS == 'Win':
			if ImageBtn.get_active():
				urllib.urlretrieve("http://www.imagemagick.org/download/binaries/", os.path.join(ConfDir, "index.html"))
				f = open(os.path.join(ConfDir, "index.html"), "r").readlines()
				ln = f[10]
				version = str(str(remove_tags(ln)).split('.exe')[0]).replace('Q8', 'Q16') + ".exe"
			
				wait = NewDialog(_("ImageMagick"), _("You will now download and run ImageMagick. Proceed the installation."))
				if os.path.exists(os.path.join(ConfDir, "IM.exe")):
					os.remove(os.path.join(ConfDir, "IM.exe"))
				urllib.urlretrieve("http://www.imagemagick.org/download/binaries/%s" % version, os.path.join(ConfDir, "IM.exe"))
				SystemLog("start %s" % os.path.join(ConfDir, "IM.exe"))
			if PILBtn.get_active():
				urllib.urlretrieve("http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe", os.path.join(ConfDir, "PIL.exe"))
				SystemLog("start %s" % os.path.join(ConfDir, "PIL.exe"))

				

		KillPage("cmd", vbox)

	notebook = MainApp.notebook
	vbox = gtk.VBox()
	hbox = gtk.HBox()
	vbox1 = gtk.VBox()
	vbox2 = gtk.VBox()
	hbox.pack_start(vbox1)
	hbox.pack_start(vbox2)

        label = gtk.Label( _("ImageMagick is needed for all image tools I included.\nIn future releases I will use PIL more. So install PIL too!") )
	label.set_justify(gtk.JUSTIFY_CENTER)
	vbox.pack_start(label, False, False, 0)

	ImageBtn = gtk.CheckButton("ImageMagick")
	vbox1.pack_start(ImageBtn)

	PILBtn = gtk.CheckBtn = gtk.CheckButton("Python Image Library")
	vbox2.pack_start(PILBtn)

	buttonInstall = gtk.Button( _("Install") )
	buttonInstall.connect("clicked", Install)

	UtilsLabel = NewPage( _("Install Image Tools") , vbox)
	UtilsLabel.show_all()

	vbox.pack_start(hbox)
	vbox.pack_start(buttonInstall, False, False, 0)
	notebook.insert_page(vbox, UtilsLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)
	


	

def CopyFrom():
	def GetDir(DirChooser, Btn):
		value = DirChoose(DirChooser)
		text = Btn.get_label().split("   :   ")[0]
		Btn.set_label(text + "   :   " + value)
		Btn.show()
		return value
	def Start(cmd):
		Ext = ExtBox.get_text()
		print _("Copying files FROM " + FromDir + " to " + ToDir + " With extension " + Ext)
		for ToFile in find_files(ToDir, "*" + Ext):
			filename = ToFile.replace(ToDir, FromDir)
			if os.path.exists(filename):
				print _("Copying %s to %s" %(filename, ToFile))
				shutil.copy(filename, ToFile)
			
		KillPage(cmd, vbox)

	CopyFromWindow = window
	CopyFromLabel = gtk.Label( _("CopyFrom"))

	vbox = gtk.VBox()
	notebook = MainApp.notebook

	label = gtk.Label( _("""This tool copies files existing in a directory FROM an other directory.
			Can be handy for porting themes and such\n\nMake sure both directories have the same structure!\n\n\n""") )

	vbox.pack_start(label, False, False, 0)

	def Choose(cmd, DirChooser, kind, Btn):
		DirChooser.set_current_folder(ScriptDir)
		if kind == 'ToDir':
			global ToDir
			ToDir = GetDir(DirChooser, Btn)
		elif kind == 'FromDir':
			global FromDir
			FromDir = GetDir(DirChooser, Btn)

	ToDirBtn = gtk.Button( _("Enter the directory you want to copy the files TO") )
	ToDirDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  	buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))

	ToDirBtn.connect("clicked", Choose, ToDirDial, 'ToDir', ToDirBtn)
	vbox.pack_start(ToDirBtn, False, False, 0)


	FromDirBtn = gtk.Button(_("Enter the directory you want to copy the files FROM") )
	FromDirDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  	buttons=(gtk.STOCK_OPEN,gtk.RESPONSE_OK))

	FromDirBtn.connect("clicked", Choose, FromDirDial, 'FromDir', FromDirBtn)
	vbox.pack_start(FromDirBtn, False, False, 0)

	hbox = gtk.HBox()

	ExtBox = gtk.Entry()
	ExtBox.set_size_request(80, 25)
	ExtBox.set_text(".")
	ExtLabel = gtk.Label( _("Enter the extension of the files you want to copy") )
	hbox.pack_start(ExtBox, False, False, 3)
	hbox.pack_start(ExtLabel, False, False, 45)

	vbox.pack_start(hbox, False, False, 0)

	StartButton = gtk.Button("CopyFrom!")
	StartButton.connect("clicked", Start)

	vbox.pack_start(StartButton, False, False, 30)

	CopyFromLabel = NewPage( _("CopyFrom"), vbox )
	CopyFromLabel.show_all()
	
	notebook.insert_page(vbox, CopyFromLabel)
	CopyFromWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Resize():
	def GetDir(cmd, DirChooser, Btn):
		try: In
		except:
			ResizeStartButton = gtk.Button(_("Start resizing"))
			ResizeStartButton.connect("clicked", StartResize)
			vbox.pack_start(ResizeStartButton, False, False, 15)
			window.show_all()
		MainApp.In = DirChoose(DirChooser)
		Btn.set_label(MainApp.In)
		Btn.show()

	def GetFile(cmd, FileChooser, Btn, label, filtern=None):
		try: In
		except:
			ResizeStartButton = gtk.Button(_("Start resizing"))
			ResizeStartButton.connect("clicked", StartResize)
			vbox.pack_start(ResizeStartButton, False, False, 15)
			window.show_all()
		MainApp.In = FileChoose(FileChooser, filtern)
		Btn.set_label(MainApp.In)
		Btn.show()
	def StartResize(cmd):
		try: MainApp.In
		except:	NewDialog("Resize", _("Please select a directory/APK before you click START"))
		else:
			DstDir = os.path.join(ScriptDir, "Resized", '')
			if NormalResize.get_active():
				Perc = ResizePercentageBox.get_text()
				if not Perc.endswith("%"):
					Perc = Perc + "%"
			if EasyResize.get_active():
				InDPI = InDPIBox.get_text()
				OutDPI = OutDPIBox.get_text()
				if InDPI == 'XHDPI':
					InRes = 720
				elif InDPI == 'HDPI':
					InRes = 480
				elif InDPI == 'MDPI':
					InRes = 320
				elif InDPI == 'LDPI':
					InRes = 240
				else:
					InRes = InDPI
				if OutDPI == 'XHDPI':
					OutRes = 720
				elif OutDPI == 'HDPI':
					OutRes = 480
				elif OutDPI == 'MDPI':
					OutRes = 320
				elif OutDPI == 'LDPI':
					OutRes = 240
				else:
					OutRes = int(OutDPI)

			if ApkResize.get_active():
				InDPI = ApkInDPIBox.get_text()
				OutDPI = ApkOutDPIBox.get_text()
				if InDPI == 'XHDPI':
					InRes = 720
					InDir1 = 'xhdpi'
				elif InDPI == 'HDPI':
					InRes = 480
					InDir1 = 'hdpi'
				elif InDPI == 'MDPI':
					InRes = 320
					InDir1 = 'mdpi'
				elif InDPI == 'LDPI':
					InRes = 240
					InDir1 = 'ldpi'
				else:
					InRes = int(InDPI)
					InDir1 = 'hdpi'
				if OutDPI == 'XHDPI':
					OutRes = 720
					OutDir1 = 'xhdpi'
				elif OutDPI == 'HDPI':
					OutRes = 480
					OutDir1 = 'hdpi'
				elif OutDPI == 'MDPI':
					OutRes = 320
					OutDir1 = 'mdpi'
				elif OutDPI == 'LDPI':
					OutRes = 240
					OutDir1 = 'ldpi'
				else:
					OutRes = int(OutDPI)
					OutDir1 = 'hdpi'
				FullZipDir = os.path.join(ScriptDir, "Resizing")
				if os.path.exists(FullZipDir):
					shutil.rmtree(FullZipDir)
				ExZip(MainApp.In, FullZipDir)
				Apk = MainApp.In
				MainApp.ResizeAPK = MainApp.In
				MainApp.In = os.path.join(ScriptDir, "Resizing", "res", "drawable-" + InDir1)
				DstDir = os.path.join(ScriptDir, "Resizing", "res", "drawable-" + OutDir1, '')

			if ApkResize.get_active() or EasyResize.get_active():
				Perc = str(round(OutRes * 100 / InRes, 2)) + "%"

			print _("Resize percentage is %s" % str(Perc))
			if os.path.exists(DstDir):
				shutil.rmtree(DstDir)
			os.makedirs(DstDir)

			SrcDir = os.path.join(MainApp.In, '')

			print("SrcDir = %s\nDstDir = %s" %(SrcDir, DstDir))

			for x in find_files(SrcDir, ".png"): print x
			for Image in find_files(SrcDir, "*.png"):
				DstFile = Image.replace(SrcDir, DstDir)
				Name = os.path.basename(Image)
				Sub = Image.replace(SrcDir, '')
				Sub = Sub.replace(Name, '')
				if not os.path.exists(os.path.join(DstDir, Sub)):
					os.makedirs(os.path.join(DstDir, Sub))
				print("%s -> %s" %(Image, DstFile))
				if Image.endswith("9.png"):
					print("%s has 9patch" % Image)
					shutil.copy(Image, DstFile)
					continue
				if Debug == True: print("convert %s -resize %s %s" % (Image, Perc, DstFile))
				SystemLog("convert %s -resize %s %s" % (Image, Perc, DstFile))
			if ApkResize.get_active():
				FinDstDir = os.path.join(ScriptDir, "Resized")
				if os.path.exists(FinDstDir):
					shutil.rmtree(FinDstDir)
				os.makedirs(FinDstDir)
				shutil.copy(MainApp.ResizeAPK, FinDstDir)
				DstApk = os.path.join(FinDstDir, os.path.basename(MainApp.ResizeAPK))
				zipf = zipfile.ZipFile(DstApk, "a")
				for file in os.listdir(DstDir):
					fullfile = os.path.join(DstDir, file)
					zipf.write(fullfile, os.path.join("res", "drawable-%s" % OutDir1, file))
				zipf.close()
			if os.path.exists(os.path.join(ScriptDir, "Resizing")):
				shutil.rmtree(os.path.join(ScriptDir, "Resizing"))
			NewDialog( _("Resized") , _("You can find the resized images in Resized") )
			KillPage(cmd, vbox)
		
		
	ResizeWindow = window
	ResizeLabel = gtk.Label("Resize")
	vbox = gtk.VBox()
	sw = gtk.ScrolledWindow()
	notebook = MainApp.notebook

	NormalResize = gtk.RadioButton(None, "Normal resizing using resize percentage")
	vbox.pack_start(NormalResize, False, False, 2)

	NormalResizeTable = gtk.Table(2, 2, True)
	NormalResizeTable.set_col_spacings(2)
	NormalResizeTable.set_row_spacings(2)

	ResizePercentageBox = gtk.Entry()
	ResizePercentageBox.set_text("%")
	ResizePercentageBox.set_size_request(0, 30)

	ResizePercentageLabel = gtk.Label( _("Enter the resize percentage 0-100 %") )

	ResizeDirDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  	buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	ResizeDirBtn = gtk.Button("Select the directory")

	ResizeDirLabel = gtk.Label( _("Choose the directory containing the images"))
	ResizeDirBtn.connect("clicked", GetDir, ResizeDirDial, ResizeDirBtn)

	NormalResizeTable.attach(ResizePercentageBox, 0, 1, 0, 1, xpadding=20)
	NormalResizeTable.attach(ResizePercentageLabel, 1, 2, 0, 1)
	NormalResizeTable.attach(ResizeDirBtn, 0, 1, 1, 2, xpadding=20)
	NormalResizeTable.attach(ResizeDirLabel, 1, 2, 1, 2)
	vbox.pack_start(NormalResizeTable, False, False, 0)

	EasyResize = gtk.RadioButton(NormalResize, _("Easy resizing using ..DPI values"))
	vbox.pack_start(EasyResize, False, False, 2)

	EasyResizeTable = gtk.Table(2, 2, True)
	
	InDPIBox = gtk.Entry()
	InDPIBox.set_text("..DPI")
	EasyResizeTable.attach(InDPIBox, 0, 1, 0, 1, xpadding=20)
	InDPILabel = gtk.Label( _("Give the DPI of the images"))
	EasyResizeTable.attach(InDPILabel, 1, 2, 0, 1)

	OutDPIBox = gtk.Entry()
	OutDPIBox.set_text("..DPI")
	EasyResizeTable.attach(OutDPIBox, 0, 1, 1, 2, xpadding=20)
	OutDPILabel = gtk.Label( _("Give the Resized DPI"))
	EasyResizeTable.attach(OutDPILabel, 1, 2, 1, 2)

	EasyResizeDirDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  	buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	EasyResizeDirBtn = gtk.Button("Select the directory")

	EasyResizeTable.attach(EasyResizeDirBtn, 0, 1, 2, 3, xpadding=20)
	ResizeDirLabel = gtk.Label(_("Choose the directory containing the images"))
	EasyResizeDirBtn.connect("clicked", GetDir, ResizeDirDial, EasyResizeDirBtn)
	EasyResizeTable.attach(ResizeDirLabel, 1, 2, 2, 3)

	vbox.pack_start(EasyResizeTable, False, False, 0)

	ApkResize = gtk.RadioButton(NormalResize, _("Resize an APK using DPI values"))
	vbox.pack_start(ApkResize, False, False, 10)

	APKResizeTable = gtk.Table(3, 2, True)
	
	ApkInDPIBox = gtk.Entry()
	ApkInDPIBox.set_text("..DPI")
	APKResizeTable.attach(ApkInDPIBox, 0, 1, 0, 1, xpadding=20)
	ApkInDPILabel = gtk.Label(_("Give the DPI of the images"))
	APKResizeTable.attach(ApkInDPILabel, 1, 2, 0, 1)

	ApkOutDPIBox = gtk.Entry()
	ApkOutDPIBox.set_text("..DPI")
	APKResizeTable.attach(ApkOutDPIBox, 0, 1, 1, 2, xpadding=20)
	ApkOutDPILabel = gtk.Label("Give the Resized DPI")
	APKResizeTable.attach(ApkOutDPILabel, 1, 2, 1, 2)

	ApkResizeDirBox = gtk.Entry()
	ApkResizeDirBox.set_text(os.path.join(ScriptDir, ''))
	ApkResizeDirBox.set_size_request(0, 30)
	
	ApkResizeApk = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	ApkResizeBtn = gtk.Button(_("Choose the APK"))
	APKResizeTable.attach(ApkResizeBtn, 0, 1, 2, 3, xpadding=20)
	ApkResizeBtn.connect("clicked", GetFile, ApkResizeApk, ApkResizeBtn, ResizeDirLabel, ".apk")

	ResizeDirLabel = gtk.Label(_("Choose the APK"))
	APKResizeTable.attach(ResizeDirLabel, 1, 2, 2, 3)

	vbox.pack_start(APKResizeTable, False, False, 0)

	ResizeLabel = NewPage("Resize", vbox)
	ResizeLabel.show_all()

	notebook.insert_page(vbox, ResizeLabel)

	ResizeWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Theme():
	def ShowColor(cmd):
		Red = int(int(RedScale.get_value()) * 65535 / 100)
		if str(Red).startswith("-"):
			Red = int(0)
		Green = int(int(GreenScale.get_value()) * 65535 / 100)
		if str(Green).startswith("-"):
			Green = int(0)
		Blue = int(int(BlueScale.get_value()) * 65535 / 100)
		if str(Blue).startswith("-"):
			Blue = int(0)
		color = gtk.gdk.Color(red=Red, green=Green, blue=Blue)
		Draw.modify_bg(gtk.STATE_NORMAL, color)
		Red = int(str(RedScale.get_value()).split('.')[0])
		Green = int(str(GreenScale.get_value()).split('.')[0])
		Blue = int(str(BlueScale.get_value()).split('.')[0])
		Clr = RGBToHTMLColor((Red, Green, Blue))
	def StartTheming(cmd):
		StockRed = RedScale.get_value()
		StockBlue = BlueScale.get_value()
		StockGreen = BlueScale.get_value()
		
		Red = int(str(RedScale.get_value()).split('.')[0])
		Green = int(str(GreenScale.get_value()).split('.')[0])
		Blue = int(str(BlueScale.get_value()).split('.')[0])
		Clr = RGBToHTMLColor((Red, Green, Blue))
		SrcDir = os.path.join(ScriptDir, "Theme")
		SystemLog("mkdir -p " + SrcDir)
		print(Clr)
		for image in find_files(SrcDir, "*.png"):
			Image1 = str(image)
			if Debug == True: print('mogrify -fill "%s" -tint 100 %s' %(Clr, Image1))
			if 'ImageOps' in globals(): Image.open('%s' % Image1).convert('LA').save('%s' % Image1)
			else: SystemLog('convert %s -colorspace gray %s' %(Image1, Image1) )
			SystemLog('mogrify -fill "%s" -tint 100 %s' %(Clr, Image1))
		NewDialog("Themed", "You can find the themed images inside Theme")
	ThemeWindow = window	
	SrcDir = os.path.join(ScriptDir, "Theme")
	ThemeLabel = gtk.Label( _("Place the images you want to theme inside " + SrcDir))
	notebook = MainApp.notebook
	
	if not os.path.exists(SrcDir):
		os.makedirs(SrcDir)

	vbox = gtk.VBox()
	vbox.pack_start(ThemeLabel, False, False, 10)

	ColorTable = gtk.Table(3, 2, True)
	vbox.pack_start(ColorTable, False, False, 0)

        adj1 = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        RedScale = gtk.HScale(adj1)
	RedScale.set_digits(0)
	RedScale.set_value(12)
	#RedScale.set_range(0,
	RedScale.connect("value-changed", ShowColor)
	ColorTable.attach(RedScale, 0, 1, 0, 1)

	RedLabel = gtk.Label( _("Enter the RED value (0-100)") )
	ColorTable.attach(RedLabel, 1, 2, 0, 1)

        adj2 = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        GreenScale = gtk.HScale(adj2)
	GreenScale.set_digits(0)
	GreenScale.set_value(66)
	GreenScale.connect("value-changed", ShowColor)
	ColorTable.attach(GreenScale, 0, 1, 1, 2)

	GreenLabel = gtk.Label( _("Enter the GREEN value (0-100)") )
	ColorTable.attach(GreenLabel, 1, 2, 1, 2)

        adj3 = gtk.Adjustment(0.0, 10.0, 101.0, 0.0, 1.0, 1.0)
        BlueScale = gtk.HScale(adj3)
	BlueScale.set_digits(0)
	BlueScale.set_value(77)
	BlueScale.connect("value-changed", ShowColor)
	ColorTable.attach(BlueScale, 0, 1, 2, 3)

	BlueLabel = gtk.Label( _("Enter the BLUE value (0-100)") )
	ColorTable.attach(BlueLabel, 1, 2, 2, 3)
	


	ColorButton = gtk.Button( _("Show Color") )
	ColorButton.connect("clicked", ShowColor)



	vbox.pack_start(ColorButton, False, False, 15)

	Draw = gtk.DrawingArea()
	Color = Draw.get_colormap().alloc_color(0, 65535, 0)
	Draw.set_size_request(100, 50)
	Draw.show()
	vbox.pack_start(Draw, False, False, 0)

	StartButton = gtk.Button( _("Start theming!") )
	StartButton.connect("clicked", StartTheming)
	vbox.pack_start(StartButton, False, False, 15)

	ThemeLabel = NewPage("Theme", vbox)
	ThemeLabel.show_all()

	notebook.insert_page(vbox, ThemeLabel)

	ThemeWindow.show_all()
	ShowColor(None)
	notebook.set_current_page(notebook.get_n_pages() - 1)
	

def PrepareBuilding():
	def Prepare(cmd):
		NewDialog("Info", _("Please check the terminal for further progress."))
		SystemLog("""sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update &
sudo apt-get upgrade &
sudo apt-get install python2.5 &
sudo add-apt-repository "deb http://archive.canonical.com/ lucid partner"
sudo add-apt-repository "deb-src http://archive.canonical.com/ubuntu lucid partner"
sudo apt-get update &
sudo apt-get install sun-java6-jdk &
sudo apt-get update &
sudo apt-get upgrade &
sudo apt-get install git-core &
sudo apt-get install valgrind &
sudo apt-get install git-core gnupg flex bison gperf build-essential \
zip curl zlib1g-dev libc6-dev lib64ncurses5-dev \
x11proto-core-dev libx11-dev lib64readline-gplv2-dev lib64z1-dev \
libgl1-mesa-dev g++-multilib tofrodos &
mkdir -p ~/bin
mkdir -p ~/android/system
curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > ~/bin/repo
chmod a+x ~/bin/repo
sudo echo '#Acer
SUBSYSTEM==usb, SYSFS{idVendor}==0502, MODE=0666

#ASUS
SUBSYSTEM==usb, SYSFS{idVendor}==0b05, MODE=0666

#Dell
SUBSYSTEM==usb, SYSFS{idVendor}==413c, MODE=0666

#Foxconn
SUBSYSTEM==usb, SYSFS{idVendor}==0489, MODE=0666

#Garmin-Asus
SUBSYSTEM==usb, SYSFS{idVendor}==091E, MODE=0666

#Google
SUBSYSTEM==usb, SYSFS{idVendor}==18d1, MODE=0666

#HTC
SUBSYSTEM=="usb", SYSFS{idVendor}=="0bb4", MODE="0666"

#Huawei
SUBSYSTEM==usb, SYSFS{idVendor}==12d1, MODE=0666

#K-Touch
SUBSYSTEM==usb, SYSFS{idVendor}==24e3, MODE=0666

#KT Tech
SUBSYSTEM==usb, SYSFS{idVendor}==2116, MODE=0666

#Kyocera
SUBSYSTEM==usb, SYSFS{idVendor}==0482, MODE=0666

#Lenevo
SUBSYSTEM==usb, SYSFS{idVendor}==17EF, MODE=0666

#LG
SUBSYSTEM==usb, SYSFS{idVendor}==1004, MODE=0666

#Motorola
SUBSYSTEM==usb, SYSFS{idVendor}==22b8, MODE=0666

#NEC
SUBSYSTEM==usb, SYSFS{idVendor}==0409, MODE=0666

#Nook
SUBSYSTEM==usb, SYSFS{idVendor}==2080, MODE=0666

#Nvidia
SUBSYSTEM==usb, SYSFS{idVendor}==0955, MODE=0666

#OTGV
SUBSYSTEM==usb, SYSFS{idVendor}==2257, MODE=0666

#Pantech
SUBSYSTEM==usb, SYSFS{idVendor}==10A9, MODE=0666

#Philips
SUBSYSTEM==usb, SYSFS{idVendor}==0471, MODE=0666

#PMC-Sierra
SUBSYSTEM==usb, SYSFS{idVendor}==04da, MODE=0666

#Qualcomm
SUBSYSTEM==usb, SYSFS{idVendor}==05c6, MODE=0666

#SK Telesys
SUBSYSTEM==usb, SYSFS{idVendor}==1f53, MODE=0666

#Samsung
SUBSYSTEM==usb, SYSFS{idVendor}==04e8, MODE=0666

#Sharp
SUBSYSTEM==usb, SYSFS{idVendor}==04dd, MODE=0666

#Sony Ericsson
SUBSYSTEM==usb, SYSFS{idVendor}==0fce, MODE=0666

#Toshiba
SUBSYSTEM==usb, SYSFS{idVendor}==0930, MODE=0666

#ZTE
SUBSYSTEM==usb, SYSFS{idVendor}==19D2, MODE=0666' > /etc/udev/rules.d/51-android.rules
sudo chmod a+r /etc/udev/rules.d/51-android.rules

echo '-----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1.4.2.2 (GNU/Linux)  
    mQGiBEnnWD4RBACt9/h4v9xnnGDou13y3dvOx6/t43LPPIxeJ8eX9WB+8LLuROSV
    lFhpHawsVAcFlmi7f7jdSRF+OvtZL9ShPKdLfwBJMNkU66/TZmPewS4m782ndtw7
    8tR1cXb197Ob8kOfQB3A9yk2XZ4ei4ZC3i6wVdqHLRxABdncwu5hOF9KXwCgkxMD
    u4PVgChaAJzTYJ1EG+UYBIUEAJmfearb0qRAN7dEoff0FeXsEaUA6U90sEoVks0Z
    wNj96SA8BL+a1OoEUUfpMhiHyLuQSftxisJxTh+2QclzDviDyaTrkANjdYY7p2cq
    /HMdOY7LJlHaqtXmZxXjjtw5Uc2QG8UY8aziU3IE9nTjSwCXeJnuyvoizl9/I1S5
    jU5SA/9WwIps4SC84ielIXiGWEqq6i6/sk4I9q1YemZF2XVVKnmI1F4iCMtNKsR4
    MGSa1gA8s4iQbsKNWPgp7M3a51JCVCu6l/8zTpA+uUGapw4tWCp4o0dpIvDPBEa9
    b/aF/ygcR8mh5hgUfpF9IpXdknOsbKCvM9lSSfRciETykZc4wrRCVGhlIEFuZHJv
    aWQgT3BlbiBTb3VyY2UgUHJvamVjdCA8aW5pdGlhbC1jb250cmlidXRpb25AYW5k
    cm9pZC5jb20+iGAEExECACAFAknnWD4CGwMGCwkIBwMCBBUCCAMEFgIDAQIeAQIX
    gAAKCRDorT+BmrEOeNr+AJ42Xy6tEW7r3KzrJxnRX8mij9z8tgCdFfQYiHpYngkI
    2t09Ed+9Bm4gmEO5Ag0ESedYRBAIAKVW1JcMBWvV/0Bo9WiByJ9WJ5swMN36/vAl
    QN4mWRhfzDOk/Rosdb0csAO/l8Kz0gKQPOfObtyYjvI8JMC3rmi+LIvSUT9806Up
    hisyEmmHv6U8gUb/xHLIanXGxwhYzjgeuAXVCsv+EvoPIHbY4L/KvP5x+oCJIDbk
    C2b1TvVk9PryzmE4BPIQL/NtgR1oLWm/uWR9zRUFtBnE411aMAN3qnAHBBMZzKMX
    LWBGWE0znfRrnczI5p49i2YZJAjyX1P2WzmScK49CV82dzLo71MnrF6fj+Udtb5+
    OgTg7Cow+8PRaTkJEW5Y2JIZpnRUq0CYxAmHYX79EMKHDSThf/8AAwUIAJPWsB/M
    pK+KMs/s3r6nJrnYLTfdZhtmQXimpoDMJg1zxmL8UfNUKiQZ6esoAWtDgpqt7Y7s
    KZ8laHRARonte394hidZzM5nb6hQvpPjt2OlPRsyqVxw4c/KsjADtAuKW9/d8phb
    N8bTyOJo856qg4oOEzKG9eeF7oaZTYBy33BTL0408sEBxiMior6b8LrZrAhkqDjA
    vUXRwm/fFKgpsOysxC6xi553CxBUCH2omNV6Ka1LNMwzSp9ILz8jEGqmUtkBszwo
    G1S8fXgE0Lq3cdDM/GJ4QXP/p6LiwNF99faDMTV3+2SAOGvytOX6KjKVzKOSsfJQ
    hN0DlsIw8hqJc0WISQQYEQIACQUCSedYRAIbDAAKCRDorT+BmrEOeCUOAJ9qmR0l
    EXzeoxcdoafxqf6gZlJZlACgkWF7wi2YLW3Oa+jv2QSTlrx4KLM=
    =Wi5D 
    -----END PGP PUBLIC KEY BLOCK-----' > ~/gpgimport
gpg --import ~/gpgimport
rm ~/gpgimport""")
		SystemLog("""sudo apt-get install git-core gnupg flex bison gperf build-essential \
zip curl zlib1g-dev libc6-dev tofrodos python-markdown \
libxml2-utils xsltproc x11proto-core-dev libgl1-mesa-dev libx11-dev""")
		if Button64.get_active():
			SystemLog("""sudo apt-get install lib32ncurses5-dev ia32-libs lib32readline5-dev lib32z-dev g++-multilib mingw32""")
		if Button32.get_active():
			SystemLog("sudo apt-get install libncurses5-dev libreadline6-dev")
		if Button1010.get_active():
			SystemLog("sudo ln -s /usr/lib32/mesa/libGL.so.1 /usr/lib32/mesa/libGL.so")
		if Button1110.get_active():
			SystemLog("sudo apt-get install libx11-dev:i386")
		if Button1204.get_active():
			SystemLog("""sudo apt-get install libncurses5-dev:i386 libx11-dev:i386 libreadline6-dev:i386 libgl1-mesa-dev:i386 \
g++-multilib mingw32 openjdk-6-jdk tofrodos libxml2-utils xsltproc zlib1g-dev:i386""")
		KillPage("cmd", box)

	PrepareWindow = window
	notebook = MainApp.notebook

	box = gtk.VBox()

	

	label=gtk.Label( _("You need this option before you can build.\nPlease select your OS..."))
	box.pack_start(label, False, False, 10)

	Button1004 = gtk.RadioButton(None, "Ubuntu 10.04")
	box.pack_start(Button1004, False, False, 10)
	Button1010 = gtk.RadioButton(Button1004, "Ubuntu 10.10")
	box.pack_start(Button1010, False, False, 10)
	Button1110 = gtk.RadioButton(Button1004, "Ubuntu 11.10")
	box.pack_start(Button1110, False, False, 10)
	Button1204 = gtk.RadioButton(Button1004, "Ubuntu 12.04")
	box.pack_start(Button1204, False, False, 10)
	separator = gtk.HSeparator()
	box.pack_start(separator, False, True, 0)
	Button32 = gtk.RadioButton(None, "32-bits")
	box.pack_start(Button32, False, False, 10)
	Button64 = gtk.RadioButton(Button32, "64-bits")	
	Button64.set_active(True)
	def SetButton64(cmd):
		Button64.set_active(True)
	Button1204.connect("toggled", SetButton64)
	if (sys.maxsize > 2**32) == True:
		Button64.set_active()
	if platform.dist()[1] == 12.04: Button1204.set_active(True)
	elif platform.dist()[1] == 11.10: Button1110.set_active(True)
	elif platform.dist()[1] == 10.10: Button1010.set_active(True)
	elif platform.dist()[1] == 10.04: Button1004.set_active(True)
	box.pack_start(Button64, False, False, 10)
	ButtonPrepare = gtk.Button("Prepare to Build")
	ButtonPrepare.connect("clicked", Prepare)
	box.pack_start(ButtonPrepare, False, False, 20)
	PrepareLabel = NewPage("Prepare", box)
	PrepareLabel.show_all()
	notebook.insert_page(box, PrepareLabel)
	PrepareWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def SDK():
	print _("Retrieving SDK")
	if OS == 'Win':
		urllib.urlretrieve('http://dl.google.com/android/installer_r18-windows.exe', os.path.join(Home, 'SDK.exe'))
		SystemLog("start %s" % os.path.join(Home, 'SDK.exe'))
	else:
		if OS == 'Mac':
			urllib.urlretrieve('http://dl.google.com/android/android-sdk_r20.0.1-macosx.zip', os.path.join(Home, 'SDK.zip'))
			print _("Extracting SDK")
			ExZip(os.path.join(Home, 'SDK.zip'), Home)
		elif OS == 'Lin':
			urllib.urlretrieve('http://dl.google.com/android/android-sdk_r20.0.1-linux.tgz', os.path.join(Home, 'SDK.tgz'))
			print _("Extracting SDK")
			tar = tarfile.open(os.path.join(Home, "SDK.tgz"))
			tar.extractall(path=Home)
		for x in os.listdir(Home): 
			if "android-sdk-" in x: sdkdir = os.path.join(Home, x)
		print _("Setting permissions")
		for file in find_files(sdkdir, "*"):
			if not os.path.isdir(file):
				os.chmod(file, 0755)
		os.chdir(os.path.join(sdkdir, "tools"))
		SystemLog(os.path.join(".", "android") + " &")



def JDK():
	if OS == 'Lin':
		SystemLog('gksudo "apt-get -y install openjdk-7-jdk"')
	else:
		Web.open('http://www.oracle.com/technetwork/java/javase/downloads/jdk-7u4-downloads-1591156.html')

def BuildSource():
	class BuildData():
		data = ''

	notebook = MainApp.notebook	
	global vbox
	vbox = gtk.VBox()
	sw = gtk.ScrolledWindow()
	BuildData.Sources, BuildData.URL = Source.Src.MakeVal("SourceStock")

	def StartSync(cmd):
		switches = ''
		if Force.get_active():
			switches = switches + " -f"
		if Quiet.get_active():
			switches = switches + " -q"
		if Local.get_active():
			switches = switches + " -l"
		if Jobs.get_active():
			switches = switches +  " -j" + Cores
		os.chdir(Home)
		if not os.path.exists(SourceDir):
			os.makedirs(SourceDir)
		os.chdir(SourceDir)
		repocmdf = open(os.path.join(ScriptDir, "Source", "repocmd"), "w")
		repocmdf.write(BuildData.repocmd)
		repocmdf.close()
		switchesf = open(os.path.join(ScriptDir, "Source", "syncswitches"), "w")
		switchesf.write(switches)
		switchesf.close()

		SystemLog(os.path.join(ScriptDir, "Source", "Build.sh") + ' sync')
		StartBuild("cmd")
	def StartBuild(cmd):
		if not os.path.exists(os.path.join(SourceDir, ".repo")):
			NewDialog("ERROR", _(SourceDir + " does not exist!\nPress SYNC instead."))
		else:
			notebook.remove_page(notebook.get_n_pages() -1)
			sw = gtk.ScrolledWindow()
			BuildLabel = NewPage("Build", sw)
			BuildLabel.show_all()
			vbox = gtk.VBox()
			Std = gtk.RadioButton(None, "Std")

			for devi in find_files(os.path.join(SourceDir, "device"), "vendorsetup.sh"):
				for line in open(devi).readlines():
					if not line.startswith('#') and 'add_lunch_combo' in line:
						Text = line.replace('\n', '')
						Text = Text.replace('add_lunch_combo', '')
						Text = Text.replace('_', '--')
						NameBtn = gtk.RadioButton(Std, Text)
						vbox.pack_start(NameBtn)
			for devi in find_files(os.path.join(SourceDir, "vendor"), "vendorsetup.sh"):
				for line in open(devi).readlines():
					if not line.startswith('#') and 'add_lunch_combo' in line:
						Text = line.replace('\n', '')
						Text = Text.replace('add_lunch_combo', '')
						Text = Text.replace('_', '--')
						NameBtn = gtk.RadioButton(Std, Text)
						vbox.pack_start(NameBtn)

			StartButton = gtk.Button("Build!")
			vbox.pack_start(StartButton)
			StartButton.connect("clicked", Make, Std)

			sw.add_with_viewport(vbox)
			notebook.insert_page(sw, BuildLabel, 4)
			window.show_all()
			notebook.set_current_page(4)
	def Make(cmd, GroupStandard):
		switches = ''
		if Force2.get_active():
			switches = switches + " -f"
		if Quiet2.get_active():
			switches = switches + " -q"
		if Jobs2.get_active():
			switches = switches +  " -j" + Cores
		os.chdir(SourceDir)
		active = str([r for r in GroupStandard.get_group() if r.get_active()][0].get_label().replace('--', '_'))
		active = active.replace(' ', '')
		print >>open(os.path.join(ScriptDir, "Source", "makeswitches"), "w"), switches
		SystemLog("%s make %s&" %(os.path.join(ScriptDir, "Source", "Build.sh"), active))			


	def NewSources(cmd, SourceFile):
		f = open(os.path.join(Home, ".SA", "Device"), "w")
		print >> f,SourceFile
		SourceFile = SourceFile.replace('.py', '')
		SourceFile = SourceFile.replace('\n', '')
		BuildData.Sources, BuildData.URL = Source.Src.MakeVal(SourceFile)
        	notebook.remove_page(6)
		vbox3.destroy()
        	notebook.queue_draw_area(0,0,-1,-1)
		f.close()
		SetPage()

	def SetURL(cmd, num, NameBtn):
		if NameBtn.get_active():
			global Name, SourceDir
			BuildData.repocmd = BuildData.URL[num]
			Name = BuildData.Sources[num]
			SourceDir = os.path.join(Home, "WORKING_" + Name)


	global Force, Quiet, Local, Jobs
	hbox = gtk.HBox()

	label = gtk.Label( _("Choose the OS you want to build:"))
	vbox.pack_start(label, False, False, 10)

	Std = gtk.RadioButton(None, "Std")
	Std.show()

	vbox2 = gtk.VBox()
	vbox.pack_start(vbox2, False, False, 0)

	def SetPage():
		global vbox3
		vbox3 = gtk.VBox()
		vbox2.pack_start(vbox3, False, False, 0)
		Number = len(BuildData.Sources)
		for num in range(0, Number):
			Name = BuildData.Sources[num]
			NameBtn = gtk.RadioButton(Std, Name)
			NameBtn.connect("clicked", SetURL, num, NameBtn)
			vbox3.pack_start(NameBtn, False, False, 0)
		window.show_all()
	SetPage()

	hbox = gtk.HBox(False)
	vbox1 = gtk.VBox()
	vbox5 = gtk.VBox()

	SyncButton = gtk.Button(_("Sync"))
	SyncButton.connect("clicked", StartSync)
	vbox1.pack_start(SyncButton, False, False, 0)
	hbox.pack_start(vbox1)

	Force = gtk.CheckButton( _("Force sync"))
	vbox1.pack_start(Force, False, False, 0)

	Quiet = gtk.CheckButton( _("Be quiet!"))
	vbox1.pack_start(Quiet, False, False, 0)

	Local = gtk.CheckButton( _("Sync local only"))
	vbox1.pack_start(Local, False, False, 0)

	Jobs = gtk.CheckButton(_("Custom number of parallel jobs: %s" % Cores ))
	vbox1.pack_start(Jobs, False, False, 0)

	SkipButton = gtk.Button( _("Build (Only when synced)"))
	SkipButton.connect("clicked", StartBuild)
	vbox5.pack_start(SkipButton, False, False, 0)
	hbox.pack_start(vbox5)


	Force2 = gtk.CheckButton( _("Force build"))
	vbox5.pack_start(Force2, False, False, 0)

	Quiet2 = gtk.CheckButton( _("Be quiet!"))
	vbox5.pack_start(Quiet2, False, False, 0)

	Jobs2 = gtk.CheckButton(_("Custom number of parallel jobs: %s" % Cores ))
	vbox5.pack_start(Jobs2, False, False, 0)

	vbox.pack_start(hbox, False, False, 10)


	BuildLabel = NewPage(_("Build from Source"), vbox)
	BuildLabel.show_all()

	sw.add_with_viewport(vbox)

	notebook.insert_page(sw, BuildLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

	SourceMenu = gtk.MenuItem(_("Development"))
	menu.append(SourceMenu)
	DevelopmentMenu = gtk.Menu()
	SourceMenu.set_submenu(DevelopmentMenu)

	DeviceOption = gtk.MenuItem(_("Device"))
	DeviceMenu = gtk.Menu()
	DevelopmentMenu.append(DeviceOption)
	DeviceOption.set_submenu(DeviceMenu)

	for SourceFile in find_files(os.path.join(ScriptDir, "Source"), "Source*.py"):
		SourceFile = os.path.basename(SourceFile)
		Name = str(SourceFile.replace("Source", '')).replace('.py', '')
		MenuItem = gtk.MenuItem(Name)
		DeviceMenu.append(MenuItem)
		MenuItem.connect("activate", NewSources, SourceFile)
		MenuItem.show()
	menu.show_all()

	if os.path.exists(os.path.join(Home, ".SA", "Device")):
		Text = open(os.path.join(Home, ".SA", "Device"), "r")
		Text = Text.readlines()[0]
		NewSources("cmd", Text)
	else:
		NewDialog(_("Device"), _("You can choose the device you want to build for in the top bar."))


def AddGovernor():
	def Start(cmd):
		dialog = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("Kconfig")
		filter.add_mime_type("Kconfig")
		filter.add_pattern("Kconfig")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			dialog.hide_all()
			Kconfig = dialog.get_filename()
			Dirs = str(Kconfig).split("/")
			DirNum = len(Dirs)
			KernelDirs = Dirs[1:DirNum - 3]
			KernelRoot = '/'
			for d in KernelDirs:
				KernelRoot = os.path.join(KernelRoot, d)
			cpufreqdir = os.path.dirname(Kconfig)
			cpufreq = os.path.join(KernelRoot, "include", "linux", "cpufreq.h")
			NewKC = os.path.join(ScriptDir, "Kconfig")
			NewKCFile = open(NewKC, "a")
			MakeFile = os.path.join(cpufreqdir, "Makefile")
			NewMakeFile = os.path.join(ScriptDir, "Makefile")
			NewMake = open(NewMakeFile, "a")
			NewCpuFreq = os.path.join(ScriptDir, "cpufreq.h")
			NewCpu = open(NewCpuFreq, "a")

			for x in [NewKC, NewMakeFile, NewCpuFreq]:
				if os.path.exists(x):
					os.remove(x)
			for x in [NewKCFile, NewMake, NewCpu]:
				x.flush()
			for x in [MakeFile, Kconfig, cpufreq]:
				if os.path.exists(os.path.join(ConfDir, os.path.basename(x))):
					os.remove(os.path.join(ConfDir, os.path.basename(x)))
				shutil.copy(x, os.path.join(ConfDir, os.path.basename(x)))

			Set = False

			for GovBtn in BtnLst:
				if GovBtn.get_active():
					GovName = GovBtn.get_label()
					GovFile = os.path.join(GovDir, "cpufreq_%s.c" % GovName)
					one = open(os.path.join(GovDir, GovName + "1"), "r").read()
					two = open(os.path.join(GovDir, GovName + "2"), "r").read()
					three = open(os.path.join(GovDir, GovName + "3"), "r").read()
					four = open(os.path.join(GovDir, GovName + "4"), "r").read()
					for line in open(Kconfig, "r").readlines():
						if 'config CPU_FREQ_DEFAULT_GOV_' in line:
							Set = True
						if Set == True:
							NewKCFile.write("\n%s\n\n" % one)
							Set = False
						NewKCFile.write(line)

					for line in open(Kconfig, "r").readlines():
						if 'config CPU_FREQ_GOV_' in line:
							Set = True
						if Set == True:
							NewKCFile.write("\n%s\n\n" % two)
							Set = False
						NewKCFile.write(line)

					for line in open(MakeFile, "r").readlines():
						if "obj-$(CONFIG_CPU_FREQ_GOV_" in line:
							Set = True
						if Set == True:
							NewMake.write(three)
							Set = False
						NewMake.write(line)
					for line in open(cpufreq, "r"):
						if 'defined(CONFIG_CPU_FREQ_DEFAULT_GOV_' in line:
							Set = True
						if Set == True and '#endif' in line:
							NewCpu.write(four)
						NewCpu.write(line)

					for x in [MakeFile, Kconfig, cpufreq]:
						os.remove(x)
					shutil.copy(NewMakeFile, MakeFile)
					shutil.copy(NewKC, Kconfig)
					shutil.copy(NewCpuFreq, cpufreq)
					NewDialog(_("Added"), _("Added governors") )
		dialog.destroy()
	
	AddGovWindow = window
	notebook = MainApp.notebook
	sw = gtk.ScrolledWindow()
	
	vbox = gtk.VBox()
	label = gtk.Label( _("Ofcourse you need the kernel SOURCE, not the update.zip ;P") )

	SmartAssBtn = gtk.CheckButton("smartass")
	SmartAss2Btn = gtk.CheckButton("smartass2")
	LazyBtn = gtk.CheckButton("lazy")
	LulzActiveBtn = gtk.CheckButton("lulzactive")
	LagFreeBtn = gtk.CheckButton("lagfree")
	BtnLst = [SmartAssBtn, SmartAss2Btn, LazyBtn, LulzActiveBtn, LagFreeBtn]
	for Btn in BtnLst:
		vbox.pack_start(Btn, False, False, 0)
		Btn.show()

	ChooseKCButton = gtk.Button(None, _("Pick your drivers/cpufreq/Kconfig and start!"))
	vbox.pack_start(ChooseKCButton, True, False, 5)
	ChooseKCButton.connect("clicked", Start)
	
	GovLabel = NewPage(_("Add Governor"), sw)
	GovLabel.show_all()
	sw.add_with_viewport(vbox)
	notebook.insert_page(sw, GovLabel)
	AddGovWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def DeCompile():
	def Start(cmd):
		if DecompileButton.get_active():
			Number = len(decname)
			if Number == 0:
				NewDialog(_("ERROR"), _("No images inside %s. exit." % os.path.join("APK", "IN")))
			for num in range(0, Number):
				APK = decname[num]
				for apk in find_files(os.path.join(ScriptDir, "APK", "IN"), '*.apk'):
					name = os.path.basename(apk)
					if APK == name :
						ApkDir = APK.replace('.apk', '')
						APK = os.path.join(ScriptDir, "APK", "IN", APK)
						OutDir = os.path.join(ScriptDir, "APK", "DEC", ApkDir)
						if Debug == True: print("java -jar %s d -f %s %s" %(ApkJar, APK, OutDir))
						SystemLog("java -jar %s d -f %s %s" %(ApkJar, APK, OutDir))
						print _("Decompiled " + APK)
			Refresh("cmd")
		if CompileButton.get_active():
			Number = len(comname)
			if Number == 0:
				NewDialog(_("ERROR"), _("No images inside %s. exit." % os.path.join("APK", "IN") ))
			for num in range(0, Number):
				Dec = comname[num]
				for dec in os.listdir(os.path.join(ScriptDir, "APK", "DEC")):
					if dec == Dec :
						ApkFolder = os.path.join(ScriptDir, "APK", "DEC", dec)
						ApkName = os.path.join(ScriptDir, "APK", "OUT", "Unsigned-" + Dec + ".apk")
						if Debug == True: print("\njava -jar %s b -f %s %s\n" %(ApkJar, ApkFolder, ApkName))
						os.chdir(UtilDir)
						SystemLog("java -jar %s b -f %s %s " %(ApkJar, ApkFolder, ApkName))
						print _("Compiled %s" % ApkName)
						

	def Refresh(cmd):
		KillPage("cmd", vbox)
		DeCompile()


	DeCompileWindow = window
	notebook = MainApp.notebook
	sw = gtk.ScrolledWindow()
	
	vbox = gtk.VBox()

	InfoLabel = gtk.Label(_("Place APKs inside %s to select them." % os.path.join("APK", "IN")))
	vbox.pack_start(InfoLabel, False, False, 0)

	DecompileButton = gtk.RadioButton(None, _("Decompile"))
	CompileButton = gtk.RadioButton(DecompileButton, _("Compile"))
	vbox.pack_start(DecompileButton, False, False, 10)
	decname = []


	for apk in find_files(os.path.join(ScriptDir, "APK", "IN"), '*.apk'):
		name = os.path.basename(apk)
		NameBtn = gtk.CheckButton(name)
		NameBtn.connect("toggled", AddToList, decname, name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)


	vbox.pack_start(CompileButton, False, False, 10)

	comname = []

	for dec in os.listdir(os.path.join(ScriptDir, "APK", "DEC")):
		name = os.path.join(ScriptDir, "APK" , "DEC", dec)
		NameBtn = gtk.CheckButton(dec)
		NameBtn.connect("toggled", AddToList, comname, dec, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartButton = gtk.Button(_("Start (De)Compiling"))
	StartButton.connect("clicked", Start)
	vbox.pack_start(StartButton, False, False, 15)


	RefreshBtn = gtk.Button(_("Refresh") )
	RefreshBtn.connect("clicked", Refresh)
	vbox.pack_end(RefreshBtn, False, False, 10)



	DeComLabel = NewPage("(De)Compile", sw)
	DeComLabel.show_all()
	sw.add_with_viewport(vbox)
	notebook.insert_page(sw, DeComLabel)
	DeCompileWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)
	
	
def OptimizeImage():
	def Start(cmd):
		dialog = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(True)
		filter = gtk.FileFilter()
		filter.set_name("Images")
		filter.add_mime_type("image/png")
		filter.add_pattern("*.png")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			dialog.hide_all()
			for file in dialog.get_filenames():
				if Debug == True: print ("%s -o99 %s" %(OptPng, file))				
				SystemLog("%s -o99 %s &" %(OptPng, file))
			NewDialog(_("Optimize Images"),  _("Successfully optimized images"))
		elif response == gtk.RESPONSE_CANCEL:
			print _('Closed, no files selected')
		dialog.destroy()
	
	OptimizeImageWindow = window
	notebook = MainApp.notebook
	sw = gtk.ScrolledWindow()
	
	vbox = gtk.VBox()
	ChooseImageButton = gtk.Button(None, _("Choose Images and Optimize"))
	vbox.pack_start(ChooseImageButton, True, False, 5)
	ChooseImageButton.connect("clicked", Start)
	
	OptimizeLabel = NewPage(_("Optimize Images"), sw)
	OptimizeLabel.show_all()
	sw.add_with_viewport(vbox)
	notebook.insert_page(sw, OptimizeLabel)
	OptimizeImageWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

#TODO: Verify if this method are 100% running for all APK and reuse optimize function!
def OptimizeInside():
	def Start(cmd):
		Number = len(apkname)
		if Number == 0:
			NewDialog(_("ERROR"), _("No images inside %s. exit." % os.path.join("APK", "IN")))
		for num in range(0, Number):
			#Extract APK
			APK = apkname[num]
			APKPath = os.path.join(ScriptDir, "APK", "IN", APK)
			DstDir = os.path.join(ScriptDir, "APK", "EX", APK.replace('.apk', ''))
			print APKPath
			ExZip(APKPath, DstDir)
			
			#Do Optimize
			for apk_img in find_files(os.path.join(ScriptDir, "APK", "EX", APK.replace('.apk', '')), "*.png"):
				name = os.path.abspath(apk_img)
				if Debug == True: print ("%s -o99 %s" %(OptPng, name))		
				print ("%s -o99 \"%s\"" %(OptPng, name))		
				SystemLog("%s -o99 \"%s\"" %(OptPng, name))
				
			#Repackage APK
			DirPath = os.path.join(ScriptDir, "APK", "EX", APK.replace('.apk', ''))
			DstFile = zipfile.ZipFile(os.path.join(ScriptDir, "APK", "OUT", "Unsigned-" + APK), "w")
			for fpath in find_files(DirPath, "*"):
				f = fpath.replace(DirPath, '')
				DstFile.write(fpath, f)
			DstFile.close()
			#Do a CLEAN
			tree = os.path.join(ScriptDir, "APK", "EX", APK.replace('.apk', ''))
			shutil.rmtree(tree, True)

	notebook = MainApp.notebook
	OptInsideWindow = window
	vbox = gtk.VBox()
	sw = gtk.ScrolledWindow()

	apkname = []

	for apk in find_files(os.path.join(ScriptDir , "APK", "IN"), "*.apk"):
		name = os.path.basename(apk)
		NameBtn = gtk.CheckButton(name)
		NameBtn.connect("toggled", AddToList, apkname, name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartButton = gtk.Button(_("Do Optimize Inside APK"))
	StartButton.connect("clicked", Start)
	vbox.pack_start(StartButton, False, False, 10)

	OptInsideLabel = NewPage(_("Optimize Inside APK"), sw)
	OptInsideLabel.show_all()
	sw.add_with_viewport(vbox)
	notebook.insert_page(sw, OptInsideLabel)
	OptInsideWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)


def ExPackage():
	def Start(cmd):
		if ExtractButton.get_active():
			Number = len(exname)
			for num in range(0, Number):
				APK = exname[num]
				APKPath = os.path.join(ScriptDir, "APK", "IN", APK)
				DstDir = os.path.join(ScriptDir, "APK", "EX", APK.replace('.apk', ''))
				print APKPath
				ExZip(APKPath, DstDir)
				Refresh("cmd")
		elif RepackageButton.get_active():
			Number = len(repname)
			for num in range(0, Number):
				Ex = repname[num]
				DirPath = os.path.join(ScriptDir, "APK", "EX", Ex)
				DstFile = zipfile.ZipFile(os.path.join(ScriptDir, "APK", "OUT", "Unsigned-" + Ex + ".apk"), "w")
				for fpath in find_files(DirPath, "*"):
					f = fpath.replace(DirPath, '')
					DstFile.write(fpath, f)
				DstFile.close()

	def Refresh(cmd):
		KillPage("cmd", vbox)
		ExPackage()
		
	notebook = MainApp.notebook
	ExPackWindow = window
	vbox = gtk.VBox()

	InfoLabel = gtk.Label(_("Place APKs inside %s to select them." % os.path.join("APK", "IN")))
	vbox.pack_start(InfoLabel, False, False, 0)
	
	ExtractButton = gtk.RadioButton(None, "Extract")
	vbox.pack_start(ExtractButton, False, False, 10)

	exname = []

	for apk in find_files(os.path.join(ScriptDir, "APK", "IN"), "*.apk"):
		name = os.path.basename(apk)
		NameBtn = gtk.CheckButton(name)
		NameBtn.connect("toggled", AddToList, exname, name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	RepackageButton = gtk.RadioButton(ExtractButton, "Repackage")
	vbox.pack_start(RepackageButton, False, False, 10)

	repname = []

	for ex in os.listdir(os.path.join(ScriptDir, "APK", "EX")):
		name = os.path.join(ScriptDir, "APK", "EX", ex)
		NameBtn = gtk.CheckButton(ex)
		NameBtn.connect("toggled", AddToList, repname, ex, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartButton = gtk.Button(_("Extract / Repackage"))
	StartButton.connect("clicked", Start)
	vbox.pack_start(StartButton, False, False, 10)

	RefreshBtn = gtk.Button(_("Refresh") )
	RefreshBtn.connect("clicked", Refresh)
	vbox.pack_end(RefreshBtn, False, False, 10)
	sw = gtk.ScrolledWindow()
	
	ExPackLabel = NewPage("ExPackage", sw)
	ExPackLabel.show_all()
	sw.add_with_viewport(vbox)
	notebook.insert_page(sw, ExPackLabel)
	ExPackWindow.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Sign():
	def StartSign(cmd):
		print Std.get_group()
		name = [r for r in Std.get_group() if r.get_active()][0].get_label()
		key1 = os.path.join(ScriptDir, "Utils", name + ".x509.pem")
		key2 = os.path.join(ScriptDir, "Utils", name + ".pk8")
		Number = len(sign)
		for num in range(0, Number):
			APK = sign[num]
			APKName = APK.replace('Unsigned-', '')
			APKName = os.path.basename(APKName)
			APK = os.path.join(ScriptDir, "APK", APK)
			APKName = os.path.join(ScriptDir, "APK", "OUT", "Signed-" + APKName)
			if Debug == True: print("java -jar %s -w %s %s %s %s" %(SignJar, key1, key2, APK, APKName))
			SystemLog("java -jar %s -w %s %s %s %s" %(SignJar, key1, key2, APK, APKName))
		
		
	notebook = MainApp.notebook
	vbox = gtk.VBox()

	InfoLabel = gtk.Label(_("Place APKs inside %s to select them.\n\n\n" % os.path.join("APK", "IN")))
	vbox.pack_start(InfoLabel, False, False, 0)

	label = gtk.Label(_("Choose the key you want to sign with:"))
	vbox.pack_start(label, False, False, 10)
	Std = gtk.RadioButton(None, "None")
	for key in find_files(UtilDir, "*.pk8"):
		name = str(os.path.basename(key)).replace(".pk8", '')
		NameBtn = gtk.RadioButton(Std, name)
		vbox.pack_start(NameBtn, False, False, 2)
	[r for r in Std.get_group() if r.get_label() == "testkey"][0].set_active(True)

	label = gtk.Label("Choose the APK you want to sign:")
	vbox.pack_start(label, False, False, 10)

	sign = []

	for apk in find_files(os.path.join(ScriptDir, "APK", "OUT"), "*.apk"):
		name = os.path.join("OUT", os.path.basename(apk))
		NameBtn = gtk.CheckButton(name)
		NameBtn.connect("clicked", AddToList, sign, name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)
	
	for apk in find_files(os.path.join(ScriptDir, "APK", "IN"), "*.apk"):
		name = os.path.join("IN", os.path.basename(apk))
		NameBtn = gtk.CheckButton(name)
		NameBtn.connect("clicked", AddToList, sign, name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartBtn = gtk.Button("Sign")
	StartBtn.connect("clicked", StartSign)
	vbox.pack_start(StartBtn, False, False, 5)

	SignLabel = NewPage("Sign", vbox)
	SignLabel.show_all()
	notebook.insert_page(vbox, SignLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Zipalign():
	def StartZip(cmd):
		Numbers = len(zipapk)
		for num in range(0, Numbers):
			APK = zipapk[num]
			FullAPK = os.path.join(ScriptDir, "APK", APK)
			Name = os.path.basename(FullAPK)
			OutFile = os.path.join(ScriptDir, "APK", "OUT", "Aligned-" + Name)
			if Debug == True: print(ZipalignFile + " -fv 4 %s %s" %(FullAPK, OutFile))
			SystemLog("%s -fv 4 %s %s" %(ZipalignFile, FullAPK, OutFile))
	notebook = MainApp.notebook
	vbox = gtk.VBox()

	InfoLabel = gtk.Label(_("Place APKs inside %s to select them." % os.path.join("APK", "IN")))
	vbox.pack_start(InfoLabel, False, False, 10)
	
	zipapk = []

	for APK in find_files(os.path.join(ScriptDir, "APK"), "*.apk"):
		Name = APK.replace(os.path.join(ScriptDir, "APK", ''), '')
		NameBtn = gtk.CheckButton(Name)
		NameBtn.connect("toggled", AddToList, zipapk, Name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartBtn = gtk.Button(_("Zipalign"))
	StartBtn.connect("clicked", StartZip)
	vbox.pack_start(StartBtn, False, False, 5)
	
	
	ZipLabel = NewPage("Zipalign", vbox)
	ZipLabel.show_all()
	
	notebook.insert_page(vbox, ZipLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Install():
	def StartInst(cmd):
		print _("\n Waiting for device to connect via ADB...\n\n")
		SystemLog("adb wait-for-device")
		print _("Connected")
		Number = len(apk)
		for num in range(0, Number):
			APK = apk[num]
			SystemLog("adb install %s" % APK)

	ADB = str(commands.getoutput("adb version"))
	if not ADB.startswith("Android Debug Bridge version"):
		print _("The Android SDK is not installed. Do you want to install it now?\n")
		Choice = YesNo("Android SDK", _("Android SDK is not installed. \nDo you want to install it now?"))
		if not Choice == '0' :
			SDK()
		return None
	notebook = MainApp.notebook
	
	vbox = gtk.VBox()
	InfoLabel = gtk.Label(_("Place APKs inside %s to select them." % os.path.join("APK", "IN")))
	vbox.pack_start(InfoLabel, False, False, 0)
	
	apk = []

	for APK in find_files(os.path.join(ScriptDir, "APK"), "*.apk"):
		Name = APK
		NameBtn = gtk.CheckButton(Name)
		NameBtn.connect("toggled", AddToList, apk, Name, NameBtn)
		vbox.pack_start(NameBtn, False, False, 0)

	StartBtn = gtk.Button(_("Install"))
	StartBtn.connect("clicked", StartInst)
	vbox.pack_start(StartBtn, False, False, 5)
	
	
	InstLabel = NewPage("Install", vbox)
	InstLabel.show_all()
	
	notebook.insert_page(vbox, InstLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def BakSmali():
	def StartSmali(cmd):
		if Std.get_active():
			NewDialog("ERROR!", _("No smali folder selected!"))
		else:
			if not CstApi.get_text() == '':
				Api = "-a %s" % CstApi.get_text()
			else:
				Api = ''
			smali = [r for r in Std.get_group() if r.get_active()][0].get_label()
			OutputText = Output.get_text()
			if not OutputText.endswith(".dex"):
				OutputText = Output + ".dex"
			Out = os.path.join(ScriptDir, "Advance", "Smali", "OUT", OutputText)
			if Debug==True: print("java -jar %s %s -o %s" %(SmaliJar, os.path.join(ScriptDir, "Advance", "Smali", "Smali", smali), Out))
			print _("Smaling %s into %s with %s" %(os.path.join(ScriptDir, "Advance", "Smali", "Smali", smali), Out, Api))
			SystemLog("java -jar %s %s -o %s %s" %(SmaliJar, os.path.join(ScriptDir, "Advance", "Smali", "Smali", smali), Out, Api))

	def StartBakSmali(cmd):
		dialog = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(True)
		filter = gtk.FileFilter()
		filter.set_name("(o)dex")
		filter.add_mime_type("(o)dex")
		filter.add_pattern("*dex")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			dialog.hide()
			if not CstApi.get_text() == '':
				Api = "-a %s" % CstApi.get_text()
			else:
				Api = ''
			for dexfile in dialog.get_filenames():
				dexfilebase = os.path.basename(dexfile)
				dexname = dexfilebase.replace('.dex', '')
				dexname = dexname.replace('.odex', '')
				outdir = os.path.join(ScriptDir, "Advance", "Smali", "Smali", dexname)
				print _("Baksmaling %s to %s with %s" %(dexfile, outdir, Api))
				SystemLog("java -jar %s %s -o %s %s" %(BaksmaliJar, dexfile, outdir, Api))
			NewDialog(_("BakSmali"),  _("Successfully finished BakSmali"))
		elif response == gtk.RESPONSE_CANCEL:
			print _('Closed, no files selected')
		dialog.destroy()
				
	notebook = MainApp.notebook
	vbox = gtk.VBox()

	BakSmaliBtn = gtk.Button(_("Choose file(s) to Baksmali"))
	BakSmaliBtn.connect("clicked", StartBakSmali)
	vbox.pack_start(BakSmaliBtn, False, False, 3)

	label = gtk.Label( _("\n\n OR choose a Smali folder to Smali:"))
	vbox.pack_start(label, False, False, 0)

	Std = gtk.RadioButton(None, "Std")

	for Folder in os.listdir(os.path.join(ScriptDir, "Advance", "Smali", "Smali")):
		NameBtn = gtk.RadioButton(Std, Folder)
		vbox.pack_start(NameBtn, False, False, 0)

	Output = gtk.Entry()
	Output.set_text("out.dex")
	vbox.pack_start(Output, False, False, 0)

	SmaliBtn = gtk.Button("Smali")
	SmaliBtn.connect("clicked", StartSmali)
	vbox.pack_start(SmaliBtn, False, False, 3)

	space = gtk.Label("")
	vbox.pack_start(space, False, False, 10)

	CstApiLabel = gtk.Label( _("Choose a custom API Level:") )
	vbox.pack_start(CstApiLabel, False, False, 0)
	
	CstApi = gtk.Entry()
	vbox.pack_start(CstApi, False, False, 0)

	SmaliLabel = NewPage("BakSmali", vbox)
	SmaliLabel.show_all()
	notebook.insert_page(vbox, SmaliLabel)
	vbox.show_all()
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Deodex():
	MainApp.Out = None
	def DoDeodex(cmd, deo, bootclass=''):
		buildprop = open(os.path.join(ScriptDir, "Advance", "ODEX", "WORKING", "system", "build.prop"), "r")
		for line in buildprop.readlines():
			if line.startswith("ro.build.version.release=2.3.7"):
				global api
				version = line.replace('ro.build.version.release=', '')
				if version.startswith('2.3'):
					api = ' -a 12'
				elif version.startswith('3'):
					api = ' -a 13'
				elif version.startswith('4.0'):
					api = ' -a 14'
				elif version.split('.')[0] == '4' and version.split('.')[1] == '0' and version.split('.')[-1] >= 3:
					api = ' -a 15'
				elif version.startswith('4.1'):
					api = ' -a 16'

		WorkDir = os.path.join(ScriptDir, "Advance", "ODEX", "CURRENT")
		for apk in deo:
			ExDir = os.path.join(ScriptDir, "Advance", "ODEX", "WORKING")
			shutil.rmtree(WorkDir, True)
			os.makedirs(WorkDir)
			apk = os.path.join(ExDir, apk)
			odex = apk.replace('apk', 'odex')
			print _("Deodexing %s" % odex)
			if Debug == True: print _("BakSmaling %s" % odex)
			SystemLog("java -Xmx512m -jar %s%s%s -x %s -o %s" %(BaksmaliJar, bootclass, api, odex, WorkDir) )
			if Debug == True: print _("Smaling %s" % odex)
			SystemLog("java -Xmx512m -jar %s %s %s -o %s" %(SmaliJar, api, os.path.join(WorkDir, "*"), os.path.join(WorkDir, "classes.dex")))
			for fname in os.listdir(WorkDir):
				if not fname == "classes.dex":
					fname = os.path.join(WorkDir, fname)
					if os.path.isdir(fname):
						shutil.rmtree(fname)
					elif not os.path.isdir(fname):
						os.remove(fname)

			classes = os.path.join(WorkDir, "classes.dex")
			if os.path.exists(classes):
				if Debug == True: print _("Adding %s to %s" %(classes, apk))
				zipf = zipfile.ZipFile(apk, "a")
				zipf.write(classes, "classes.dex")
				zipf.close()


			os.remove(odex)

		print _("\n\nDeodexing done!\n\n")
		NewDialog("Deodex", _("Done!"))
			
	def DeodexStart(cmd):
		sw = gtk.ScrolledWindow()
		vbox = gtk.VBox()
		sw.add_with_viewport(vbox)
		deo = []
		UpdateZip = MainApp.Out
		print _("Extracting %s" % UpdateZip)
		ExDir = os.path.join(ScriptDir, "Advance", "ODEX", "WORKING", '')
		ExZip(UpdateZip, ExDir)
		if os.path.exists(os.path.join(ExDir, "system", "framework")):
			bootclass = " -d %s" % os.path.join(ExDir, "system", "framework")
		for filea in find_files(ExDir, "*.apk"):
			if os.path.exists(filea.replace('apk', 'odex')):
				files = filea.replace(ExDir, '')
				NameBtn = gtk.CheckButton(files)
				NameBtn.set_active(1)
				deo.append(filea)
				NameBtn.connect("toggled", AddToList, deo, files, NameBtn)
				vbox.pack_start(NameBtn, False, False, 0)
		StartButton = gtk.Button("Start deodex!")
		StartButton.connect("clicked", DoDeodex, deo, bootclass)
		vbox.pack_start(StartButton, False, False, 0)
		DeodexLabel = NewPage( _("Start deodex") , sw)
		DeodexLabel.show_all()
		notebook.insert_page(sw, DeodexLabel)
		window.show_all()
		notebook.set_current_page(notebook.get_n_pages() - 1)
	notebook = MainApp.notebook
	vbox = gtk.VBox(False, 0)

	RomChooser = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

	RomChooseBtn = gtk.Button("Choose ROM to deodex")
	RomChooseBtn.connect("clicked", GetFile, RomChooser, [RomChooseBtn], False, ".zip")
	vbox.pack_start(RomChooseBtn, False, False, 0)

	DoneBtn = gtk.Button( _("Done") )
	DoneBtn.connect("clicked", DeodexStart)
	vbox.pack_start(DoneBtn, False, False, 3)
	
	DeodexLabel = NewPage("De-ODEX", vbox)
	DeodexLabel.show_all()
	notebook.insert_page(vbox, DeodexLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Odex():
	MainApp.Out = None
	def DoOdex(cmd, odex, bootclass=''):
		buildprop = open(os.path.join(ScriptDir, "Advance", "ODEX", "WORKING", "system", "build.prop"), "r")
		for line in buildprop.readlines():
			if line.startswith("ro.build.version.release=2.3.7"):
				global api
				version = line.replace('ro.build.version.release=', '')
				if version.startswith('2.3'):
					api = ' -a 12'
				elif version.startswith('3'):
					api = ' -a 13'
				elif version.startswith('4.0'):
					api = ' -a 14'
				elif version.startswith('4.1'):
					api = ' -a 15'
		for apk in odex:
			ExDir = os.path.join(ScriptDir, "Advance", "ODEX", "WORKING")
			WorkDir = os.path.join(ScriptDir, "Advance", "ODEX", "CURRENT")
			shutil.rmtree(WorkDir, True)
			os.makedirs(WorkDir)
			apk = os.path.join(ExDir, apk)
			odex = apk.replace('apk', 'odex')

			print _("Odexing %s" % odex)
			if "classes.dex" in zipfile.ZipFile(apk).namelist():
				zipfile.ZipFile(apk).extract("classes.dex", WorkDir)
				Classes = os.path.join(WorkDir, "classes.dex")
				shutil.move(Classes, odex)
			else:
				print _("Skipped %s " % odex)
			SystemLog("%s d -y -tzip %s classes.dex" %(sz, apk) )

		print _("\n\nOdexing done!\n\n")
		NewDialog("Odex", _("Done!"))
			
	def OdexStart(cmd):
		sw = gtk.ScrolledWindow()
		vbox = gtk.VBox()
		sw.add_with_viewport(vbox)
		odex = []
		UpdateZip = MainApp.Out
		print _("Extracting %s" % UpdateZip)
		ExDir = os.path.join(ScriptDir, "Advance", "ODEX", "WORKING", '')
		ExZip(UpdateZip, ExDir)
		if os.path.exists(os.path.join(ExDir, "system", "framework")):
			bootclass = " -d %s" % os.path.join(ExDir, "system", "framework")
		for filea in find_files(ExDir, "*.apk"):
			if not os.path.exists(filea.replace('apk', 'odex')):
				files = filea.replace(ExDir, '')
				NameBtn = gtk.CheckButton(files)
				NameBtn.set_active(1)
				odex.append(filea)
				NameBtn.connect("toggled", AddToList, odex, files, NameBtn)
				vbox.pack_start(NameBtn, False, False, 0)
		StartButton = gtk.Button("Start Odex!")
		StartButton.connect("clicked", DoOdex, odex, bootclass)
		vbox.pack_start(StartButton, False, False, 0)
		DeodexLabel = NewPage( _("Start deodex") , sw)
		DeodexLabel.show_all()
		notebook.insert_page(sw, DeodexLabel)
		window.show_all()
		notebook.set_current_page(notebook.get_n_pages() - 1)

	notebook = MainApp.notebook
	vbox = gtk.VBox(False, 0)

	RomChooser = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

	RomChooseBtn = gtk.Button("Choose ROM to odex")
	RomChooseBtn.connect("clicked", GetFile, RomChooser, [RomChooseBtn], False, ".zip")
	vbox.pack_start(RomChooseBtn, False, False, 0)

	DoneBtn = gtk.Button( _("Done") )
	DoneBtn.connect("clicked", OdexStart)
	vbox.pack_start(DoneBtn, False, False, 20)
	
	DeodexLabel = NewPage("Re-ODEX", vbox)
	DeodexLabel.show_all()
	notebook.insert_page(vbox, DeodexLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def BinaryPort():
	def ChooseFile(cmd, Chooser, Btn, kind):
			response = Chooser.run()
			if response == gtk.RESPONSE_OK:
				if kind == 'ToROM':
					global ToROM
					ToROM = Chooser.get_filename()
					Btn.set_label("IN: %s" % ToROM)
				if kind == 'ROM':
					global ROM
					ROM = Chooser.get_filename()
					Btn.set_label("ROM: %s" % ROM)
			Chooser.destroy()





	def Start(cmd):
		zipfile.ZipFile(ToROM).extractall(path=InDirTo)
		buildprop = open(os.path.join(InDirTo, "system", "build.prop"))
		for line in buildprop.readlines():
			if line.startswith("ro.build.version.release="):
				Version = line.replace("ro.build.version.release=", '')
				Ver = list(Version)
				StockVer = Ver[0] + Ver[1] + Ver[2]
		zipfile.ZipFile(ROM).extractall(path=InDirFrom)

		buildprop = open(os.path.join(InDirFrom, "system", "build.prop"))
		for line in buildprop.readlines():
			if line.startswith("ro.build.version.release="):
				Version = line.replace("ro.build.version.release=", '')
				Ver = list(Version)
				ROMVer = Ver[0] + Ver[1] + Ver[2]
		if not StockVer == ROMVer:
			NewDialog( _("Info"), _("Choose a ROM you want to port to your device with version %s.\n\n Version of your BASE: %s\nVersion of the ROM you want to port: %s" %(StockVer, StockVer, ROMVer)) )
		else:
			def Copy(From, To):
				if os.path.exists(To):
					print _("Removing %s" % To)
					if os.path.isdir(To):
						shutil.rmtree(To, True)
					else:
						os.remove(To)
				if os.path.exists(From):
					print _("Copying %s to %s" %(From, To))
					if os.path.isdir(From):
						shutil.copytree(From, To)
					else:
						shutil.copy(From, To)
			Copy(InDirTo, WorkDir)
			if os.path.exists(BackDir):
				shutil.rmtree(BackDir)
			os.mkdir(BackDir)
			for apk in ['Stk.apk', 'VpnServices.apk', 'Camera.apk', 'Bluetooth.apk']:
				apk = os.path.join(InDirFrom, "system", "app", apk)
				if os.path.exists(apk):
					shutil.copy(apk, BackDir)
					odex = apk.replace('apk', 'odex')
					if os.path.exists(odex):
						shutil.copy(odex, BackDir)
						
			Copy(os.path.join(InDirFrom, "system", "app"), os.path.join(WorkDir, "system", "app"))
			Copy(os.path.join(InDirFrom, "system", "framework"), os.path.join(WorkDir, "system", "framework"))
			Copy(os.path.join(InDirFrom, "system", "media"), os.path.join(WorkDir, "system", "media"))
			Copy(os.path.join(InDirFrom, "system", "fonts"), os.path.join(WorkDir, "system", "fonts"))
			Copy(os.path.join(InDirFrom, "data"), os.path.join(WorkDir, "data"))
			Copy(os.path.join(InDirFrom, "system", "lib", "libandroid_runtime.so"), os.path.join(WorkDir, "system", "lib", "libandroid_runtime.so"))
			for x in os.listdir(BackDir):
				Copy(os.path.join(BackDir, x), os.path.join(WorkDir, "system", "app", x))
	notebook = MainApp.notebook
	vbox = gtk.VBox(False, 0)
	InDirTo = os.path.join(ScriptDir, "Advance", "PORT", "TO")
	InDirFrom = os.path.join(ScriptDir, "Advance", "PORT", "ROM")
	WorkDir = os.path.join(ScriptDir, "Advance", "PORT", "WORKING")
	BackDir = os.path.join(ScriptDir, "Advance", "PORT", "Backup")
	ToFileDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  	buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	ToExtractBtn = gtk.Button( _("Choose ROM you want to port to:"))
	ToExtractBtn.connect("clicked", ChooseFile, ToFileDial, ToExtractBtn, "ToROM")
	RomFileDial = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  	buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	RomFileBtn = gtk.Button( _("Choose the ROM you want to port") )
	RomFileBtn.connect("clicked", ChooseFile, RomFileDial, RomFileBtn, 'ROM')
	vbox.pack_start(ToExtractBtn, False, False, 0)
	vbox.pack_start(RomFileBtn, False, False, 0)

	StartBtn = gtk.Button( _("Start porting") )
	StartBtn.connect("clicked", Start)
	vbox.pack_start(StartBtn, False, False, 30)
	BinaryLabel = NewPage( _("Binary port"), vbox)
	BinaryLabel.show_all()
	notebook.insert_page(vbox, BinaryLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def Compile():
	MainApp.ScriptFile = FullFile
	MainApp.Icon = os.path.join(ScriptDir, "images", "icon.ico")
	def CstPy(cmd):
		MainApp.ScriptFile = FileChoose(CustomPythonFile, ".py")
	def CstIco(cmd):
		MainApp.Icon = FileChoose(CustomIcon, ".ico")
	def StartCompile(cmd):
		ScriptFile = MainApp.ScriptFile
		PyDir = os.path.join(Home, "PyInstallerTmp")
		PyFile = os.path.join(PyDir + 'PyInstaller.zip')
		PyInstDir = os.path.join(Home, "PyInstaller")
		icon = "-i %s" % MainApp.Icon

		if not os.path.exists(PyDir):
			New = True
			os.mkdir(PyDir)
			print("%s made" % PyDir)
		else:
			New = False
			print("%s already exists" % PyDir)


		Name = "StudioAndroid"
		if not os.path.basename(ScriptFile) == "SA.py":
			Name = str(os.path.basename(ScriptFile)).replace('.py', '')

		if New == True:
			urllib.urlretrieve('https://github.com/pyinstaller/pyinstaller/zipball/develop', PyFile)
			ExZip(PyFile, PyDir)
			os.remove(PyFile)
		DwnDir = os.path.join(PyDir, os.listdir(PyDir)[0])

		if not os.path.exists(PyInstDir):
			os.mkdir(PyInstDir)
			print("%s made" % PyInstDir)
		else:
			print("%s already exists" % PyInstDir)

		if New == True:
			for x in os.listdir(DwnDir):
				CopySrc = os.path.join(DwnDir, x)
				CopyDst = os.path.join(PyInstDir, x)
				if not os.path.exists(CopyDst):
					if os.path.isdir(CopySrc):
						shutil.copytree(CopySrc, CopyDst)
					else:
						shutil.copy(CopySrc, CopyDst)

		os.chdir(PyInstDir)
		
		if OS == 'Win':
			PythonF = os.path.join(PythonDir, "python.exe")

			print _("Python = %s" % PythonF)

			SystemLog("%s pyinstaller.py -y -F %s %s -n %s" %(PythonF, ScriptFile, icon, Name))
		elif OS == 'Mac':
			SystemLog("python pyinstaller.py -y -F %s -n %s" %(ScriptFile, Name))
		else:
			SystemLog("python pyinstaller.py -y -F %s -n %s" %(ScriptFile, Name))


		CompiledDir = os.path.join(PyInstDir, Name, "dist")
		compiled = os.path.join(CompiledDir, os.listdir(CompiledDir)[0])

		shutil.copy(compiled, ScriptDir)
	
	notebook = MainApp.notebook
	vbox = gtk.VBox()

	label = gtk.Label("\nWelcome!\nThis is my home made tool to compile Python Scripts on any OS.\n")
	vbox.pack_start(label, False, False, 0)

	CustomPythonFile = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	CustomPyBtn = gtk.Button("Choose .py file (default SA.py)")
	CustomPyBtn.connect("clicked", CstPy)
	vbox.pack_start(CustomPyBtn, False, False, 0)

	CustomIcon = gtk.FileChooserDialog("Open..",  None, gtk.FILE_CHOOSER_ACTION_OPEN, 
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	CustomIcon = gtk.Button("Choose .ico file (default icon.ico)")
	CustomIcon.connect("clicked", CstIco)
	vbox.pack_start(CustomIcon, False, False, 0)

	StartComp = gtk.Button("Start compiling...")
	StartComp.connect("clicked", StartCompile)
	vbox.pack_start(StartComp, False, False, 40)

	CompLabel = NewPage("Compile", vbox)
	CompLabel.show_all()
	notebook.insert_page(vbox, CompLabel)
	vbox.show_all()
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def ADBConfig():
	def Configure(cmd):
		active = [r for r in ConnectBtn.get_group() if r.get_active()][0].get_label()
		if not active == "Connect via IP:":
			GlobalData.AdbOpts = "-s %s" % active
		else:
			IPAdressPort = IP.get_text()
			Port = IPAdressPort.split(":")[1]
			#print("%s tcpip %s" %(adb, Port))
			#SystemLog("%s tcpip %s" %(adb, Port))
			
			SystemLog("%s connect %s" %(adb, IPAdressPort))
			GlobalData.AdbOpts = "-s %s" % active
			
	notebook = MainApp.notebook
	vbox = gtk.VBox()
	AdbConfigLabel = NewPage("Configure ADB",vbox)

	label = gtk.Label("Please select your device below:")
	vbox.pack_start(label, False, False, 15)

	devices = []

	SystemLog("%s start-server" % adb)
	adbc = commands.getoutput("%s devices" % adb).split('\n')[1:-1]
	for line in adbc:
		devicen = line.split('\t')[0]
		devices.append(devicen)

	NameBtn = None
	for device in devices:
		NameBtn = gtk.RadioButton(NameBtn, device)
		vbox.pack_start(NameBtn)

	ConnectHbox = gtk.HBox(True)
	ConnectBtn = gtk.RadioButton(NameBtn, "Connect via IP:")
	ConnectHbox.pack_start(ConnectBtn)
	IP = gtk.Entry()
	IP.set_text("IP Adress:PORT")
	ConnectHbox.pack_start(IP)
	vbox.pack_start(ConnectHbox)

	ConfigureBtn = gtk.Button("Configure")
	ConfigureBtn.connect("clicked", Configure)
	vbox.pack_start(ConfigureBtn, False)

	notebook.insert_page(vbox, AdbConfigLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def LogCat():
	notebook = MainApp.notebook
	vbox = gtk.VBox()
	sw = gtk.ScrolledWindow()
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

	encoding = locale.getpreferredencoding()
	utf8conv = lambda x : unicode(x, encoding).encode('utf8')


	gobject.threads_init()
	gtk.gdk.threads_init()

	LogCatLabel = NewPage("Logcat",vbox)

	def read_output(view, buffer, command):
		stdin, stdouterr = os.popen4(command)
		while 1:
			line = stdouterr.readline()
			if not line:
				break
			gtk.gdk.threads_enter()
			iter = buffer.get_end_iter()
			buffer.place_cursor(iter)
			buffer.insert(iter, utf8conv(line))
			view.scroll_to_mark(buffer.get_insert(), 0.1)
			gtk.gdk.threads_leave()


	TextBox = gtk.TextView()
	buff = TextBox.get_buffer()
	TextBox.set_wrap_mode(gtk.WRAP_WORD)
	TextBox.set_editable(False)
	TextBox.set_cursor_visible(True)
	
	sw.add(TextBox)
	vbox.pack_start(sw)

	notebook.insert_page(vbox, LogCatLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

	command = "%s logcat" % adb
	thr = threading.Thread(target= read_output, args=(TextBox, buff, command))
	thr.start()

def BuildProp():
	def Save(cmd):
		textbuffer = TextBox.get_buffer()
		text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
		NewBuildProp = os.path.join(ScriptDir, 'ADB', 'new-build.prop')
		open(NewBuildProp, "w").write(text)
	def Pull(cmd):
		SystemLog("'%s' pull '/system/build.prop' '%s'" %(adb, os.path.join(ScriptDir, 'ADB', 'build.prop')))
		textbuffer.set_text(open(os.path.join(ScriptDir, 'ADB', 'build.prop'), "r").read())
		TextBox.set_buffer(textbuffer)
	def Reload(cmd):
		if os.path.exists(os.path.join(ScriptDir, 'ADB', 'new-build.prop')):
			textbuffer.set_text(open(os.path.join(ScriptDir, 'ADB', 'new-build.prop'), "r").read())
			TextBox.set_buffer(textbuffer)
		elif not os.path.exists(os.path.join(ScriptDir, 'ADB', 'new-build.prop')) and os.path.exists(os.path.join(ScriptDir, 'ADB', 'build.prop')):
			textbuffer.set_text(open(os.path.join(ScriptDir, 'ADB', 'build.prop'), "r").read())
			TextBox.set_buffer(textbuffer)
	def Push(cmd):
		NewBuildProp = os.path.join(ScriptDir, 'ADB', 'new-build.prop')
		Save(None)

		SystemLog("%s root" % adb)
		SystemLog("%s wait-for-device" % adb)
		SystemLog("%s push %s /system/build.prop" %(adb, NewBuildProp) )
			
			
		
	notebook = MainApp.notebook
	vbox = gtk.VBox()
	BuildPropLabel = NewPage("Build.prop",vbox)
	sw = gtk.ScrolledWindow()

	if not os.path.exists(os.path.join(ScriptDir, 'ADB', 'build.prop')):
		SystemLog("'%s' pull '/system/build.prop' '%s'" %(adb, os.path.join(ScriptDir, 'ADB', 'build.prop')))

	TextBox = gtk.TextView()
	TextBox.set_wrap_mode(gtk.WRAP_WORD)
	TextBox.set_editable(True)
	TextBox.set_cursor_visible(True)

	textbuffer = gtk.TextBuffer()
	textbuffer.set_text(open(os.path.join(ScriptDir, 'ADB', 'build.prop'), "r").read())
	TextBox.set_buffer(textbuffer)
	
	sw.add_with_viewport(TextBox)
	vbox.pack_start(sw)

	hbox = gtk.HBox(True)

	SaveBtn = gtk.Button("Save")
	SaveBtn.connect("clicked", Save)
	hbox.pack_start(SaveBtn, False)

	PullBtn = gtk.Button("Pull un-edited")
	PullBtn.connect("clicked", Pull)
	hbox.pack_start(PullBtn, False)

	ReloadEdited = gtk.Button("Reload edited")
	ReloadEdited.connect("clicked", Reload)
	hbox.pack_start(ReloadEdited, False)

	PushBtn = gtk.Button("Push saved build.prop")
	hbox.pack_start(PushBtn, False)

	vbox.pack_end(hbox, False)
	

	notebook.insert_page(vbox, BuildPropLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)


def BackupRestore():
	def BackupData(cmd):
		dir = date()
		os.mkdir(os.path.join(ScriptDir, 'ADB', dir))
		for x in ['/data/misc/wifi/wpa_supplicant.conf', '/data/wifi/bcm_supp.conf', '/data/misc/wifi/wpa.conf', '/data/data/com.android.providers.contacts/databases/contacts2.db', '/data/data/com.android.providers.telephony/databases/mmssms.db']:
			
			basename = x.split('/')[-1]
			SystemLog("%s pull %s %s" %(adb, x, os.path.join(ScriptDir, 'ADB', dir, basename)))
	def RestoreData(cmd, NameBtn):
		if not NameBtn == None:
			active = [r for r in NameBtn.get_group() if r.get_active()][0].get_label()
			fullpath = os.path.join(ScriptDir, 'ADB', active)
		for x in ['/data/misc/wifi/wpa_supplicant.conf', '/data/wifi/bcm_supp.conf', '/data/misc/wifi/wpa.conf', '/data/data/com.android.providers.contacts/databases/contacts2.db', '/data/data/com.android.providers.telephony/databases/mmssms.db']:
			basename = x.split('/')[-1]
			filepath = os.path.join(fullpath, basename)
			SystemLog("%s push %s %s" %(adb, filepath, x))
	def Backup(cmd):
		opts = []
		if BackupAPKs.get_active():opts.append('-apk')
		if Shared.get_active():opts.append('-shared')
		if All.get_active():opts.append('-all')
		if DecludeSystemApps.get_active(): opts.append('-nosystem')
		options = ' '.join(opts)
		SystemLog("%s backup -f %s %s" %(adb, os.path.join(ScriptDir, 'ADB', '%s.ab' % date()), options))
		NewDialog(_("Warning!"), _("Please copy your backups from the ADB directory to a safe place elsewhere"))
	def Restore(cmd):
		file = os.path.join(ScriptDir, 'ADB', [r for r in NameBtn.get_group() if r.get_active()][0].get_label()) + '.ab'
		SystemLog("%s restore %s" %(adb, file))
	notebook = MainApp.notebook
	hbox = gtk.HBox(True)
	frame = gtk.Frame("Backup apps and/or data")
	vbox = gtk.VBox()
	frame.add(vbox)
	hbox.pack_start(frame)
	BackupRestoreLabel = NewPage("Backup/Restore",hbox)

	BackupAPKs = gtk.CheckButton(_("Backup the APKs too"))
	vbox.pack_start(BackupAPKs)
	
	Shared = gtk.CheckButton(_("Backup shared storage"))
	vbox.pack_start(Shared)	
	
	All = gtk.CheckButton(_("Backup ALL applications"))
	vbox.pack_start(All)
	
	DecludeSystemApps = gtk.CheckButton(_("Declude System apps"))
	vbox.pack_start(DecludeSystemApps)
	
	BackupBtn = gtk.Button(_("Backup (get a cup of coffee)"))
	BackupBtn.connect("clicked", Backup)
	vbox.pack_start(BackupBtn, False)


	NameBtn = None
	frame2 = gtk.Frame("Restore backups")
	vbox2 = gtk.VBox()
	frame2.add(vbox2)
	for x in find_files(os.path.join(ScriptDir, 'ADB'), "*.ab"):
		for file in find_files(os.path.join(ScriptDir, 'ADB'), "*.ab"):
			BaseFile = os.path.basename(file).replace('.ab', '')
			NameBtn = gtk.RadioButton(NameBtn, BaseFile)
			vbox2.pack_start(NameBtn)

	if not NameBtn == None:
		RestoreBtn = gtk.Button(_("Restore (get a cup of coffee)"))
		RestoreBtn.connect("clicked", Restore)
		vbox2.pack_start(RestoreBtn, False)
		hbox.pack_start(frame2)

	vbox3 = gtk.VBox()
	frame3 = gtk.Frame(_("Backup Contacts, SMS, WiFi"))
	frame3.add(vbox3)

	BackupDataBtn = gtk.Button(_("Backup Contacts, Wifi, SMS"))
	BackupDataBtn.connect("clicked", BackupData)
	vbox3.pack_start(BackupDataBtn, False)

	NameBtn = None
	for x in os.listdir(os.path.join(ScriptDir, 'ADB')):
		if os.path.exists(os.path.join(ScriptDir, 'ADB', x, '')):
			NameBtn = gtk.RadioButton(NameBtn, x)
			vbox3.pack_start(NameBtn)

	if not NameBtn == None:
		RestoreDataSpecBtn = gtk.Button(_("Restore Contacts, WiFi, SMS"))
		RestoreDataSpecBtn.connect("clicked", RestoreData, NameBtn)
		vbox3.pack_end(RestoreDataSpecBtn, False)


	hbox.pack_start(frame3)

	notebook.insert_page(hbox, BackupRestoreLabel)
	window.show_all()
	notebook.set_current_page(notebook.get_n_pages() - 1)

def AdbFE():
	class Data():
		PrevDir = '/sdcard/'
		MainPrevDir = ScriptDir
	def Previous(cmd, type='Android'):
		if type == 'Android':
			Update(None, Data.PrevDir, sw, type)
		elif type == 'PC':
			Update(None, Data.MainPrevDir, SwPC, type)
	def Refresh(cmd, sw, type='Android'):
		if type == 'Android':
			Update(None, Data.CurrentDir, sw, type)
		elif type == 'PC':
			Update(None, Data.MainCurrentDir, sw, type)
	def Push(cmd, Btn):
		print("%s -> %s" %(Btn.realname, Data.CurrentDir))
		SystemLog("%s push '%s' '%s'" %(adb, Btn.realname, Data.CurrentDir))
		Refresh(None, sw, 'Android')
	def Pull(cmd, Btn):
		print("%s -> %s" %(Btn.realname, Data.MainCurrentDir))
		SystemLog("%s pull '%s' '%s'" %(adb, Btn.realname, Data.MainCurrentDir))
		Refresh(None, SwPC, 'PC')		
	def Update(cmd, Dir, sw, type='Android'):
		NewDir = os.path.join(Dir, '')
		child = sw.get_child()
		if not child == None: child.destroy()
		vbox1 = gtk.VBox()
		sw.add_with_viewport(vbox1)
		if type == 'Android':
			Data.PrevDir = os.path.dirname(os.path.normpath(NewDir))
			Data.CurrentDir = NewDir
			for x in [["'%s' shell find '%s' -maxdepth 1 -type d | sort -d" %(adb, NewDir), True], ["'%s' shell find '%s' -maxdepth 1 -type f | sort -d" %(adb, NewDir), False]]:
				cmd = x[0]
				Dir = x[1]
				for filen in str(commands.getoutput(cmd)).split('\n'):
					FileName = str(filen).replace('\r', '')
					BaseName = os.path.basename(os.path.normpath(FileName))
					if FileName == NewDir:
						continue
					box = gtk.HBox()
					image = gtk.Image()
					if Dir == True and BaseName.startswith("."): imf = os.path.join(ScriptDir, "images", "folder.png")
					elif Dir == True: imf = os.path.join(ScriptDir, "images", "folder-brown.png")
					else: imf = os.path.join(ScriptDir, "images", "file.png")
					image.set_from_file(imf)
					Btn = gtk.Button(BaseName)
					Btn.realname = FileName
					if Dir == True:
						Btn.connect("clicked", Update, FileName, sw, 'Android')
					Btn.set_relief(gtk.RELIEF_NONE)
					# Set PULL BTN
					PullBtn = gtk.Button()
					im = gtk.Image()
					im.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
					PullBtn.set_image(im)
					PullBtn.connect("clicked", Pull, Btn)
					box.pack_start(PullBtn, False)
					# 
					box.pack_start(image, False, False, 4)
					box.pack_start(Btn, False)
					vbox1.pack_start(box, False, False, 0)
			location.set_text(NewDir)
		else:
			Data.MainPrevDir = os.path.dirname(os.path.normpath(NewDir))
			Data.MainCurrentDir = NewDir
			dirlist = []
			for dir in os.listdir(NewDir):
				if os.path.isdir(os.path.join(NewDir, dir)): dirlist.append(os.path.join(NewDir, dir))
			dirlist.sort()
			filelist = []
			for file in os.listdir(NewDir):
				if not os.path.isdir(os.path.join(NewDir, file)): filelist.append(os.path.join(NewDir, file))
			filelist.sort()
			for files in dirlist + filelist:
				BaseName = os.path.basename(os.path.normpath(files))
				box = gtk.HBox()
				image = gtk.Image()
				if BaseName.startswith("."): imf = os.path.join(ScriptDir, "images", "folder.png")
				elif os.path.isdir(files): imf = os.path.join(ScriptDir, "images", "folder-brown.png")
				else: imf = os.path.join(ScriptDir, "images", "file.png")
				image.set_from_file(imf)
				Btn = gtk.Button(BaseName)
				Btn.realname = files
				if os.path.isdir(files): Btn.connect("clicked", Update, files, SwPC, 'PC')
				Btn.set_relief(gtk.RELIEF_NONE)
				#Set PUSH Button
				PushBtn = gtk.Button()
				im = gtk.Image()
				im.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
				PushBtn.set_image(im)
				PushBtn.connect("clicked", Push, Btn)
				box.pack_start(PushBtn, False)
				#
				box.pack_start(image, False, False, 4)
				box.pack_start(Btn, False)
				vbox1.pack_start(box, False, False, 0)
			if dirlist + filelist == []:
				label = gtk.Label(_("Empty directory..."))
				vbox1.pack_start(label)
				
			
			LocationPC.set_text(NewDir)
		sw.show_all()
		
	notebook = MainApp.notebook
	vbox = gtk.VBox()
	AdbFELabel = NewPage("ADB FE",vbox)
	AdbFELabel.show_all()

	SwPC = gtk.ScrolledWindow()
	sw = gtk.ScrolledWindow()

	# Set Android frame
	hbox = gtk.HBox()
	location = gtk.Label('')
	BackBtn = gtk.Button()
	BackBtn.connect("clicked", Previous, "Android")
	BackImage = gtk.Image()
	BackImage.set_from_file(os.path.join(ScriptDir, "images", "back.png"))
	BackBtn.set_image(BackImage)
	RefreshImage = gtk.Image()
	RefreshImage.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
	RefreshBtn = gtk.Button()
	RefreshBtn.set_image(RefreshImage)
	RefreshBtn.connect("clicked", Refresh, sw, 'Android')
	hbox.pack_start(BackBtn, False, False, 0)
	hbox.pack_start(RefreshBtn, False, False, 0)
	hbox.pack_start(location, False, False, 4)
	vbox.pack_start(hbox, False, False, 0)
	
	# Set PC frame
	LocationPC = gtk.Label('')
	PcBackBtn = gtk.Button()
	PcBackBtn.connect("clicked", Previous, "PC")
	image = gtk.Image()
	image.set_from_file(os.path.join(ScriptDir, "images", "back.png"))
	PcBackBtn.set_image(image)
	PcRefreshImage = gtk.Image()
	PcRefreshImage.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
	PcRefreshBtn = gtk.Button()
	PcRefreshBtn.set_image(PcRefreshImage)
	PcRefreshBtn.connect("clicked", Refresh, SwPC, 'PC')
	hbox.pack_end(PcBackBtn, False, False, 0)
	hbox.pack_end(PcRefreshBtn, False, False, 0)
	hbox.pack_end(LocationPC, False, False, 4)


	HboxFM = gtk.HBox()
	vbox1 = gtk.VBox()
	sw.add_with_viewport(vbox1)
	HboxFM.pack_start(sw)

	HboxFM.pack_end(SwPC)
	Update(None, ScriptDir, SwPC, 'PC')

	Update(None, '/sdcard', sw, 'Android')

	vbox.pack_start(HboxFM)
	vbox.show_all()

	notebook.insert_page(vbox, AdbFELabel)
	notebook.set_current_page(notebook.get_n_pages() - 1)
	window.show_all()
	

def Changelog():
	ChangeWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	ChangeWindow.set_size_request(700, 600)
	ChangeWindow.set_title("StudioAndroid - Changelog")
	sw = gtk.ScrolledWindow()
	ChangeWindow.add(sw)

	changelog = open(os.path.join(ScriptDir, "changelog"), "r")
	Text = changelog.read()
	Label = gtk.Label(Text)

	sw.add_with_viewport(Label)
	ChangeWindow.show_all()

def Log():
	def DeleteLog(cmd):
		os.remove(os.path.join(ScriptDir, "log")) 
	LogWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	LogWindow.set_size_request(700, 600)
	LogWindow.set_title("StudioAndroid - Log")
	vbox = gtk.VBox(False, 4)
	sw = gtk.ScrolledWindow()
	vbox.pack_start(sw)
	LogWindow.add(vbox)

	log = open(os.path.join(ScriptDir, "log"), "r")
	Text = log.read()
	Label = gtk.Label(Text)
	Label.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
	Label.set_selectable(True)

	sw.add_with_viewport(Label)
	DeleteButton = gtk.Button( _("Delete log") )
	DeleteButton.connect("clicked", DeleteLog)
	vbox.pack_start(DeleteButton, False)
	vbox.show_all()
	LogWindow.show_all()

def Bug(cmd=''):
	text = "[QUOTE=log]%s[/QUOTE]\nHere is my log!" % open(os.path.join(ScriptDir, "log"), "r").read()
	clipboard = gtk.Clipboard()
	clipboard.set_text(text)
	NewDial = NewDialog("BUGREPORT", _("The log content has been copied to the clipboard"
				"\nPlease paste it in the reply that will be opened now!"))

	webbrowser.open("http://forum.xda-developers.com/newreply.php?do=newreply&noquote=1&p=22414621")

def Help():
	Web.open("http://forum.xda-developers.com/showpost.php?p=23546408&postcount=9")

def Update():
	if os.path.exists(os.path.join(ConfDir, "Update.zip")):
		print _("Removing old update.zip")
		os.remove(os.path.join(ConfDir, "Update.zip"))
	print _("Retrieving new Update.zip")
	urllib.urlretrieve("https://github.com/mDroidd/StudioAndroid-GtkUI/zipball/master", os.path.join(ConfDir, "Update.zip"))
	if os.path.exists(os.path.join(Home, "StudioAndroidUpdate")):
		print _("Removing old UpdateDir")
		shutil.rmtree(os.path.join(Home, "StudioAndroidUpdate"))
	print _("Extracting Update.zip")
	ExZip(os.path.join(ConfDir, "Update.zip"),os.path.join(Home, "StudioAndroidUpdate"))
	if os.path.exists(os.path.join(Home, "StudioAndroid")):
		print _("Removing old %s" % os.path.join(Home, "StudioAndroid"))
		shutil.rmtree(os.path.join(Home, "StudioAndroid"))
	else:
		shutil.rmtree(ScriptDir)
	UpdDir = os.path.join(Home, "StudioAndroidUpdate")
	UpdCont = os.listdir(UpdDir)[0]
	FullUpdDir = os.path.join(UpdDir, UpdCont)
	shutil.copytree(FullUpdDir, os.path.join(Home, "StudioAndroid"))
	shutil.rmtree(UpdDir)
	NewDialog(_("Update"), _("Succesfully updated to the newest version :)"))
	os.chdir(os.path.join(Home, "StudioAndroid"))
	if OS == "Win":
		SystemLog("start StudioWindows.exe")
	elif OS == "Lin":
		os.chmod(os.path.join(Home, "StudioAndroid", "StudioLinux"), 0755)
		SystemLog("./StudioLinux")
	elif OS == "Mac":
		os.chmod(os.path.join(Home, "StudioAndroid", "StudioMac"), 0755)
		SystemLog("./StudioMac")

if not os.path.exists(os.path.join(Home, ".SA", "Language")):
	window.destroy()
	window2.show_all()

if not FirstRun == False:
	callback("cmd", "Utils")

def main():
	try:
		gtk.main()
	except KeyboardInterrupt:
		exit()

if  __name__ == '__main__':
	main()


