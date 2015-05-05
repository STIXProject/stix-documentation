---
layout: flat
title: Analyst Exercise
active: getting-started
---

## Setup
Consult this [FireEye report](report) for a prose description of malicious actors from Iran targeting governments and commercial computers.

Download the [free STIXViz tool](/documentation/utilities/) and open the [STIX version of the report](output.xml).

Distribution is unlimited because the **data markings** do not include TLP or other restrictions.

## Report Content - Actor
The **Threat Actor** is identified as Ajax Team, who appear to be based in Iran. Their activities are characterized as **Medium Sophistication** which reflects later analysis indicating their use of customized malware implants and control infrastructure along with an unencrypted communications protocol.

![actor image](pics/actor.png)

Actor attribution was given Medium **Confidence** indicating that the vendor was not able to definitely tie the actor to a given country, but was "believed to be" associated with Iran.

## Report Content - Indicators
Several indicators are included in the report, to capture each resource used by the actor.

Since victims were anonymized, there are no historical **Incident** details, but rather individual **Indicators** used for proactive detection.

![indicator image](pics/indicators.png)


The **Email Indicator** suggests that the sender email address `invite@aeroconf2014.org` should be blocked unconditionally, as the sending domain is owned by the malicious actors.
"IEEE Aerospace Conference 2014" is a suspicious subject line seen in those emails, but may also include legitimate emails.

Under the **File Indicator** a malware sample named 'IntelRS.exe' has been seen with several hashes, which can be directly added to a blacklist.

The malware used an installation **filepath** that was fairly unique, and can be used as a trigger for generic detection as well.

Domains are owned by the malicious actors, and linked to the IP addresses resolved at the time of analysis, which appear to be hosted on an overseas provider. Firewall blocks and DNS filters can be used to prevent access to those without much issue.

## Report Content - TTP
The actor sends phishing emails to unsuspecting victims, a behavior captured under **Observed TTP**, which is given a **Relationship** to each malware sample and control server included in the report.

In order to re-use the **TTP** in other contexts, it acts as a stand-alone object linked to the **Actor**

![ttp image](pics/ttp.png)

## Report itself
`Note: The current version of STIXViz does not display reports.`

All of this information is wrapped up into a `Report` structure to parallel the paper report that FireEye released. It contains information like the report title, description, intent, etc.

## Sharing this data with others
Say you find an instance of the malware in the course of investigations, a **Sighting** of the **Indicator** can be created with a reference to the observed data. An instance of this might [appear similar to this](sighting.xml)

Methods to detect this **Threat Actor** activity can be added under a **Indicator** entry, for instance A YARA signature as a `Rule` attached to a `Test Mechanism`.
