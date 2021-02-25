import os
import json
import subprocess

from cmd import Cmd
 
class EMSPRompt(Cmd):
    prompt = 'ems> '
    intro = "Welcome to ExoMy shell! Type ? to list commands"
 
    def do_configure_image(self, s):
        '''configure the image.'''
        country = input('Country: ')
        sid = input('Wifi Sid: ')
        password = input('Wifi Password: ')

        with open('./pi_config_template.json', 'r') as file:
            template=file.read()
            file.close()
            template = template.replace('{{user `wifi_name`}}', sid)
            template = template.replace('{{user `wifi_password`}}', password)

            with open('./ExoMyPi.json', 'w') as file:
                file.write(template)
                file.close()

                print('Configure image')
                p = subprocess.Popen('docker run --rm --privileged -v ${PWD}:/build:ro -v ${PWD}/packer_cache:/build/packer_cache -v ${PWD}/output-arm-image:/build/output-arm-image -v ~/.ssh/id_rsa.pub:/root/.ssh/id_rsa.pub:ro quay.io/solo-io/packer-builder-arm-image:v0.1.5 build ExoMyPi.json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in p.stdout.readlines():
                    print(line.decode()),
                retval = p.wait()
                print('Image created')

    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True

EMSPRompt().cmdloop()