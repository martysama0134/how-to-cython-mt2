from sys import path as sys_path
from os.path import splitext as op_splitext

libpath = r'..\Py2Lib\lib'
sys_path.append(libpath)
rootpath = r'.'

capNameList = {
	"colorinfo":"colorInfo",
	"consolemodule":"consoleModule",
	"constinfo":"constInfo",
	"debuginfo":"debugInfo",
	"dragon_soul_refine_settings":"dragon_soul_refine_settings",
	"emotion":"emotion",
	"exception":"exception",
	"game":"game",
	"interfacemodule":"interfaceModule",
	"introcreate":"introCreate",
	"introempire":"introEmpire",
	"introloading":"introLoading",
	"intrologin":"introLogin",
	"intrologo":"introLogo",
	"introselect":"introSelect",
	"localeinfo":"localeInfo",
	"mousemodule":"mouseModule",
	"musicinfo":"musicInfo",
	"networkmodule":"networkModule",
	"playersettingmodule":"playerSettingModule",
	"prototype":"Prototype",
	"rootlibcythonizer":"RootLibCythonizer",
	"servercommandparser":"serverCommandParser",
	"serverinfo":"serverInfo",
	"stringcommander":"stringCommander",
	"system":"system",
	"test_affect":"test_affect",
	"ui":"ui",
	"uiaffectshower":"uiAffectShower",
	"uiattachmetin":"uiAttachMetin",
	"uiauction":"uiAuction",
	"uiautoban":"uiAutoban",
	"uicandidate":"uiCandidate",
	"uicharacter":"uiCharacter",
	"uichat":"uiChat",
	"uicommon":"uiCommon",
	"uicube":"uiCube",
	"uidragonsoul":"uiDragonSoul",
	"uiequipmentdialog":"uiEquipmentDialog",
	"uiex":"uiEx",
	"uiexchange":"uiExchange",
	"uigamebutton":"uiGameButton",
	"uigameoption":"uiGameOption",
	"uiguild":"uiGuild",
	"uihelp":"uiHelp",
	"uiinventory":"uiInventory",
	"uimapnameshower":"uiMapNameShower",
	"uimessenger":"uiMessenger",
	"uiminimap":"uiMiniMap",
	"uioption":"uiOption",
	"uiparty":"uiParty",
	"uiphasecurtain":"uiPhaseCurtain",
	"uipickmoney":"uiPickMoney",
	"uiplayergauge":"uiPlayerGauge",
	"uipointreset":"uiPointReset",
	"uiprivateshopbuilder":"uiPrivateShopBuilder",
	"uiquest":"uiQuest",
	"uirefine":"uiRefine",
	"uirestart":"uiRestart",
	"uisafebox":"uiSafebox",
	"uiscriptlocale":"uiScriptLocale",
	"uiselectitem":"uiselectitem", #
	"uiselectmusic":"uiSelectMusic",
	"uishop":"uiShop",
	"uisystem":"uiSystem",
	"uisystemoption":"uiSystemOption",
	"uitarget":"uiTarget",
	"uitaskbar":"uiTaskBar",
	"uitip":"uiTip",
	"uitooltip":"uiToolTip",
	"uiuploadmark":"uiUploadMark",
	"uiweb":"uiWeb",
	"uiwhisper":"uiWhisper",
	"utils":"utils",
}

def checkCapName(x):
	base, ext = op_splitext(x)
	try:
		return capNameList[base.lower()] + ext
	except KeyError:
		return x

#import utils
import imp
fp, pathname, description = imp.find_module('utils', [libpath])
utils = imp.load_module('utils', fp, pathname, description)

pys = utils.findMatchedFiles(rootpath, "*.py")
if __file__ in pys:
	pys.remove(__file__)
pys = [checkCapName(x) for x in pys]

import cythonizer
moduleLst = cythonizer.run(pys, forceRecompile=True)
moduleNameLst = []
sourceFileLst = []

for m in moduleLst:
	for source in m.sources:
		base, ext = op_splitext(source)
		moduleName = base.split('/')[-1]
		moduleNameLst.append(moduleName)
		sourceFileLst.append(base + (".cpp" if "c++" == m.language else ".c"))

import sourceWriter
sourceFileName = sourceWriter.run(moduleNameLst, 'rootlib')
print "%s successfully created." % sourceFileName

