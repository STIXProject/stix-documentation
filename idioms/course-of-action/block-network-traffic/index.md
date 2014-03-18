---
layout: idiom
title: Blocking Network Traffic
---

One potential course of action in response to an attack is to block network traffic associated with that attack. This idiom describes how that course of action can be represented in STIX.

## Data model

The focus of this data model is of course on the STIX [Course of Action](/documentation/coa/CourseOfActionType) component. The course of action is represented as a simple description with structured fields for the cost, efficacy, stage, and type of the course of action. A parameter is also given that indicates, using CybOX, the IP address to block.

<img src="diagram.png" alt="Blocking Network Traffic" class="aside-text" />

The `Title` field simply gives the course of action a human-readable title. Similarly, `Description` and `Short_Description` could be used to give it longer human-readable descriptions.

The `Stage` field describes the stage of the response process that the course of action is used at. This is a [controlled vocabulary](/idioms/features/controlled-vocabularies) where the default vocabulary is [COAStageVocab-1.0](/documentation/stixVocabs/COAStageVocab-1.0). For this idiom, the action is a response to some known activity so it's set to "Response".

The `Type` field, also a controlled vocabulary (default is [CourseOfActionTypeVocab-1.0](/documentation/stixVocabs/CourseOfActionTypeVocab-1.0)), indicates what general type of course of action is being described. This COA describes blocking of an IP address by perimeter firewalls, so is set to "Perimeter Blocking".

The `Objective` field describes the intended purpose of the course of action at a technical level. It consists of a text description describing that objective and a [confidence](/idioms/features/confidence) that the COA will achieve that objective. Since the objective is strightforward and the COA has a high degree of success in achieving it, that is set to high.

The `Impact` field describes the expected impact that implementing the course of action will have on normal operations. It uses [StatementType](/documentation/stixCommon/StatementType), which consists of a set of fields allowing the information producer to assert a statement about something. In this case, the `Value` field of the statement is set to "Low" (using the defualt vocabulary for this statement, [HighMediumLowVocab-1.0](/documentation/stixVocabs/HighMediumLowVocab-1.0)) and a description is given as to why the impact is low. Because this COA involves blocking an IP address that is not used for any legitimate purposes the impact to operations will be low.

Similarly, the `Cost` field is a [StatementType](/documentation/stixCommon/StatementType) field that describes the estimated cost of applying the course of action. Applying a firewall rule is cheap, and therefore the field value is set to "Low". No description is given because the statement is simple enough to not require a justification or further explanation. The `Efficacy` is yet another [StatementType](/documentation/stixCommon/StatementType) field describes the effectiveness of the COA assuming it is successful in achieving its objective.

The `Parameter_Observables` field is a set of CybOX [Observables](/documentation/cybox/ObservablesType) that describe the technical parameters to the course of action. In combination with the `Type` field, these could be used to automatically convert the course of action into something actionable in a security tool. Alternatively, they can simply be displayed in a structured fashion to the end user. In this case, the CybOX [AddressObject](/documentation/AddressObj/AddressObjectType/) is used to represent the IP address that should be blocked.

### XML

{% highlight xml linenos %}

{% endhighlight %}

[Full XML](sample.xml)

## Further Reading

See the full documentation for the relevant types for further information that may be provided:

* [CourseOfActionType](/documentation/coa/CourseOfActionType)
* [IndicatorType](/documentation/indicator/IndicatorType) - One common usage of courses of action is through the suggested course of action for an indicator.