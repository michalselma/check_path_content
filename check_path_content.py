import os
import time

os.system('cls') # Clear screen

print('### START ###')

startpath = 'C:\\'

# Counters
dircnt = 0
emptydircnt = 0
filecnt = 0
emptyfilecnt = 0
symlinkcnt = 0
errcnt = 0
activity = 0

sec_since_epoch = time.time() # Get julan date time in seconds

wrkdir = os.getcwd() # Get current work directory

# Logs
logfile = os.path.join(wrkdir, str(sec_since_epoch)+'.log') # Save log file in current work directory
print('[INFO] Creating log file:')
print(logfile)
log = open(logfile, "wt", encoding="utf-8")

# Lists
lstdirsfile = os.path.join(wrkdir, 'dirs.lst')
lstfilesfile = os.path.join(wrkdir, 'files.lst')
lstsymlinksfile = os.path.join(wrkdir, 'symlinks.lst')
lstemptydirsfile = os.path.join(wrkdir, 'emptydirs.lst')
lstemptyfilesfile = os.path.join(wrkdir, 'emptyfiles.lst')
lsterrorsfile = os.path.join(wrkdir, 'errors.lst')
print('[INFO] Creating output lists:')
print(lstdirsfile)
print(lstfilesfile)
print(lstsymlinksfile)
print(lstemptydirsfile)
print(lstemptyfilesfile)
print(lsterrorsfile)
lstdirs = open(lstdirsfile, "wt", encoding="utf-8")
lstfiles = open(lstfilesfile, "wt", encoding="utf-8")
lstsymlinks = open(lstsymlinksfile, "wt", encoding="utf-8")
lstemptydirs = open(lstemptydirsfile, "wt", encoding="utf-8")
lstemptyfiles = open(lstemptyfilesfile, "wt", encoding="utf-8")
lsterrors = open(lsterrorsfile, "wt", encoding="utf-8")

print('[INFO] Procesing files and directories under:')
print(startpath)

for root, dirs, files in os.walk(startpath):
    activity = activity + 1
    print(activity, end = '\r')
    log.write('[DEBUG] Processing root directory: '+root+'\n')
    # NOTE: During os.walk() symlinks are skipped and not processed on next iteration of current root
    # eg. if root contain 3 dirs where 2 are dirs and 1 is symlink only 2 "real" dirs will be walked further
    #print(dirs)
    #print(files)
    if dirs == [] and files == []:
        log.write('[WARN] Current directory is empty (no files and subdirs).\n')
        emptydircnt = emptydircnt + 1
        lstemptydirs.write(root+'\n')

    for dir in dirs:
        log.write('[TRACE] Subdirectory found: '+dir+'\n')
        dirpath = os.path.join(root, dir)
        log.write('[TRACE] Full path: '+dirpath+'\n')
        log.write('[TRACE] Dir path type isdir(): '+str(os.path.isdir(dirpath))+'\n')
        log.write('[TRACE] Dir path type islink(): '+str(os.path.islink(dirpath))+'\n')
        log.write('[TRACE] Dir path type isfile(): '+str(os.path.isfile(dirpath))+'\n')
        
        # isdir() itself can indicate directory or a symbolic link (symlink) pointing to a directory,
        # so additional islink() check is required to the isdir() check to identify dir or symlink
        
        if os.path.isdir(dirpath) == True and os.path.islink(dirpath) == False:
            dirtype = 'dir'
            dircnt = dircnt+1
            lstdirs.write(dirpath+'\n')
        elif os.path.isdir(dirpath) == True and os.path.islink(dirpath) == True:
            dirtype = 'symlink'
            symlinkcnt = symlinkcnt+1
            lstsymlinks.write(dirpath+'\n')
        elif os.path.isdir(dirpath) == False and os.path.islink(dirpath) == True:
            dirtype = 'error'
            log.write('[ERROR] Directory path can not be islink()==True without isdir()==True.\n')
            log.write('[ERROR] Incorrect os.walk() dir identification. Might be broken directiory Symbolic link, when symlink destination folder has been removed.\n')
            # NOTE: isdir()==False and islink()==True should never reach this point. For broken symlinks os.walk() will list and 
            # process it as file object, even isfile() for that object will be False - tbc how os.walk() distinguish dirs vs files.
            errcnt = errcnt+1
            lsterrors.write(dirpath+'\n')
        else:
            # This else covers isdir()==False and islink()==False
            dirtype = 'error'
            log.write('[ERROR] Directory path should not be isdir()==False.\n')
            log.write('[ERROR] Incorrect os.walk() dir identification. Might be broken directiory junction link, when junction link destination folder has been removed.\n')
            errcnt = errcnt+1
            lsterrors.write(dirpath+'\n')

        # isfile() should always be False for path identified by os.walk() as dir
        if os.path.isfile(dirpath) == True:
            dirtype = 'error'
            log.write('[ERROR] Directory path can not be isfile()==True. Incorrect os.walk() dir identification.\n')
            errcnt = errcnt+1
            lsterrors.write(dirpath+'\n')

        log.write('[TRACE] Dir type: '+dirtype+'\n')

    for file in files:
        log.write('[TRACE] File found: '+file+'\n')
        filepath = os.path.join(root, file)
        log.write('[TRACE] Full path: '+filepath+'\n')
        log.write('[TRACE] File path type isdir(): '+str(os.path.isdir(filepath))+'\n')
        log.write('[TRACE] File path type islink(): '+str(os.path.islink(filepath))+'\n')
        log.write('[TRACE] File path type isfile(): '+str(os.path.isfile(filepath))+'\n')

        if os.path.isfile(filepath) == True:
            filesize = os.path.getsize(filepath)
            log.write('[TRACE] File Size: '+str(filesize)+' bytes\n')
            if filesize == 0:
                log.write('[WARN] File is empty.\n') 
                emptyfilecnt = emptyfilecnt + 1
                lstemptyfiles.write(filepath+'\n')
            filecnt = filecnt + 1
            lstfiles.write(filepath+'\n')
        else:
            log.write('[ERROR] Identified isfile()==False for file. Incorrect os.walk() file identification. Might occur when dest dir of symlink has been removed.\n')
            errcnt = errcnt+1
            lsterrors.write(filepath+'\n')

print('[INFO] Directories found: '+str(dircnt))
log.write('[INFO] Directories found: '+str(dircnt)+'\n')

print('[INFO] Empty dirs found: '+str(emptydircnt))
log.write('[INFO] Empty dirs found: '+str(emptydircnt)+'\n')

print('[INFO] Files found: '+str(filecnt))
log.write('[INFO] Files found: '+str(filecnt)+'\n')

print('[INFO] Empty files found: '+str(emptyfilecnt))
log.write('[INFO] Empty files found: '+str(emptyfilecnt)+'\n')

print('[INFO] Directory Symbolic Links found: '+str(symlinkcnt))
log.write('[INFO] Directory Symbolic Links found: '+str(symlinkcnt)+'\n')

print('[INFO] Errors occured: '+str(errcnt))
log.write('[INFO] Errors occured: '+str(errcnt)+'\n')

log.close()
lstdirs.close()
lstfiles.close()
lstsymlinks.close()
lstemptydirs.close()
lstemptyfiles.close()
lsterrors.close()

print('### END ###')
