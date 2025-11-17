[Setup]
AppName=Music Player
AppVersion=1.0
DefaultDirName={pf}\Music Player
DefaultGroupName=Music Player
OutputBaseFilename=MusicPlayerInstaller
OutputDir=installer
DisableProgramGroupPage=no

[Files]
Source: "dist\Music Player\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Music Player"; Filename: "{app}\Music Player.exe"
Name: "{commondesktop}\Music Player"; Filename: "{app}\Music Player.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:";