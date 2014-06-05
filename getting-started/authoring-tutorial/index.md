---
layout: flat
---

## Prerequisites

An editor like Oxygen or XMLSpy

Knowledge of XML elements and validation against a schema.

Understanding of [STIX suggested practices](/suggestions) 

## Package up the data

All STIX content should be enclosed in STIX_Package tags, representing the title and intent of the data content.

```xml
<stix:STIX_Package>

</stix:STIX_Package>
```


### Define namespace prefixes
`STIX_Package` uses the `stix` namespace, and includes a list of namespace prefixes:

```xml
<stix:STIX_Package
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:stix="http://stix.mitre.org/stix-1"
  xmlns:stixCommon="http://stix.mitre.org/common-1"
  xmlns:cyboxCommon="http://cybox.mitre.org/common-2"
  xmlns:stixVocabs="http://stix.mitre.org/default_vocabularies-1"
  xmlns:example="http://example.com">
</stix:STIX_Package>
```

- `xsi` is required to use the `xsi:type` extension method
- `stix` defines the top-level STIX namespace  
- `stixVocabs` is the namespace for the default vocabularies
- `stixCommon` and `cyboxCommon` are library namespaces 
- `example` denotes the producer of the content, for instance your own organization. 


### Add schemaLocation

The schemaLocation attribute is a space-separated list that maps a given namespace to the file containing its schema. 
For instance, the `http://stix.mitre.org/stix-1` namespace can be found in the `http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd` schema. 

