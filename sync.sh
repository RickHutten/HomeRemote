#!/bin/bash

HOME=/mnt/c/Users/Rick
LOCAL_MUSIC_PATH=/mnt/e/Music
REMOTE_MUSIC_PATH=/home/pi/Music
PI_IP=192.168.1.9

REMOTE_LIB_FILE_NAME="music_library.txt~"
TEMP_REMOTE_FILE_NAME="remote_lib.txt~"
TEMP_LOCAL_FILE_NAME="local_lib.txt~"
TEMP_UPLOAD_FILE="upload.sh~"
TEMP_DOWNLOAD_FILE="download.sh~"
TEMP_PYTHON_FILE="sync.py~"

SCRIPT="
    cd $REMOTE_MUSIC_PATH
    find ./ -name '*.mp3' > '../'$REMOTE_LIB_FILE_NAME
    exit
"


cd $LOCAL_MUSIC_PATH
find ./ -name '*.mp3' > $HOME'/'$TEMP_LOCAL_FILE_NAME
cd $HOME



echo -n "Connecting to server..."
ssh pi@$PI_IP "$SCRIPT"
echo DONE

echo -n "Downloading music library..."
scp -q pi@192.168.1.9:$REMOTE_LIB_FILE_NAME ./$TEMP_REMOTE_FILE_NAME
echo DONE

echo -n "Removing remote temporary file..."
ssh pi@$PI_IP "rm $REMOTE_LIB_FILE_NAME"
echo DONE

# Write Python code cause I don't know how to do it in bash :p
echo "print 'Running Python Script...'

remote_file = open('$TEMP_REMOTE_FILE_NAME')
remote_lines = remote_file.readlines()
remote_file.close()

local_file = open('$TEMP_LOCAL_FILE_NAME')
local_lines = local_file.readlines()
local_file.close()

not_local = []
not_remote = []

def main():
    global not_remote
    # Get remote files
    for line in remote_lines:
        if line not in local_lines:
            not_local.append(line.strip())

    print len(not_local), 'files to download from server'
    while len(not_local) > 0:
        ans = raw_input('Do you want to download these files? [y/n] ').lower()
        if ans in ['y', 'n']:
            if ans == 'y':
                download()	
            break
	
    for line in local_lines:
        if line not in remote_lines:
            not_remote.append(line.strip())
	
    print len(not_remote), 'files to upload to server'
    while len(not_remote) > 0:
        ans = raw_input('Do you want to upload these files? [y/n] ').lower()
        if ans in ['y', 'n']:
            if ans == 'y':
                upload()
            break				

def download():
    try:
        f = open('$TEMP_DOWNLOAD_FILE', 'w')
        f.write('echo \'Downloading files...\'\n')
        for line in not_local:
            local_path = '$LOCAL_MUSIC_PATH' + line[1:]
            remote_path = '$REMOTE_MUSIC_PATH' + line[1:]
            f.write('mkdir -p \"' + '/'.join(local_path.split('/')[:-1]) + '\"\n')
	
            f.write('scp pi@$PI_IP:\"\\\\\"' + remote_path + '\\\\\"\" \'' + local_path + '\'\n')
    finally:
        f.close()

def upload():
    try:
        f = open('$TEMP_UPLOAD_FILE', 'w')
        f.write('echo \'Uploading files...\'\n')
        dirs = set()
        for line in not_remote:
            remote_path = '$REMOTE_MUSIC_PATH' + line[1:]
            dirs.add('/'.join(remote_path.split('/')[:-1]))
        for dir in dirs:
            f.write('ssh pi@$PI_IP mkdir -p \"\\\\\"' + dir + '\\\\\"\"\n')
        for line in not_remote:
            local_path = '$LOCAL_MUSIC_PATH' + line[1:]
            remote_path = '$REMOTE_MUSIC_PATH' + line[1:]
            f.write('scp \"' + local_path + '\" pi@$PI_IP:\"\\\\\"' + ('/').join(remote_path.split('/')[:-1]) + '\\\\\"\" \n')  # Finally correct
    finally:
        f.close()

main()

" > $TEMP_PYTHON_FILE

# Create empty output files
touch $TEMP_UPLOAD_FILE $TEMP_DOWNLOAD_FILE
# Run python script
python $TEMP_PYTHON_FILE
# Remove old files
rm $TEMP_PYTHON_FILE $TEMP_REMOTE_FILE_NAME $TEMP_LOCAL_FILE_NAME
# Run output files of python script
./$TEMP_DOWNLOAD_FILE
./$TEMP_UPLOAD_FILE

echo -n "Done! Press ENTER to exit "
read

# Remove output files
rm $TEMP_DOWNLOAD_FILE
rm $TEMP_UPLOAD_FILE
