[Setup]
AppName=Music Player
AppVersion=1.0
DefaultDirName={pf}\Music Player
DefaultGroupName=Music Player
OutputBaseFilename=MusicPlayerInstaller
OutputDir=installer
DisableProgramGroupPage=no

[Files]
Source: "installer\Music Player\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Files]
Source: "documentation\images\donate.bmp"; Flags: dontcopy

[Icons]
Name: "{group}\Music Player"; Filename: "{app}\Music Player.exe"
Name: "{commondesktop}\Music Player"; Filename: "{app}\Music Player.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:";

[Code]
var
  DonatePage: TWizardPage;
  DonateImage: TBitmapImage;
  DonateLabel: TNewStaticText;

procedure InitializeWizard;
begin
  { Create the Donate page }
  DonatePage := CreateCustomPage(wpSelectTasks, 'Support the Developer', 'Optional Donation');

  { Add image }
  DonateImage := TBitmapImage.Create(DonatePage);
  DonateImage.Parent := DonatePage.Surface;
  DonateImage.Left := ScaleX(10);
  DonateImage.Top := ScaleY(10);
  DonateImage.Width := ScaleX(188);
  DonateImage.Height := ScaleY(106);
  DonateImage.Stretch := True;

  DonateImage.Bitmap.LoadFromFile(ExpandConstant('{src}\images\donate.bmp'));

  DonateLabel := TNewStaticText.Create(DonatePage);
  DonateLabel.Parent := DonatePage.Surface;

  DonateLabel.Left := ScaleX(10);
  DonateLabel.Top := ScaleY(122);
  DonateLabel.Width := ScaleX(300);
  DonateLabel.Height := ScaleY(200);
  DonateLabel.WordWrap := True;
  DonateLabel.Caption :=
    'If you would like to support future development,' #13#10 +
    'you can donate using this card number:' #13#10#13#10 +
    'Card: 4111 1111 1111 1111';

end;