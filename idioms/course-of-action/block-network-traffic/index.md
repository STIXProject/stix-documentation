---
layout: idiom
title: COA to Block Network Traffic
---

One potential course of action in response to an attack is to block network traffic associated with that attack. This idiom describes how that course of action can be represented in STIX.

## Scenario

In this scenario, an organization wishes to represent a course of action describing blocking traffic to a known PIVY C2 server located at a specific IP address.

## Data model

<img src="diagram.png" alt="Blocking Network Traffic" class="aside-text" />

The focus of this data model is of course on the STIX [Course of Action](/documentation/coa/CourseOfActionType) component. The course of action is represented as a simple description with structured fields for the cost, efficacy, stage, and type of the course of action. A parameter is also given that indicates, using CybOX, the IP address to block.

The `Title` field simply gives the course of action a human-readable title. Similarly, `Description` and `Short Description` could be used to give it longer human-readable descriptions if desired.

The `Stage` field describes the stage of the response process that the course of action is used at. This is a [controlled vocabulary](/idioms/features/controlled-vocabularies) where the default vocabulary is [COAStageVocab-1.0](/documentation/stixVocabs/COAStageVocab-1.0). For this idiom, the action is a response to some known activity so it's set to "Response".

The `Type` field, also a controlled vocabulary (default is [CourseOfActionTypeVocab-1.0](/documentation/stixVocabs/CourseOfActionTypeVocab-1.0)), indicates what general type of course of action is being described. This COA describes blocking of an IP address by perimeter firewalls, so is set to "Perimeter Blocking".

The `Objective` field describes the intended purpose of the course of action at a technical level. It consists of a text description describing that objective and a [confidence](/idioms/features/confidence) that the COA will achieve that objective. Since the objective is strightforward and the COA has a high degree of success in achieving it, that is set to high.

The `Impact` field describes the expected impact that implementing the course of action will have on normal operations. It uses [StatementType](/documentation/stixCommon/StatementType), which consists of a set of fields allowing the information producer to assert a statement about something. In this case, the `Value` field of the statement is set to "Low" (using the defualt vocabulary for this statement, [HighMediumLowVocab-1.0](/documentation/stixVocabs/HighMediumLowVocab-1.0)) and a description is given as to why the impact is low. Because this COA involves blocking an IP address that is not used for any legitimate purposes the impact to operations will be low.

Similarly, the `Cost` field is a [StatementType](/documentation/stixCommon/StatementType) field that describes the estimated cost of applying the course of action. Applying a firewall rule is cheap, and therefore the field value is set to "Low". No description is given because the statement is simple enough to not require a justification or further explanation. The `Efficacy` is yet another [StatementType](/documentation/stixCommon/StatementType) field describes the effectiveness of the COA assuming it is successful in achieving its objective.

The `Parameter Observables` field is a set of CybOX [Observables](/documentation/cybox/ObservablesType) that describe the technical parameters to the course of action. In combination with the `Type` field, these could be used to automatically convert the course of action into something actionable in a security tool. Alternatively, they can simply be displayed in a structured fashion to the end user. In this case, the CybOX [AddressObject](/documentation/AddressObj/AddressObjectType/) is used to represent the IP address that should be blocked.

## XML

{% highlight xml linenos %}
<coa:CourseOfActionType id="example:coa-55f57cc7-ddd5-467b-1312-6fd602549d9e" xsi:type='coa:CourseOfActionType' version="1.1">
    <coa:Title>Block traffic to PIVY C2 Server (10.10.10.10)</coa:Title>
    <coa:Stage xsi:type="stixVocabs:COAStageVocab-1.0">Response</coa:Stage>
    <coa:Type xsi:type="stixVocabs:CourseOfActionTypeVocab-1.0">Perimeter Blocking</coa:Type>
    <coa:Objective>
        <coa:Description>Block communication between the PIVY agents and the C2 Server</coa:Description>
        <coa:Applicability_Confidence>
            <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
        </coa:Applicability_Confidence>
    </coa:Objective>
    <coa:Parameter_Observables cybox_major_version="2" cybox_minor_version="1" cybox_update_version="0">
        <cybox:Observable id="example:Observable-ef0d428f-7f22-44bd-b210-1e2524d2408e">
            <cybox:Object id="example:Address-ac809826-1c67-45de-addc-e91fe357b328">
                <cybox:Properties xsi:type="AddressObj:AddressObjectType" category="ipv4-addr">
                    <AddressObj:Address_Value>10.0.0.0</AddressObj:Address_Value>
                </cybox:Properties>
            </cybox:Object>
        </cybox:Observable>
    </coa:Parameter_Observables>
    <coa:Impact>
        <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">Low</stixCommon:Value>
        <stixCommon:Description>This IP address is not used for legitmate hosting so there should be no operational impact.</stixCommon:Description>
    </coa:Impact>
    <coa:Cost>
        <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">Low</stixCommon:Value>
    </coa:Cost>
    <coa:Efficacy>
        <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">High</stixCommon:Value>
    </coa:Efficacy>
</coa:CourseOfActionType>

{% endhighlight %}

[Full XML](block-network-traffic.xml)

## Python

{% highlight python linenos %}
from stix.coa import CourseOfAction, Objective
from stix.common import Confidence
from cybox.core import Observables
from cybox.objects.address_object import Address

coa = CourseOfAction()
coa.title = "Block traffic to PIVY C2 Server (10.10.10.10)"
coa.stage = "Response"
coa.type_ = "Perimeter Blocking"

obj = Objective()
obj.description = "Block communication between the PIVY agents and the C2 Server"
obj.applicability_confidence = Confidence("High")

coa.objective = obj
coa.impact = "Low"
coa.impact.description = "This IP address is not used for legitmate hosting so there should be no operational impact."
coa.cost = "Low"
coa.efficacy = "High"

addr = Address(address_value="10.0.0.0", category=Address.CAT_IPV4)
coa.parameter_observables=Observables(addr)

print coa.to_xml()
{% endhighlight %}

[Full Python](block-network-traffic.py)

## Further Reading

See the full documentation for the relevant types for further information that may be provided:

* [CourseOfActionType](/documentation/coa/CourseOfActionType)
* [IndicatorType](/documentation/indicator/IndicatorType) - One common usage of courses of action is through the suggested course of action for an indicator.
