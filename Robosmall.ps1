# vim: set et tw=0:

# Backups only more vital data folders from  HPP  to  a smaller drive
# -------------------------------------------------------------------
# E: SDSSDA240G
# G: the smaller storage

# Prepare a file to log all of the changes made:
$ThisScript = $PSCommandPath.TrimStart($PSScriptRoot)
$ChangesLog = "G:\"+$ThisScript.TrimEnd("ps1")+"log"
"vim: nowrap tw=0:" > $ChangesLog
"" >> $ChangesLog

$FoldersArray = @(
  "Copied",
  "F+F",
  "IT_stack",
  "Now",
  "Theatre0",
  "Theatre1",
  "Then0",
  "Then1",
  "toReduce",
  "Work",
  0) # dummy item

# Do the work:
foreach ($FC in $FoldersArray) {
  if ( $FC ) {
    $Glog="G:\k-$FC"+"_fromHPP.log"
    "vim: nowrap tw=0:" > $Glog
    "" >> $Glog
    $Command = "robocopy /mir E:\Dropbox\JH\$FC G:\$FC /np /unilog+:$Glog /tee /fft"
    iex $Command # Comment this line to disable the file copying
    $Command >> $ChangesLog
    gc $Glog | select-string '    New File|    Newer|    Older|`*EXTRA File|  New Dir|`*EXTRA Dir' >> $ChangesLog
    "" >> $ChangesLog
  }
}
