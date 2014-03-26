#!/usr/bin/env python 


import commands
import datetime
import logging
import os
import time

from oasispackage.interfaces import BaseDistribution

class cvmfs21(BaseDistribution):


    def __init__(self, project):

        super(cvmfs21, self).__init__(project)

        #self.log = logging.getLogger("cvmfs")
        self.log.debug('init of cvmfs21 plugin')

        # self.project.dest is like  /cvmfs/myvo.opensciencegrid.org
        # the repo is the <myvo.opensciencegrid.org> part
        self.repo = self.project.destdir.split('/')[2]


    def transfer(self):

        self.log.info('transfering files from %s to %s' %(self.project.srcdir, self.project.destdir))

        ## cmd = 'cvmfs_server transaction %s' %self.repo
        # example:   cvmfs_server transaction atlas.opensciencegrid.org
        cmd = 'sudo -u oasis cvmfs_server transaction %s' %self.repo
        self.log.info('command = %s' %cmd)


        st, out = commands.getstatusoutput(cmd)
        if st:
            self.log.critical('interaction with cvmfs server failed.')
            self.log.critical('RC = %s' %st)
            self.log.critical('output = %s' %out)
            return st

        ## cmd = 'rsync -a -l --delete %s/ %s' %(self.project.srcdir, self.project.destdir)
        # example:   rsync -a -l --delete /home/atlas /cvmfs/atlas.opensciencegrid.org
        cmd = 'sudo -u oasis rsync -a -l --delete %s/ %s' %(self.project.srcdir, self.project.destdir)
        self.log.info('command = %s' %cmd)

        st, out = commands.getstatusoutput(cmd)
        if st:
            self.log.critical('transferring files failed.')
            self.log.critical('RC = %s' %st)
            self.log.critical('output = %s' %out)
            return st

        return st

    def publish(self):
        
        rc = self._publish()
        if rc:
            self.log.critical('publishing failed. Aborting.')
            return rc

        return 0

    def _publish(self):

        self.log.info('publishing CVMFS for repository %s' %self.repo)

        ## cmd = 'cvmfs_server publish %s' %self.repo 
        # example:   cvmfs_server publish atlas.opensciencegrid.org
        cmd = 'sudo -u oasis cvmfs_server publish %s' %self.repo 
        self.log.info('command = %s' %cmd)

        st, out = commands.getstatusoutput(cmd)
        if st:
            self.log.critical('publishing failed.')
            self.log.critical('RC = %s' %st)
            self.log.critical('output = %s' %out)
        return st
    
    def resign(self):
        '''
        Re-sign the .cvmfswhitelist of a  given repository
        '''

        return 0 

        #   masterkey = '/etc/cvmfs/keys/%s.masterkey' %self.repo
        #   # FIXME
        #   # check if masterkey file exists, and raise an exception otherwise 
        #   # for example, if this code is run at a Replica host

        #   whitelist = '/srv/cvmfs/%s/.cvmfswhitelist' %sef.repo

        #   self.log.info('Signing 7-day whitelist for repo %s  with master key...' %self.repo)

        #   now = datetime.datetime.utcnow()
        #   now_str = now.strftime('%Y%m%d%H%M%S')
        #   # this is equivalent to date -u "+%Y%m%d%H%M%S"

        #   nextweek = now + datetime.timedelta(days=7) 
        #   nextweek_str = nextweek.strftime('%Y%m%d%H%M%S')
        #   # this is equivalent to date -u --date='next week' "+%Y%m%d%H%M%S"

        #   # read the whitelist file
        #   # content of whitelist file is like this
        #   #
        #   #   ['20140325141252\n', 
        #   #    'E20140401141252\n', 
        #   #    'Nmis.opensciencegrid.org\n', 
        #   #    '4E:6C:E9:0D:92:83:F0:D5:22:82:02:CD:C5:DA:0C:E3:C1:86:74:FB\n', 
        #   #    '--\n', 
        #   #    '(stdin)= e034cf1b9f11801ffcefdbf64d04c\n', 
        #   #    '\xad\xb0\xc6g\x96....4\xc7\xdb\x\x8b@\xb5\x97Z\xd3?\x0baS\n', 
        #   #    '\x83\xd4|\x98b\xf7~\xe3\xe1E.....4r\xe6=^\xfc\xc2b7\xf1\x06']
        #   #
        #   f = open(whitelist)
        #   lines = f.readlines()
        #   content_repo = lines[2][:-1]
        #   content_fingerprint = lines[3][:-1]


        #   ------  VERSION IN BASH  -----------


        #           echo `date -u "+%Y%m%d%H%M%S"` > ${whitelist}.unsigned
        #           echo "E`date -u --date='next week' "+%Y%m%d%H%M%S"`" >> ${whitelist}.unsigned

        #           # copy the repo name and the fingerprint(s) from original
        #           awk '/^N/ {doprint=1}
        #            /^--/ {exit}
        #            doprint==1 {print}' ${whitelist} >> ${whitelist}.unsigned

        #           sha1=`cat ${whitelist}.unsigned | openssl sha1 | head -c40`
        #           echo "--" >> ${whitelist}.unsigned
        #           echo $sha1 >> ${whitelist}.unsigned
        #           echo -n $sha1 > ${whitelist}.sha1
        #           openssl rsautl -inkey $MASTERKEY -sign -in ${whitelist}.sha1 -out ${whitelist}.signature
        #           cat ${whitelist}.unsigned ${whitelist}.signature > $whitelist
        #           rm -f ${whitelist}.unsigned ${whitelist}.signature ${whitelist}.sha1




