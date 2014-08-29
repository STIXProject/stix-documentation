#!/usr/bin/env python
# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import sys
from stix.core import STIXPackage, STIXHeader

def parse_stix( pkg ):
    print "== INCIDENT Assets Impacted =="
    for inc in pkg.incidents:
        print "---"
        print "Title: "+ inc.title
        for asset in inc.affected_assets:
            print "---"
            print "Description: "+ str(asset.description)
            print "Type: "+ str(asset.type_)
            print "How many: "+ str(asset.type_.count_affected)
            print "Role: " + str(asset.business_function_or_role )
            print "Owner: " +str(asset.owernship_class ) # typo since py-stix master has bug as of 8-29
            print "Manager: " +str(asset.management_class )
            print "Location: " +str(asset.location_class )

            for effect in asset.nature_of_security_effect:
                    print "---"
                print "Lost:" + str(effect.property_ )
                print "Effect:" + str(effect.description_of_effect )
                print "Was private data stolen?: " + str(effect.non_public_data_compromised )
                print "Was it encrypted?: " + str(effect.non_public_data_compromised.data_encrypted )

    return 0

if __name__ == '__main__':
    try: fname = sys.argv[1]
    except: exit(1)
    fd = open(fname)
    stix_pkg = STIXPackage.from_xml(fd)

    parse_stix(stix_pkg)
