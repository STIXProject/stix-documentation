---
layout: getting_started
---

# Impetus
A common use case for STIX is to convert an existing report into XML format that can be shared and ingested automatically.

For the purpose of this example, we will be using a [FireEye report](report) on malicious actors in Iran. 

Python bindings for STIX will be used to generate the resulting XML, which may look [something like this.](output.xml)

## Capture metadata about report
Keeping track of the author, date of publication, and the intent of the report is valuable when evaluating the actionability of information.

``` python
stix_header.description = "Indicators for FireEye report on Saffron"
stix_header.add_package_intent ("Threat Report")
stix_header.information_source = InformationSource()
stix_header.information_source.time = Time()
stix_header.information_source.time.produced_time = datetime.strptime('2014-05-15', "%Y-%m-%d")
```

If the report includes limited distribution markings, those restrictions would be included here.


## Create Indicator for email message 

Several types of indicators are clearly visible -  malicious emails sent by the actors as a prime example.

First, instantiate an `Indicator` for the malicious email.
``` python
email_ind = Indicator()
email_ind.title = "Phishing email"
email_ind.description = "Malicious emails sent from actors"
```

Then, create an `EmailMessage` observable and link it to the `Indicator`.

``` python
# build observable
eml = EmailMessage()
eml.sender = "invite@aeroconf2014.org"
eml.subject = "IEEE Aerospace Conference 2014"

# link to indicator
email_ind.add_object(eml)
```

## Break out Indicator for malware

Similarly, malware samples can be captured along with their hashes.

``` python
malware_ind = Indicator()
malware_ind.title = "Malware used by actors"
malware_ind.description = "Remote access trojan Stealer"
```

In this case, the observable type is `File`, which includes the original file path and name.

``` python
sample = File()
sample.add_hash ( Hash('6dc7cc33a3cdcfee6c4edb6c085b869d'))
sample.file_extension = '.exe'
sample.file_name = 'IntelRS.exe' 
sample.file_path = 'C:\Documents and Settings{USER}\Application Data\IntelRapidStart\AppTransferWiz.dll'

# link to indicator
malware_ind.add_object(sample)
```

## Generate Indicator for control server

All together now, we can create an `Indicator` for the use of a remtoe server to control the malware, and link it to `DomainName` and `Address` observables.

``` python
control_ind = Indicator()
control_ind.title = "Malware control server"
control_ind.description = "Malicious domains ond IP wned by actors"

# add domain object
domain = DomainName()
domain.value = 'yahoomail.com.co'
control_ind.add_object(domain)

ip = Address()
ip.category = ip.CAT_IPV4
ip.address_value = '81.17.28.227'
control_ind.add_object(ip)
```

# Enriching the report

Add context by creating a relationship between the malware sample and its control server IP.

``` python
sample.add_related(ip,"Related_To")
```

Each indicator can also include where it came from and when it was first seen.

``` python
indicator.set_producer_identity("FireEye")
indicator.set_produced_time(datetime.strptime('2014-05-15', "%Y-%m-%d"))
```

## Adding a TTP
Stepping back from the indicator, the next step is to represent the TTP that the indicator indicates. In STIX, TTPs are used to represent three primary concepts:

* Resources (infrastructure and tools)
* Behavior (attack patterns, malware, exploits)
* Victim Targeting

``` python
malware = TTP()
malware.title = 'Malware Implant'
malware.description = 'Customized trojan written in .NET'
malware.intended_effects = 'Account Takeover'

control_ind.add_indicated_ttp(TTP(idref=malware.id_))

```

## Define threat actor

To capture the overall intrusion team behind this campaign, we create a `ThreatActor` object.

This enables defenders to share estimates of the actor's intent, motivation, and sophistication.


``` python
actor = ThreatActor()
actor.title = "Ajax Team"
actor.description = "Iranian intrusion team"
actor.add_motivation ("Political")
actor.add_motivation ("Military")
actor.add_sophistication ("Practitioner")
actor.add_intended_effect ("Advantage - Political")
```


We can also link the previously observed TTP of using a particular malware sample to the actor

``` python
actor.observed_ttps = ObservedTTPs(TTP(idref=malware.id_))
```