URLs are found under the  [current release](http://stix.mitre.org/language/version1.1.1/)  
Copies of schema files can also be referenced locally.

```xml
<stix:STIX_Package
<..trimmed>
  xsi:schemaLocation="
    http://stix.mitre.org/stix-1 http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd
    http://stix.mitre.org/common-1 http://stix.mitre.org/XMLSchema/common/1.1.1/stix_common.xsd
    http://cybox.mitre.org/common-1 http://cybox.mitre.org/XMLSchema/common/2.1/cybox_common.xsd
    http://stix.mitre.org/default_vocabularies-1 http://stix.mitre.org/XMLSchema/default_vocabularies/1.1.1/stix_default_vocabularies.xsd
  ">
</stix:STIX_Package>
```

### Set the version and ID fields

```xml
<stix:STIX_Package
  ...
  version="1.1.1"
  id="example:package-382ded87-52c9-4644-bab0-ad3168cbad59"
  timestamp="2014-02-20T09:00:00.000000"
  >
</stix:STIX_Package>
```

The current version of STIX is `1.1.1`
The `id` attribute is set to a globally-unique
These files can also be referenced locally for offline access.

`timestamp` is set to the creation time of this document. It can be updated later to include new information with the same ID 


## Add the STIX_Header

Add a STIX_Header element to store 

```xml
<stix:STIX_Package
  <stix:STIX_Header>
    <stix:Title> My First Package </stix:Title>
  </stix:STIX_Header>
</stix:STIX_Package>
```
### Add Intent

The package intent tells consumers what type of data is being sent. 

These fields can optionally follow a standard vocabulary, listed [in the schema](http://stix.mitre.org/language/version1.1.1/xsddocs/core/1.1.1/stix_core_xsd.html#STIXHeaderType_Package_Intent) . 

`PackageIntentVocab-1.0` can be defined in the `xsi:type` field to enforce this vocab, which we set to "Indicators - Malware Artifacts" for this example.

```xml
<stix:STIX_Header>
  <stix:Title>Example File Hash Watchlist for Fake Malware XYZ</stix:Title>
  <stix:Package_Intent xsi:type="stixVocabs:PackageIntentVocab-1.0">Indicators - Malware Artifacts</stix:Package_Intent>
</stix:STIX_Header>
```

### Add the Information Source

The information source field contains information about, naturally, the source of the watchlist. We'll fill in the author (us) and the time it was created:

```xml
<stix:STIX_Header>
  <stix:Title>Example File Hash Watchlist for Fake Malware XYZ</stix:Title>
  <stix:Package_Intent xsi:type="stixVocabs:PackageIntentVocab-1.0">Indicators - Malware Artifacts</stix:Package_Intent>
  <stix:Information_Source>
    <stixCommon:Identity>
      <stixCommon:Name>John Smith</stixCommon:Name>
    </stixCommon:Identity>
    <stixCommon:Time>
      <cyboxCommon:Produced_Time>2013-12-20T12:48:50Z</cyboxCommon:Produced_Time>
    </stixCommon:Time>
  </stix:Information_Source>
</stix:STIX_Header>
```

There are a few things we did here:

1. The `Information_Source` element is still in the STIX namespace, but the `Identity` and `Time` children are in the `stixCommon` namespace. You can see what namespace a node is in either through autocomplete (it will automatically add the correct one) or by looking at the schema.
1. You see we also use `cyboxCommon` for the `Time` element. Some places in STIX use elements from the CybOX common namespace.
1. Notice the "Z" at the end of the time. It is strongly suggested that all times in STIX and CybOX include a specification of the timezone if it is know, so in this case we set it to UTC by appending a Z. You can also use UTC offsets (-1:00), etc.

## Add the Indicator

Now that we've finished the header, let's move on to adding the indicator itself. First, we create the wrapper element and a stub indicator.

```xml
<stix:STIX_Package ...>
  <stix:STIX_Header><!-- snip --></stix:STIX_Header>
  <stix:Indicators>
    <stix:Indicator></stix:Indicator>
  </stix:Indicators>
</stix:STIX_Package>
```

Now, if you go to autocomplete new elements in the indicator you'll find that not many are available. This is because the core STIX components also use the `xsi:type` abstraction mechanism. This allows STIX Core to be used without requiring it to import each of the components. It does mean, however that we need to add the indicators schema to our document. We add the prefix mapping to the head of the document with the other namespaces and update the schemaLocation attribute to add the mapping to the actual schema:

```xml
<stix:STIX_Package
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:stix="http://stix.mitre.org/stix-1"
  xmlns:stixVocabs="http://stix.mitre.org/default_vocabularies-1"
  xmlns:stixCommon="http://stix.mitre.org/common-1"
  xmlns:cyboxCommon="http://cybox.mitre.org/common-2"
  xmlns:indicator="http://stix.mitre.org/Indicator-2"
  xmlns:example="http://example.com"
  xsi:schemaLocation="
    http://stix.mitre.org/stix-1 http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd
    http://stix.mitre.org/Indicator-2 http://stix.mitre.org/XMLSchema/indicator/2.1/indicator.xsd
    http://stix.mitre.org/common-1 http://stix.mitre.org/XMLSchema/common/1.1.1/stix_common.xsd
    http://cybox.mitre.org/common-1 http://cybox.mitre.org/XMLSchema/common/2.1/cybox_common.xsd
    http://stix.mitre.org/default_vocabularies-1 http://stix.mitre.org/XMLSchema/default_vocabularies/1.1.1/stix_default_vocabularies.xsd
  ">
```

Next, we need to set the xsi:type to `indicator:IndicatorType`. 

```xml
<stix:Indicator xsi:type="indicator:IndicatorType">
```

Before adding content, set an ID and timestamp. Following the suggesting practice, we set the prefix to our producer prefix, use "indicator-" as the basis for the ID portion, and generate a new GUID to fill in the rest:

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975" timestamp="2014-02-20T09:00:00.000000Z">
```

Like we did with STIX_Header, we also look at the suggested practices for STIX indicators to see what elements we should add. They are:

* Either Observable, Observable Composition, or Indicator Composition to represent the detectable pattern
* Title
* Type
* Valid_Time_Position
* Indicated_TTP, even if pointing to a very simple TTP with just a title
* A confidence assertion

### Set the Indicator Title and Type

`Title` and `Type` are very similar to the `Title` and `Package_Intent` fields on `STIX_Header`: title is just a title for the indicator, and type indicates what general type of indicator it is (using a controlled vocabulary).

It might be worth seeing if you can add these yourself before looking to see how I did it. Specifically, make sure you can identify the fact that `Type` is a controlled vocabulary field and, from there, figure out which vocabulary to use.

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975">
  <indicator:Title>Malware XYZ Hashes</indicator:Title>
  <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1.1">File Hash Watchlist</indicator:Type>
</stix:Indicator>
```

### Set the Observable Pattern using CybOX

Alright, this is going to get a little more complicated. Since STIX uses CybOX to represent cyber observable patterns in indicators, we need to move on to CybOX. Basically, we're filling out the "what to look for" portion of an indicator using CybOX.

Essentially we need to identify the correct CybOX object to use for file hashes and then create a static pattern observable in CybOX that represents the hash. What does that mean? First, we need an observable wrapper to contain the CybOX pattern. Then, we need an Object element to indicate that we're creating a static (stateful measure) observable instead of a dynamic (event-based) observable. Lastly, we add a CybOX object, using the Properties field, and give it the properties we want the indicator to look for.

So to start, we just need to create the CybOX observable and object wrappers:

#### Observable and Object

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975" timestamp="2014-02-20T09:00:00.000000Z">
  <indicator:Title>Malware XYZ Hashes</indicator:Title>
  <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1.1">File Hash Watchlist</indicator:Type>
  <indicator:Observable id="example:observable-3d7b08aa-88bf-4f9c-bb34-939b7548b636">
    <cybox:Object id="example:observable-5a5a0a2d-3b75-4ba6-932f-9d5f596c3c5b">
    </cybox:Object>
  </indicator:Observable>
</stix:Indicator>
```

Notice that we've assigned IDs for the Observable and Object. CybOX IDs are recommended on major components and follow the same format as STIX IDs. You'll also see that we've started using the "cybox" namespace, which has not been defined yet. If you're using an XML tool, it probably complained at you. The fix, as usual, is to import this schema.

#### Object Properties

Next, we need to identify the correct CybOX object type to use to represent file hashes. Looking through the list on the [CybOX release page](http://cybox.mitre.org/language/version2.1/), the best choice seems to be the FileObject. Opening the documentation for that object, we can see that it does include a Hashes element that we can use to represent file hashes. As we did when we added the Indicator component, we'll need to add this schema to our instance document by defining the namespace prefix in the head of the document and adding the mapping to the schema in the `schemaLocation` attribute.

```xml
<stix:STIX_Package
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:stix="http://stix.mitre.org/stix-1"
  xmlns:stixVocabs="http://stix.mitre.org/default_vocabularies-1"
  xmlns:stixCommon="http://stix.mitre.org/common-1"
  xmlns:cyboxCommon="http://cybox.mitre.org/common-2"
  xmlns:cybox="http://cybox.mitre.org/cybox-2"
  xmlns:indicator="http://stix.mitre.org/Indicator-2"
  xmlns:FileObj="http://cybox.mitre.org/objects#FileObject-2"
  xmlns:example="http://example.com"
  xsi:schemaLocation="
    http://stix.mitre.org/stix-1 http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd
    http://stix.mitre.org/Indicator-2 http://stix.mitre.org/XMLSchema/indicator/2.1/indicator.xsd
    http://stix.mitre.org/common-1 http://stix.mitre.org/XMLSchema/common/1.1.1/stix_common.xsd
    http://cybox.mitre.org/cybox-2 http://cybox.mitre.org/XMLSchema/core/2.1/cybox_core.xsd
    http://cybox.mitre.org/common-1 http://cybox.mitre.org/XMLSchema/common/2.1/cybox_common.xsd
    http://cybox.mitre.org/objects#FileObject-2 http://cybox.mitre.org/XMLSchema/objects/File/2.1/File_Object.xsd
    http://stix.mitre.org/default_vocabularies-1 http://stix.mitre.org/XMLSchema/default_vocabularies/1.1.1/stix_default_vocabularies.xsd
  ">
```

You'll need to do this every time you use a type from a new schema (generally when you use xsi:type) unless it has already been added.

Next, we'll create the `Properties` element and fill in the `xsi:type`:

```xml
<indicator:Object id="example:observable-5a5a0a2d-3b75-4ba6-932f-9d5f596c3c5b">
  <cybox:Properties xsi:type="FileObj:FileObjectType">
  </cybox:Properties>
</indicator:Object>
```

Finally, we add in the fields to represent the hash. This will vary greatly depending on what type of indicator you want to create: IP indicators, domain indicators, e-mail indicators, file indicators, etc. will all use different fields. Essentially, search through the objects and the object fields to see what you want the indicator to trigger on and add those fields.

```xml
<cybox:Properties xsi:type="FileObj:FileObjectType">
  <FileObj:Hashes>
    <cyboxCommon:Hash>
      <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0" condition="Equals">MD5</cyboxCommon:Type>
      <cyboxCommon:Simple_Hash_Value condition="Equals" apply_condition="ANY">01234567890abcdef01234567890abcdef##comma##abcdef1234567890abcdef1234567890##comma##00112233445566778899aabbccddeeff</cyboxCommon:Simple_Hash_Value>
    </cyboxCommon:Hash>
  </FileObj:Hashes>
</cybox:Properties>
```

This looks a little bit complicated, but you should be able to see the logic behind it now that you understand how STIX and CybOX work. We have a couple wrapper elements around the hashes, then a controlled vocabulary describing the type of hash and a `Simple_Hash_Value` field with the hashes to look for. Of course, you'll also seem some extra stuff there: the `condition` attributes, the `apply_condition`, and the `##comma##` separators.

#### CybOX Pattern Fields

Here's how it works: all of the lowest-level fields in CybOX representing cyber observables data extend from a field that implements CybOX patterning capability called `BaseObjectPropertyType`. That type adds fields and defines behavior for CybOX patterning. There are two fields you will see used very frequently in indicators:

* `condition`, which specifies how to match the target (data you're applying the indicator against) to the pattern
* `apply_condition`, which specifies how multiple items should be matched

As you probably guessed, `##comma## is used to separate multiple list items. So, how do you use these fields?

First, decide on an appropriate condition. For this hash match, we use "Equals" because we want to test whether file hashes equal each other. When using observables in an indicator (or really any time you use observables for patterns) you need to have the condition attribute set. Omitting it implies the CybOX observable was an instance.

As another example, if we were testing for IP Addresses in a range we might use "Starts_With" and supply a partial IP address, or if we were searching for keywords in an e-mail we could use "Contains" and supply the keywords. The various CybOX conditions and how they work are described in the schema annotations.

Next, if you have a single item to test against (single hash, single IP, whatever) you can move on, you don't need to use `@apply_condition`. If you do have multiple values, it's likely that you want the pattern to match if any of them match, in which case you should use `@apply_condition="ANY"`. This is essentially a blacklist. An alternative is to use `@apply_condition="NONE"` and provide good values instead of bad values, which is essentially a whitelist. Finally, you can test that the tested values matches ALL of the items in the list using `@apply_condition="ALL"`.

That's basically how to use CybOX patterns. Remember that to create a CybOX pattern you always need to use the `condition` attribute, even if you just set it to "Equals".

### Add the Confidence and Valid_Time_Position

It's generally a good idea to include a confidence in your indicators so you can let consumers know how confident in it you are and a valid time position to let them know when the indicator is valid for. Note that these are not required, it's just a suggested practice. In particular, in a lot of cases you won't have a defined time window for indicators. When this happens, it's fine to omit the time position.

These fields are fairly standard STIX, so I'll just show you the end result. It might be a good exercise to try adding them yourself first, though.

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975" timestamp="2014-02-20T09:00:00.000000Z">
  <indicator:Title>Malware XYZ Hashes</indicator:Title>
  <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1.1">File Hash Watchlist</indicator:Type>
  <indicator:Valid_Time_Position>
    <indicator:Start_Time>2014-01-01T12:48:50Z</indicator:Start_Time>
    <indicator:End_Time>2014-01-31T12:48:50Z</indicator:End_Time>
  </indicator:Valid_Time_Position>
  <indicator:Observable id="example:observable-3d7b08aa-88bf-4f9c-bb34-939b7548b636">
    <cybox:Object id="example:observable-5a5a0a2d-3b75-4ba6-932f-9d5f596c3c5b">
      <cybox:Properties xsi:type="FileObj:FileObjectType">
        <FileObj:Hashes>
          <cyboxCommon:Hash>
            <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0" condition="Equals">MD5</cyboxCommon:Type>
            <cyboxCommon:Simple_Hash_Value condition="Equals" apply_condition="ANY">01234567890abcdef01234567890abcdef##comma##abcdef1234567890abcdef1234567890##comma##00112233445566778899aabbccddeeff</cyboxCommon:Simple_Hash_Value>
          </cyboxCommon:Hash>
        </FileObj:Hashes>
      </cybox:Properties>
    </cybox:Object>
  </indicator:Observable>
  <indicator:Confidence>
    <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">Medium</stixCommon:Value>
  </indicator:Confidence>
</stix:Indicator>
```

The Valid_Time_Position is added above Observable (most STIX elements are ordered) and the Confidence structure is added below it. Did you catch the controlled vocabulary for Confidence/Value and remember to add the timezone for the Valid_Time_Position? We also started using a new vocabulary in the CybOX vocabularies namespace, so you would have needed to import the CybOX vocabularies namespace/schema as we did for the STIX vocab schema earlier.

## Add the TTP

Stepping back from the indicator, the next step is to represent the TTP that the indicator indicates. In STIX, TTPs are used to represent three primary concepts:

* Resources (infrastructure and tools)
* Behavior (attack patterns, malware, exploits)
* Victim Targeting

In this case, we want to represent a piece of malware. For this example we'll just give it a name, but you could also represent more complicated information about it using something like MAEC.

First, we need to import the TTP schema by defining the namespace and adding it to the schemaLocation. I won't show what this looks like for space reasons, but just replace what we did for indicator with TTP (making sure to copy the namespace and XSD location correctly).

Next, we add the TTPs element with an xsi:type, id, and timestamp:

```xml
<stix:TTPs>
  <stix:TTP xsi:type="ttp:TTPType" id="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd" timestamp="2014-02-20T09:00:00.000000Z">
  </stix:TTP>
</stix:TTPs>
```

### Setting the malware information

Next, we'll give it a title appropriate to the malware we want to represent and a Behavior/Malware instance to identify the malware:

```xml
<stix:TTP xsi:type="ttp:TTPType" id="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd">
  <ttp:Title>Malware XYZ</ttp:Title>
  <ttp:Behavior>
    <ttp:Malware>
      <ttp:Malware_Instance>
        <ttp:Name>Malware XYZ</ttp:Name>
      </ttp:Malware_Instance>
    </ttp:Malware>
  </ttp:Behavior>
</stix:TTP>
```

## Bringing it all together

Alright, now we've got an indicator with file hashes for a piece of malware and a representation of the malware itself in a TTP. How do we say that when we see the indicator, it might indicate you're seeing malware activity? Just having them in the same package is not enough.

This is where STIX relationships come in. Essentially, we want to relate the Indicator to the TTP using the "Indicated_TTP" field on the indicator:

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975" timestamp="2014-02-20T09:00:00.000000Z">
  <!-- snip -->
  <indicator:Indicated_TTP>
    <stixCommon:TTP idref="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd"/>
  </indicator:Indicated_TTP>
</stix:Indicator>
```

As you can see, a relationship is fairly straightforward to add. All you have to do is add the wrapper element, create a new TTP (no need for the `xsi:type` in this case, since `@idref` is on the base type), and set the `@idref` to the ID of the TTP that you want to point to. That TTP can be in the same document, a document you send alongside it, or even in a document that was sent at another time. Essentially, relationships in STIX are considered global, not local.

One other note about relationships is that, if we wanted, we could reference a specific version of the TTP by including the timestamp field. For example:

```xml
<indicator:Indicated_TTP>
  <stixCommon:TTP idref="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd" timestamp="2014-02-20T09:00:00.000000Z"/>
</indicator:Indicated_TTP>
```

That will reference the specific version of the TTP that was published with the timestamp "2014-02-20T09:00:00.000000Z". In this case though, we want to reference the "latest" version of that TTP as it evolves so leave off the timestamp field.

An alternative to the reference-based approach using @idref is embedding the TTP inside the indicator. For the most part, STIX relationships allow either approach.  page has some guidelines for when to use each. As an example of embedding, we can just copy the TTP itself into the indicator where previously we had the TTP with an `idref`:

```xml
<stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975">
  <!-- snip -->
  <indicator:Indicated_TTP>
    <stix:TTP xsi:type="ttp:TTPType" id="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd" timestamp="2014-02-20T09:00:00.000000Z">
      <ttp:Title>Malware XYZ</ttp:Title>
      <ttp:Behavior>
        <ttp:Malware>
          <ttp:Malware_Instance>
            <ttp:Name>Malware XYZ</ttp:Name>
          </ttp:Malware_Instance>
        </ttp:Malware>
      </ttp:Behavior>
    </stix:TTP>
  </indicator:Indicated_TTP>
  <!--snip-->
</stix:Indicator>
```

# Complete example
```xml
<stix:STIX_Package
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:stix="http://stix.mitre.org/stix-1"
  xmlns:stixVocabs="http://stix.mitre.org/default_vocabularies-1"
  xmlns:cyboxVocabs="http://cybox.mitre.org/default_vocabularies-2"
  xmlns:stixCommon="http://stix.mitre.org/common-1"
  xmlns:cybox="http://cybox.mitre.org/cybox-2"
  xmlns:cyboxCommon="http://cybox.mitre.org/common-2"
  xmlns:indicator="http://stix.mitre.org/Indicator-2"
  xmlns:ttp="http://stix.mitre.org/TTP-1"
  xmlns:FileObj="http://cybox.mitre.org/objects#FileObject-2"
  xmlns:example="http://example.com"
  xsi:schemaLocation="
    http://stix.mitre.org/stix-1 http://stix.mitre.org/XMLSchema/core/1.1.1/stix_core.xsd
    http://stix.mitre.org/Indicator-2 http://stix.mitre.org/XMLSchema/indicator/2.1/indicator.xsd
    http://stix.mitre.org/TTP-1 http://stix.mitre.org/XMLSchema/ttp/1.1.1/ttp.xsd
    http://stix.mitre.org/common-1 http://stix.mitre.org/XMLSchema/common/1.1.1/stix_common.xsd
    http://cybox.mitre.org/cybox-2 http://cybox.mitre.org/XMLSchema/core/2.1/cybox_core.xsd
    http://cybox.mitre.org/common-1 http://cybox.mitre.org/XMLSchema/common/2.1/cybox_common.xsd
    http://cybox.mitre.org/objects#FileObject-2 http://cybox.mitre.org/XMLSchema/objects/File/2.1/File_Object.xsd
    http://stix.mitre.org/default_vocabularies-1 http://stix.mitre.org/XMLSchema/default_vocabularies/1.1.1/stix_default_vocabularies.xsd
    http://cybox.mitre.org/default_vocabularies-2 http://cybox.mitre.org/XMLSchema/default_vocabularies/2.1/cybox_default_vocabularies.xsd
  "
  version="1.1.1"
  id="example:package-382ded87-52c9-4644-bab0-ad3168cbad59"
  timestamp="2014-02-20T09:00:00.000000Z">
  <stix:STIX_Header>
    <stix:Title>Example File Hash Watchlist for Fake Malware XYZ</stix:Title>
    <stix:Package_Intent xsi:type="stixVocabs:PackageIntentVocab-1.0">Indicators - Malware Artifacts</stix:Package_Intent>
    <stix:Information_Source>
      <stixCommon:Identity>
        <stixCommon:Name>John Smith</stixCommon:Name>
      </stixCommon:Identity>
      <stixCommon:Time>
        <cyboxCommon:Produced_Time>2013-12-20T12:48:50Z</cyboxCommon:Produced_Time>
      </stixCommon:Time>
    </stix:Information_Source>
  </stix:STIX_Header>
  <stix:Indicators>
    <stix:Indicator xsi:type="indicator:IndicatorType" id="example:indicator-3c3885fe-a350-4a5c-aae3-6f014df36975" timestamp="2014-02-20T09:00:00.000000Z">
      <indicator:Title>Malware XYZ Hashes</indicator:Title>
      <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1.1">File Hash Watchlist</indicator:Type>
      <indicator:Valid_Time_Position>
        <indicator:Start_Time>2014-01-01T12:48:50Z</indicator:Start_Time>
        <indicator:End_Time>2014-01-31T12:48:50Z</indicator:End_Time>
      </indicator:Valid_Time_Position>
      <indicator:Observable id="example:observable-3d7b08aa-88bf-4f9c-bb34-939b7548b636">
        <cybox:Object id="example:observable-5a5a0a2d-3b75-4ba6-932f-9d5f596c3c5b">
          <cybox:Properties xsi:type="FileObj:FileObjectType">
            <FileObj:Hashes>
              <cyboxCommon:Hash>
                <cyboxCommon:Type xsi:type="cyboxVocabs:HashNameVocab-1.0" condition="Equals">MD5</cyboxCommon:Type>
                <cyboxCommon:Simple_Hash_Value condition="Equals" apply_condition="ANY">01234567890abcdef01234567890abcdef##comma##abcdef1234567890abcdef1234567890##comma##00112233445566778899aabbccddeeff</cyboxCommon:Simple_Hash_Value>
              </cyboxCommon:Hash>
            </FileObj:Hashes>
          </cybox:Properties>
        </cybox:Object>
      </indicator:Observable>
      <indicator:Indicated_TTP>
        <stixCommon:TTP idref="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd"/>
      </indicator:Indicated_TTP>
      <indicator:Confidence>
        <stixCommon:Value xsi:type="stixVocabs:HighMediumLowVocab-1.0">Medium</stixCommon:Value>
      </indicator:Confidence>
    </stix:Indicator>
  </stix:Indicators>
  <stix:TTPs>
    <stix:TTP xsi:type="ttp:TTPType" id="example:ttp-f3eb3e3f-fb53-427e-9171-ff5bc0b1e6cd" timestamp="2014-02-20T09:00:00.000000Z">
      <ttp:Title>Malware XYZ</ttp:Title>
      <ttp:Behavior>
        <ttp:Malware>
          <ttp:Malware_Instance>
            <ttp:Name>Malware XYZ</ttp:Name>
          </ttp:Malware_Instance>
        </ttp:Malware>
      </ttp:Behavior>
    </stix:TTP>
  </stix:TTPs>
</stix:STIX_Package>
```
