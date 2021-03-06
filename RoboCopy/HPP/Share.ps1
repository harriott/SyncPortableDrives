# Joseph Harriott  http://momentary.eu/  Mon 25 Jun 2018

# Backup my Share files.
# PS> D:\Dropbox\JH\IT_stack\onGitHub\SyncPortableDrives\RoboSM3_Share.ps1
# ------------------------------------------------------------------------

# Drives:
# F: SM3
$backupFolder = "F:\ShareRcBu"
$FoldersArray = @(
  # first element of each row allows for that row to be switched off, by setting to 0
  #   gVim  Tabularize/,/l0l0l0  then view in a larger window
  #
  (0,"F:\Share\AV-Stack"                 ,"$backupFolder\AV-Stack")                 ,
  (0,"F:\Share\Dr-CAT-Buddhism"          ,"$backupFolder\Dr-CAT-Buddhism")          ,
  (0,"F:\Share\Dr-CAT-Buddhism-Theravada","$backupFolder\Dr-CAT-Buddhism-Theravada"),
  (0,"F:\Share\Dr-CAT-OutThere"          ,"$backupFolder\Dr-CAT-OutThere")          ,
  (0,"F:\Share\Dr-CAT-OutThere-UK"       ,"$backupFolder\Dr-CAT-OutThere-UK")       ,
  (0,"F:\Share\IT-Copied"                ,"$backupFolder\IT-Copied")                ,
  (0,"F:\Share\IT-DebianBased-Copied"    ,"$backupFolder\IT-DebianBased-Copied")    ,
  (1,"F:\Share\More"                     ,"$backupFolder\More")                     ,
  (0,0                                   ,0) # dummy row                            ,to close
  )

# Dialogue with myself:
. $PSScriptRoot\Colours.ps1
$reply = Read-Host "Do you want to backup (B) F:\Share\ (or simulate (b))? "
[System.Console]::ResetColor()
""

$simulate = ""
if ($reply -ceq "B") {
  "Okay, running backups to $backupFolder`n"
  $reply = "b"
  }
elseif ($reply -ceq "b") {
  "Okay, running simulation for `"mirror to $backupFolder`"`n"
  $simulate = " /l"
  } else { exit }

# Prepare variables for log file:
$ThisScript = $PSCommandPath.TrimStart($PSScriptRoot)
$ChangesLog = "F:\Share\"+$ThisScript.TrimEnd("ps1")+"log"

# Do the work:
$Progress = ""
. $PSScriptRoot\Work.ps1

