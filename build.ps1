# param (
# 	[switch]$DO_DEBUG=$false,
# 	[switch]$RELATIVE=$false,
# 	[string]$PELICANOPTS="",
# 	[string]$SERVER="0.0.0.0",
# 	[string]$PORT
# )
function Get-IniContent ($filePath)
{
    $ini = @{}
    switch -regex -file $FilePath
    {
        “^\[(.+)\]” # Section
        {
            $section = $matches[1]
            $ini[$section] = @{}
            $CommentCount = 0
        }
        “^(;.*)$” # Comment
        {
            $value = $matches[1]
            $CommentCount = $CommentCount + 1
            $name = “Comment” + $CommentCount
            $ini[$section][$name] = $value
        }
        “(.+?)\s*=(.*)” # Key
        {
            $name,$value = $matches[1..2]
            $ini[$section][$name] = $value
        }
    }
    return $ini
}

$SettingsFilePath="~/.buildbot/settings.ini"
if (Test-Path $SettingsFilePath) {
	$Settings=Get-IniContent $SettingsFilePath
	foreach ($item in $Settings["SCHNEEBRENNER"]) { 
		Write-Output $item }
}
$DEBUG=$false
$RELATIVE=$false
$PELICANOPTS=""
$SERVER="0.0.0.0"
$PORT=""

foreach ($argument in $args) {
	if ($argument -eq "DEBUG=1") {$DEBUG=$true}
	if ($argument -eq "RELATIVE=1") {$RELATIVE=$true}
	if ($argument -contains "PORT=") {$PORT=$argument.split('=')[1]}
	if ($argument -contains "SERVER=") {$SERVER=$argument.split('=')[1]}
}

$BASEDIR=$PSScriptRoot
$INPUTDIR="${BASEDIR}/content"
$OUTPUTDIR="${BASEDIR}/output"
$CONFFILE="${BASEDIR}/pelicanconf.py"
$PUBLISHCONF="${BASEDIR}/publishconf.py"

$SSH_HOST=$Settings["SCHNEEBRENNER"]["server"]
$SSH_PORT=$Settings["SCHNEEBRENNER"]["port"]
$SSH_USER=$Settings["SCHNEEBRENNER"]["user"]
$SSH_TARGET_DIR=$Settings["SCHNEEBRENNER"]["target_dir"]


if ($DEBUG) {
	$PELICANOPTS += " -D"
}

if ($RELATIVE) {
	$PELICANOPTS +=" --relative-urls"
}


if ($PORT -ne "") {
	$PELICANOPTS +=" -p ${PORT}"
}


function Get-Help {
	Write-Output 'Makefile for a pelican Web site                                           '
	Write-Output '                                                                          '
	Write-Output 'Usage:                                                                    '
	Write-Output '   build html                           (re)generate the web site          '
	Write-Output '   build clean                          remove the generated files         '
	Write-Output '   build regenerate                     regenerate files upon modification '
	Write-Output '   build publish                        generate using production settings '
	Write-Output '   build serve [PORT=8000]              serve site at http://localhost:8000'
	Write-Output '   build serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	Write-Output '   build devserver [PORT=8000]          serve and regenerate together      '
	Write-Output '   build devserver-global               regenerate and serve on 0.0.0.0    '
	Write-Output '   build ssh_upload                     upload the web site via SSH        '
	Write-Output '   build sftp_upload                    upload the web site via SFTP       '
	Write-Output '   build rsync_upload                   upload the web site via rsync+ssh  '
	Write-Output '                                                                          '
	Write-Output 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	Write-Output 'Set the RELATIVE variable to 1 to enable relative urls                    '
	Write-Output '                                                                          '
}

function Get-Html {
 	pelican "${INPUTDIR}" -o "${OUTPUTDIR}" -s "${CONFFILE}" ${PELICANOPTS}
}

# clean:
# 	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

# regenerate:
# 	"$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

function Get-Serve {
	pelican -l "${INPUTDIR}" -o "${OUTPUTDIR}" -s "${CONFFILE}" ${PELICANOPTS}
}

# serve-global:
# 	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)

# devserver:
# 	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

# devserver-global:
# 	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b 0.0.0.0

# publish:
# 	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)

# ssh_upload: publish
# 	scp -P $(SSH_PORT) -r "$(OUTPUTDIR)"/* "$(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)"
function ssh-upload {
 	scp -P $SSH_PORT -r "${OUTPUTDIR}"/* "${SSH_USER}@${SSH_HOST}:${SSH_TARGET_DIR}"
}

# sftp_upload: publish
# 	printf 'put -r $(OUTPUTDIR)/*' | sftp $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

# rsync_upload: publish
# 	rsync -e "ssh -p $(SSH_PORT)" -P -rvzc --include tags --cvs-exclude --delete "$(OUTPUTDIR)"/ "$(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)"

foreach ($argument in $args) {
	if ($argument -eq "help") { Get-Help }
	if ($argument -eq "html") { Get-Html }
	if ($argument -eq "serve") { Get-Serve }
}