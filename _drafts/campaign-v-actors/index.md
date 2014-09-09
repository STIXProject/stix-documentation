---
layout: flat
title: Defining Campaigns vs Threat Actors
constructs:
  - Campaign
  - Threat Actor
  - TTP
summary:  Discussion and examples on when to use the term "Campaign" vs "Actor".
---

In STIX terminology, an individual or group in the market for intrusion services and data theft is called a `Threat Actor`.  Their activity towards that end - information theft and system compromise is called a `Campaign`. Such behavior might fit along the lines of stealing financial information from banking customers or [targeting a particular business sector](../industry-sector). 

When data is collected on intrusion attempts, it may not include attribution on the actor causing them. In this case, the preferred method is to define that activity as a `Campaign` with a placeholder `Threat Actor` identity until additional information comes to light. 

As an example, if domains used in an intrusion are owned and registered by a single persona, they would be given `Low Confidence` in relation to the incident.  If the persona is known to be used by a professional intrusion team, it could be related to that larger group.  Occasionally it is possible to fingerprint an actor by the customizations made in their tools (such as language choice or debug information), which would further increase `Confidence` in the actor being involved.

When an actor is known but cannot be linked to existing intrusions, they can be created as a `Threat Actor` with their `Identity` information filled out with their handles, location, known tools and network infrastructure. If those markers are observed in a new incident or correlated with historical data, the `Actor` can be related according to its confidence rating.

It is tempting to name a given `Campaign` after the malware or apparent group involved, however these methods are not very precise and prone to conflicts in naming between information sources. Imagine a situation where one organization declares that the "Netcat" malware had targeted their network, or the "Poison Ivy" actors were involved in a given intrusion.

Overall, a Campaign is some time-bounded activity that uses intrusion methods against a set of targets, while a Threat Actor is the entity performing such behavior.

## Data model

We use the [CampaignType](/data-model/{{site.current_version}}/campaign/CampaignType) to render the campaign and [ThreatActorType](/data-model/{{site.current_version}}/campaign/ThreatActorType) for the actor.

In this case, a `Campaign` has an identified `ThreatActor` and constrained victim targeting. Since the actor was likely involved in other incidents, it may be related to other campaigns as well.

## XML
{% highlight xml linenos %}
<stix:STIX_Package 
	xmlns:example="http://example.com"
	xmlns:campaign="http://stix.mitre.org/Campaign-1"
	xmlns:ttp="http://stix.mitre.org/TTP-1"
	xmlns:ta="http://stix.mitre.org/ThreatActor-1"
	xmlns:stixCommon="http://stix.mitre.org/common-1"
	xmlns:stixVocabs="http://stix.mitre.org/default_vocabularies-1"
	xmlns:stix="http://stix.mitre.org/stix-1"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="
	http://stix.mitre.org/Campaign-1 http://stix.mitre.org/XMLSchema/campaign/1.1.1/campaign.xsd
	http://stix.mitre.org/TTP-1 http://stix.mitre.org/XMLSchema/ttp/1.1.1/ttp.xsd
	http://stix.mitre.org/ThreatActor-1 http://stix.mitre.org/XMLSchema/threat_actor/1.1.1/threat_actor.xsd
	http://stix.mitre.org/common-1 http://stix.mitre.org/XMLSchema/common/1.1.1/stix_common.xsd
	http://stix.mitre.org/default_vocabularies-1 http://stix.mitre.org/XMLSchema/default_vocabularies/1.1.1/stix_default_vocabularies.xsd
	http://stix.mitre.org/stix-1 http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd" id="example:Package-81810123-b298-40f6-a4e7-186efcd07670" version="1.1.1" timestamp="2014-08-08T15:50:10.983851+00:00">
    <stix:Campaigns>
        <stix:Campaign id="example:Campaign-e5268b6e-4931-42f1-b379-87f48eb41b1e" timestamp="2014-08-08T15:50:10.983728+00:00" xsi:type='campaign:CampaignType' version="1.1.1">
            <campaign:Title>Compromise of ATM Machines</campaign:Title>
            <campaign:Related_TTPs>
                <campaign:Related_TTP>
                    <stixCommon:TTP id="example:ttp-2d1c6ab3-5e4e-48ac-a32b-f0c01c2836a8" timestamp="2014-08-08T15:50:10.983464+00:00" xsi:type='ttp:TTPType' version="1.1.1">
                        <ttp:Title>Victim Targeting: Customer PII and Financial Data</ttp:Title>
                        <ttp:Victim_Targeting>
                            <ttp:Targeted_Information xsi:type="stixVocabs:InformationTypeVocab-1.0">Information Assets - Financial Data</ttp:Targeted_Information>
                        </ttp:Victim_Targeting>
                    </stixCommon:TTP>
                </campaign:Related_TTP>
            </campaign:Related_TTPs>
            <campaign:Attribution>
                <stixCommon:Threat_Actor id="example:threatactor-56f3f0db-b5d5-431c-ae56-c18f02caf500" timestamp="2014-08-08T15:50:10.983629+00:00" xsi:type='ta:ThreatActorType' version="1.1.1">
                    <ta:Title>People behind the intrusion</ta:Title>
                </stixCommon:Threat_Actor>
            </campaign:Attribution>
        </stix:Campaign>
    </stix:Campaigns>
</stix:STIX_Package>
{% endhighlight %}


[Full XML](campaign-v-actors.xml)

## Python

{% highlight python linenos %}
#!/usr/bin/env python
# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

'''
The following code requires python-stix v1.1.0.4 or greater installed.
For installation instructions, please refer to https://github.com/STIXProject/python-stix.
'''

def main():
    from stix.campaign import Campaign, Attribution
    from stix.threat_actor import ThreatActor
    from stix.core import STIXPackage
    from stix.ttp import TTP, VictimTargeting

    ttp = TTP()
    ttp.title = "Victim Targeting: Customer PII and Financial Data"
    ttp.victim_targeting = VictimTargeting()
    ttp.victim_targeting.add_targeted_information("Information Assets - Financial Data")

    actor = ThreatActor()
    actor.title = "People behind the intrusion"

    c = Campaign()
    c.attribution.append(actor)
    c.title = "Compromise of ATM Machines"
    c.related_ttps.append(ttp)

    pkg = STIXPackage()
    pkg.add_campaign(c)

    print pkg.to_xml()

if __name__ == '__main__':
    main()
{% endhighlight %}

[Full Python](campaign-v-actors.py)

## Further Reading

See the full documentation for the relevant types for further information that may be provided:

* [CampaignType](/data-model/{{site.current_version}}/campaign/CampaignType)
* [TTPType](/data-model/{{site.current_version}}/ttp/TTPType)
* [VictimTargetingType](/data-model/{{site.current_version}}/ttp/VictimTargetingType)
