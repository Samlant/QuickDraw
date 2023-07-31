; Bundling Script

#define MyDistributionFiles "E:My Stuff\My Project Center\Work\QuickDraw\pkging\dist"
#define MyBuildDir "E:My Stuff\My Project Center\Work\QuickDraw\pkging\build"
#define MyAppName "QuickDraw"
#define MyAppVersion "v3.0.0.alpha"
; #define MyAppVersion GetEnv('APPVERSIONTEXT')
#define MyAppVersionFileName "v3_0_0_alpha"
; #define MyAppVersionFileName GetEnv('APPVERSIONFILE')
#define MyAppURL "https://github.com/Samlant/QuickDraw"
#define MyAppExeName "QuickDraw.exe"
#define MyAppIcoName "icon.ico"
#define MyInstallIcoName "install.ico"
#define MyConfigurationsFileName "configurations.ini"
#define MyAPIKeyName "ms_graph_state.jsonc"


[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName}-{#MyAppVersionFileName}
AppPublisherURL={#MyAppURL}
DefaultDirName={localappdata}\Work-Tools
DefaultGroupName=Work-Tools
OutputDir={#MyBuildDir}
OutputBaseFilename={#MyAppName}-{#MyAppVersionFileName}-Setup
DisableReadyPage=yes
SetupIconFile={#MyDistributionFiles}\{#MyInstallIcoName}
LicenseFile={#MyDistributionFiles}\LICENSE.txt
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableStartupPrompt=yes
PrivilegesRequired=lowest

[Files]
Source: "{#MyDistributionFiles}\{#MyAppExeName}"; DestDir: "{app}"
Source: "{#MyDistributionFiles}\{#MyAppIcoName}"; DestDir: "{app}"
Source: "{#MyDistributionFiles}\README.html"; Flags: isreadme; DestDir: "{app}"
Source: "{#MyDistributionFiles}\README.md"; DestDir: "{app}"
Source: "{#MyDistributionFiles}\{#MyConfigurationsFileName}"; DestDir: "{app}"
Source: "{#MyDistributionFiles}\LICENSE.txt"; DestDir: "{app}"
Source: "{#MyDistributionFiles}\{#MyAPIKeyName}"; DestDir: "{app}"


[Tasks]
Name: autoRunFile; Description: "Auto-run on Windows Start-up";
Name: startmenu; Description: "Create a Start Menu folder";
Name: desktopicon; Description: "Create a &desktop icon";

[Icons]
Name: "{group}\Work-Tools\{#MyAppExeName}"; Filename: "{app}\QuickDraw.exe"; IconFilename: "{#MyAppIcoName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcoName}"; Tasks: desktopicon
Name: "{group}\Work-Tools\{cm:ProgramOnTheWeb, {#MyAppName}}"; Filename: "{#MyAppURL}"; Tasks: startmenu
Name: "{group}\Work-Tools\{cm:UninstallProgram, {#MyAppName}}"; Filename: "{uninstallexe}"; Tasks: startmenu
Name: "{group}\Work-Tools\{cm:UninstallProgram, {#MyAppName}}"; Filename: "{uninstallexe}"; Tasks: startmenu
Name: "{userstartup}\QuickDraw"; Filename: "{app}\{#MyAppExeName}"; Tasks: autoRunFile

[Dirs]


[INI]
; place entries here to depict different languages available for the installer

[Run]
; rune programs post-installer

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]



